from pprint import pprint

from rest_framework import  serializers

from core.models import Product


class ProductPagSerializer(serializers.Serializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'stock')

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100, allow_blank=True)
    price = serializers.FloatField()
    stock = serializers.IntegerField()


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'stock')

    name = serializers.CharField(max_length=100, allow_blank=True)
    price = serializers.FloatField()
    stock = serializers.IntegerField()

    def create(self, validated_data):
        """
            Create and return a new `Product` instance, given the validated data.
        """

        trans = []
        trans = Product.objects.create(**validated_data)

        return trans

    def update(self, instance, validated_data):
        """
            Update and return an existing `Product` instance, given the validated data.
        """

        instance.name = validated_data.get('name', instance.name)
        instance.price = validated_data.get('price', instance.price)
        instance.stock = validated_data.get('stock', instance.stock)

        instance.save()
        return instance
