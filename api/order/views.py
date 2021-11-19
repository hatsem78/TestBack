import datetime
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from api.common import get_total_dolar, get_total_pesos
from api.order.serializers import OrderPagSerializer, OrderSerializer
from api.order_detail.serializers import OrderDetailPagSerializer, OrderDetailSerializer
from core.models import Order, OrderDetail


class OrderAdd(APIView):
    """
    List all Order, or create a new snippet.
    """
    def get(self, request, format=None):
        snippets = Order.objects.all()
        serializer = OrderPagSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):

        date_time = datetime.datetime.strptime(request.data['date_time'].replace('/', '-'), '%Y-%m-%d')
        request.data['date_time'] = date_time

        serializer = OrderSerializer(data=request.data)

        try:
            if serializer.is_valid():
                serializer.save()
                serializer.initial_data['id'] = serializer.instance.id
                return Response(serializer.initial_data, status=status.HTTP_201_CREATED)
        except Exception as error:
            errors = error.args[0]
            return Response({'error': errors}, content_type="application/json")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetails(APIView):

    def _getInstance(self, validated_data):
        """
            Update and return an existing `Order` instance, given the validated data.
        """
        instance = {
            'id': validated_data.id,
            'date_time': validated_data.date_time.strftime('%Y-%m-%d')
        }

        return instance

    def get_object(self, pk):
        try:
            object = Order.objects.get(pk=pk)
            return object
        except Order.DoesNotExist:
            from django.http import Http404
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = OrderSerializer(snippet)
        result = self._getInstance(snippet)
        order_detail = OrderDetail.objects.filter(order=pk)

        result["product"] = order_detail.values("cuantity", "product_id__name", "product_id__price")
        result['total_pesos'] = get_total_pesos(pk)
        result['total_dolar'] = get_total_dolar(pk)

        return Response(result)

    def put(self, request, pk, format=None):

        object = self.get_object(pk)

        date_time = datetime.datetime.strptime(request.data['date_time'].replace('/', '-'), '%Y-%m-%d')
        request.data['date_time'] = date_time

        serializer = OrderSerializer(object, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(self._getInstance(serializer.instance))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):

        self.update_stock_product(pk)
        snippet = self.get_object(pk)
        snippet.delete()

        return Response({"delete": "ok"}, status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def update_stock_product(id_order):

        order_detail = OrderDetail.objects.filter(order=id_order).values()

        for element in order_detail:

            OrderDetailSerializer.add_stock_prod(
                element['product_id'],
                element['cuantity']
            )



