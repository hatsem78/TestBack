from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from api.common import get_check_stock, get_check_product_in_order
from api.order_detail.serializers import OrderDetailPagSerializer, OrderDetailSerializer
from core.models import OrderDetail
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
class OrderDetailadd(APIView):

    """
    List all OrderDetail, or create a new OrderDetail.
    """
    permission_classes = (IsAuthenticated, JSONWebTokenAuthentication)

    def get(self, request, format=None):
        snippets = OrderDetail.objects.all()
        serializer = OrderDetailPagSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):

        serializer = OrderDetailSerializer(data=request.data)

        try:

            if serializer.is_valid():

                check_stock, stock = get_check_stock(request.data["product"])

                check_product = get_check_product_in_order(request.data["product"])

                if check_product and "product" in request.data:

                    return Response(
                        {"msg-error": "El producto id: " + str(
                            request.data["product"]) + " no se puede repetir en la orden"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                if (not check_stock or stock < int(request.data["cuantity"])) and "product" in request.data:

                    return Response(
                        {"msg-error": "Insuficiente stock"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                serializer.save()

                serializer.initial_data['id'] = serializer.instance.id

                OrderDetailSerializer.delete_stock_prod(
                    id_producto=request.data['product'],
                    cuantity=request.data['cuantity']
                )

                return Response(serializer.initial_data, status=status.HTTP_201_CREATED)

        except Exception as error:
            errors = error.args[0]
            return Response({'error': errors}, content_type="application/json")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailDetail(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def _get_instance(validated_data):
        """
            Update and return an existing `OrderDetail` instance, given the validated data.
        """
        instance = {
            'id': validated_data.id, 
            'cuantity': validated_data.cuantity, 
            'order': validated_data.order,
            'product': validated_data.product
        }

        return instance

    @staticmethod
    def get_object(pk):
        try:
            object_locale = OrderDetail.objects.get(pk=pk)

            return object_locale
        except OrderDetail.DoesNotExist:
            from django.http import Http404
            raise Http404

    def get(self, request, pk, format=None):
        result = self.get_object(pk)

        result = self._get_instance(result)

        return Response(result)

    def put(self, request, pk, format=None):

        object = self.get_object(pk)

        serializer = OrderDetailSerializer(object, data=request.data)

        if serializer.is_valid():

            check_stock, stock = get_check_stock(request.data["product"])

            if (not check_stock or int(stock) < int(request.data["cuantity"])) and "product" in request.data:
                return Response(
                    {"msg-error": "Insuficiente stock"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            try:

                serializer.save()
            except Exception as error:
                errors = error.args[0]
                return Response({'error': errors},  status=status.HTTP_404_NOT_FOUND)

            return Response(serializer.initial_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        order_detail = self.get_object(pk)

        OrderDetailSerializer.add_stock_prod(
            order_detail.product_id,
            order_detail.cuantity
        )

        order_detail.delete()

        return Response({"msg": "Eliminado correctamente"}, status=status.HTTP_204_NO_CONTENT)


