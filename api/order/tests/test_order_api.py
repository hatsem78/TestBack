import json

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from api.order.serializers import OrderPagSerializer
from core.models import Order

CREATE_ORDER_URL = reverse('order:add')


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

        self.one = Order.objects.create(date_time='2021-01-01')
        self.two = Order.objects.create(date_time='2021-01-01')

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_order_success(self):
        """Test creating using with a valid payload is successful"""

        payload = {
            "date_time": "2021-01-03",
        }

        res = self.client.post(CREATE_ORDER_URL, payload, format='json')

        order = Order.objects.get(date_time="2021-01-03")

        serializer = OrderPagSerializer(order)

        self.assertEqual(serializer.data, serializer.data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_update_order_success(self):
        payload = {
            "date_time": "2021-01-03"
        }

        base_url = reverse(
            "order:update",
            kwargs={'pk': self.one.pk}
        )

        response = self.client.put(base_url, payload, format='json')

        self.assertEqual("2021-01-03", response.data['date_time'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_order_not_found(self):
        """Test creating using with a valid payload not found"""
        payload = {
            "date_time": "2021-01-03"
        }

        base_url = reverse(
            "order:update",
            kwargs={'pk': 50}
        )

        response = self.client.put(base_url, payload, format='json')

        resp = json.loads(response.content)

        self.assertEqual(resp["detail"], 'Not found.')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_order_delete(self):
        base_url = reverse(
            "order:delete",
            kwargs={'pk': self.two.pk}
        )

        response = self.client.delete(base_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
