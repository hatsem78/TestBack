from rest_framework import  serializers
from rest_framework.fields import CharField

from api.common import get_total_pesos, get_total_dolar

from core.models import Order, OrderDetail


class OrderPagSerializer(serializers.ModelSerializer):

    product = CharField(write_only=True)
    total_pesos = CharField(write_only=True)
    total_dolar = CharField(write_only=True)

    class Meta:
        model = Order
        fields = ('id', 'date_time',  "product", "total_pesos", "total_dolar")

    id = serializers.IntegerField()
    date_time = serializers.DateTimeField()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        pk = data["id"]
        order_detail = OrderDetail.objects.filter(order=pk)
        data["product"] = order_detail.values("cuantity", "product_id__name", "product_id__price")
        data['total_pesos'] = get_total_pesos(pk)
        data['total_dolar'] = get_total_dolar(pk)
        return data



class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ('id', 'date_time')

    id = serializers.IntegerField(read_only=True)
    date_time = serializers.DateTimeField()

    def create(self, validated_data):
        """
            Create and return a new `Order` instance, given the validated data.
        """

        trans = []
        trans = Order.objects.create(**validated_data)

        return trans

    def update(self, instance, validated_data):
        """
            Update and return an existing `Order` instance, given the validated data.
        """

        instance.date_time = validated_data.get('date_time', instance.date_time)

        instance.save()
        return instance
