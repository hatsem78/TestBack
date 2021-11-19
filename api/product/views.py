from pprint import pprint

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from api.product.serializers import ProductPagSerializer, ProductSerializer
from core.models import Product


class ProductAdd(APIView):
    """
    List all Product, or create a new snippet.
    """
    def get(self, request, format=None):
        snippets = Product.objects.all()
        serializer = ProductPagSerializer(snippets, many=True)
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

    def _getInstance(self, validated_data):
        """
            Update and return an existing `Product` instance, given the validated data.
        """
        instance = {}
        instance['id'] = validated_data.id
        instance['name'] = validated_data.name
        instance['price'] = validated_data.price
        instance['stock'] = validated_data.stock

        return instance

    def get_object(self, pk):
        try:
            object = Product.objects.get(pk=pk)
            return object
        except Product.DoesNotExist:
            from django.http import Http404
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = ProductSerializer(snippet)
        result = self._getInstance(snippet)

        return Response(result)

    def put(self, request, pk, format=None):

        object = self.get_object(pk)

        serializer = ProductSerializer(object, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(self._getInstance(serializer.instance))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
