from pprint import pprint

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from api.product.serializers import ProductPagSerializer, ProductSerializer
from core.models import Product
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
class ProductAdd(APIView):
    """
    List all Product, or create a new snippet.
    """
    permission_classes = (IsAuthenticated, JSONWebTokenAuthentication)

    def get(self, request, format=None):
        product = Product.objects.all()
        serializer = ProductPagSerializer(product, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):

        serializer = ProductSerializer(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                serializer.initial_data['id'] = serializer.instance.id
                return Response(serializer.initial_data, status=status.HTTP_201_CREATED)
        except Exception as error:
            errors = error.args[0]
            return Response({'error': errors}, content_type="application/json")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetail(APIView):
    permission_classes = (IsAuthenticated,)

    def _getInstance(self, validated_data):
        """
            Update and return an existing `Product` instance, given the validated data.
        """
        instance = {
            'id': validated_data.id,
            'name': validated_data.name,
            'price': validated_data.price,
            'stock': validated_data.stock
        }

        return instance

    @staticmethod
    def get_object(pk):
        try:
            object = Product.objects.get(pk=pk)
            return object
        except Product.DoesNotExist:
            from django.http import Http404
            raise Http404

    def get(self, request, pk, format=None):
        product = self.get_object(pk)

        result = self._getInstance(product)

        return Response(result)

    def put(self, request, pk, format=None):

        product = self.get_object(pk)

        serializer = ProductSerializer(product, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(self._getInstance(serializer.instance))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        product = self.get_object(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
