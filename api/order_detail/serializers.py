from pprint import pprint

from rest_framework import serializers

from copy import copy, deepcopy
from core.models import OrderDetail, Order, Product


class OrderDetailPagSerializer(serializers.Serializer, ):
    class Meta:
        model = OrderDetail
        fields = ('id', "order", 'product_name', "product_price", 'cuantity')

    id = serializers.IntegerField(read_only=True)
    cuantity = serializers.IntegerField()
    product_name = serializers.CharField(max_length=200, allow_blank=True)
    product_price = serializers.FloatField()


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = ('id', 'order', 'cuantity', 'product')

    id = serializers.IntegerField(read_only=True)
    cuantity = serializers.IntegerField()
    order = serializers.IntegerField()
    product = serializers.IntegerField()

    def create(self, validated_data):
        """
            Create and return a new `OrderDetail` instance, given the validated data.
        """

        trans = []

        validated_data['order'] = Order.objects.get(id=validated_data['order'])
        validated_data['product'] = Product.objects.get(id=validated_data['product'])

        trans = OrderDetail.objects.create(**validated_data)

        return trans

    def update(self, instance, validated_data):
        """
            Update and return an existing `OrderDetail` instance, given the validated data.
        """

        old_cuantity = copy(instance.cuantity)

        instance.cuantity = validated_data.get('cuantity', instance.cuantity)
        instance.order = Order.objects.get(id=validated_data['order'])
        instance.product = Product.objects.get(id=validated_data['product'])

        instance.save()

        self.update_stock_prod(
            validated_data['order'],
            int(validated_data.get('cuantity', instance.cuantity)),
            old_cuantity

        )

        return instance

    @staticmethod
    def delete_stock_prod(id_producto, cuantity):

        prod = Product.objects.get(id=id_producto)

        prod.stock = int(prod.stock) - int(cuantity)
        prod.save()

    @staticmethod
    def add_stock_prod(id_producto, cuantity):

        prod = Product.objects.get(id=id_producto)

        prod.stock = int(prod.stock) + int(cuantity)
        prod.save()

    @staticmethod
    def update_stock_prod(id_producto, cuantity, old_cuantity):

        prod = Product.objects.get(id=id_producto)

        if cuantity < old_cuantity:
            result = old_cuantity - cuantity
            prod.stock = prod.stock + result
        else:
            result = cuantity - old_cuantity
            prod.stock = prod.stock - result

        prod.save()
