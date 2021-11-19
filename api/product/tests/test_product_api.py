from pprint import pprint

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.utils import json

from api.product.serializers import ProductPagSerializer
from core.models import Product

CREATE_USER_URL = reverse('product:add')


def create_user(**params):
    """Helper function to create new user"""
    return get_user_model().objects.create_user(**params)


class ProductApiTests(TestCase):
    """Test the users API (public)"""

    def setUp(self):
        self.client = APIClient()

        self.user = create_user(
            email='test@londonappdev.com',
            password='testpass',
            name='fname',
        )
        self.banana = Product.objects.create(name='Banana', price=3, stock=100)
        self.pera = Product.objects.create(name='Pera', price=3, stock=100)

        Product.objects.create(name='Manzana', price=3, stock=100)

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_product_success(self):
        """Test creating using with a valid payload is successful"""
        payload = {
          "name": "banana",
          "price": 30.52,
          "stock": 100
        }

        res = self.client.post(CREATE_USER_URL, payload)

        product = Product.objects.get(name="banana")

        serializer = ProductPagSerializer(product)

        self.assertEqual(serializer.data, serializer.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_update_product_success(self):


        payload = {
            "name": "banana",
            "price": 30.52,
            "stock": 100
        }

        response = self.client.put("http://0.0.0.0:8010/api/product/update/1/", payload)

        self.assertEqual('banana', response.data['name'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_deletey(self):
        response = self.client.delete("http://0.0.0.0:8010/api/product/update/"+
                                      str(self.pera.pk) + "/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

