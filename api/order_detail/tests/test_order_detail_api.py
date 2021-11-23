import datetime
import json
from pprint import pprint

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from api.order_detail.serializers import OrderDetailPagSerializer
from core.models import Order, Product, OrderDetail

CREATE_ORDER_URL = reverse('order_detail:add')


def create_user(**params):
    """Helper function to create new user"""
    return get_user_model().objects.create_user(**params)


class OrderApiTests(TestCase):
    """Test the users API (public)"""

    def setUp(self):
        self.client = APIClient()

        self.user = create_user(
            email='test@londonappdev.com',
            password='testpass',
            name='fname',
        )

        self.one = Order.objects.create(date_time='2021-01-05')
        self.two = Order.objects.create(date_time='2021-01-01')

        self.banana = Product.objects.create(name='Banana', price=3, stock=100)
        self.pera = Product.objects.create(name='Pera', price=3, stock=100)

        self.manzana = Product.objects.create(name='Manzana', price=3, stock=100)

        self.kigui = Product.objects.create(name='kigui', price=3, stock=10)

        self.order_detail_one = OrderDetail.objects.create(
            order=self.one,
            product=self.banana,
            cuantity=10
        )

        self.order_detail_two = OrderDetail.objects.create(
            order=self.two,
            product=self.pera,
            cuantity=10
        )

        self.order_detail_three = OrderDetail.objects.create(
            order=self.two,
            product=self.kigui,
            cuantity=10
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_order_detail_success(self):
        """Test creating using with a valid payload is successful"""

        payload = {
            "order": self.one.pk,
            "product": self.manzana.pk,
            "cuantity": 10
        }

        response = self.client.post(CREATE_ORDER_URL, payload, format='json')

        order = OrderDetail.objects.get(id=self.order_detail_one.pk)

        serializer = OrderDetailPagSerializer(order)

        resp = json.loads(response.content)

        self.assertEqual(serializer.data['cuantity'], resp['cuantity'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_order_detail_stock_hay(self):
        """Test creating using with a valid payload is successful"""

        payload = {
            "order": self.one.pk,
            "product": self.manzana.pk,
            "cuantity": 400
        }

        response = self.client.post(CREATE_ORDER_URL, payload, format='json')

        resp = json.loads(response.content)

        self.assertEqual(resp['msg-error'], 'Insuficiente stock')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_product_not_found(self):
        """Test creating using with a valid payload product is not found"""

        payload = {
            "order": self.one.pk,
            "product": 50,
            "cuantity": 20
        }

        base_url = reverse(
            "order_detail:update",
            kwargs={'pk': self.order_detail_one.pk}
        )

        response = self.client.put(base_url, payload)

        resp = json.loads(response.content)

        self.assertEqual(resp["detail"], 'Not found.')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_order_not_found(self):
        """Test creating using with a valid payload order is not found"""

        payload = {
            "order": 50,
            "product": self.banana.pk,
            "cuantity": 20
        }

        base_url = reverse(
            "order_detail:update",
            kwargs={'pk': self.order_detail_one.pk}
        )

        response = self.client.put(base_url, payload)

        resp = json.loads(response.content)

        self.assertEqual(resp["error"], "Order matching query does not exist.")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_order_detail_not_found(self):
        """Test creating using with a valid payload is successful"""

        payload = {
            "order": self.one.pk,
            "product": self.banana.pk,
            "cuantity": 20
        }

        base_url = reverse(
            "order_detail:update",
            kwargs={'pk': 20}
        )

        response = self.client.put(base_url, payload)

        resp = json.loads(response.content)

        self.assertEqual(resp["detail"], 'Not found.')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_order_detail_success(self):
        """Test update using with a valid payload is successful"""

        payload = {
            "order": self.one.pk,
            "product": self.banana.pk,
            "cuantity": 20
        }

        base_url = reverse(
            "order_detail:update",
            kwargs={'pk': self.order_detail_one.pk}
        )

        response = self.client.put(base_url, payload)

        resp = json.loads(response.content)

        self.assertEqual(20, int(resp['cuantity']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_order_detail_insufficient_stock(self):
        """Test update using with a valid payload is insufficient stock"""

        payload = {
            "order": self.one.pk,
            "product": self.kigui.pk,
            "cuantity": 20
        }

        base_url = reverse(
            "order_detail:update",
            kwargs={'pk': self.order_detail_three.pk}
        )

        response = self.client.put(base_url, payload)

        resp = json.loads(response.content)

        self.assertEqual("Insuficiente stock", resp['msg-error'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_order_detail_delete(self):
        base_url = reverse(
            "order_detail:delete",
            kwargs={'pk': self.order_detail_two.pk}
        )

        response = self.client.delete(base_url)

        self.assertEqual({'msg': 'Eliminado correctamente'}, response.data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
