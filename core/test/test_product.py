from django.test import TestCase

from core.models import Product


class ProductTest(TestCase):
    """ Test module for Product model """

    def setUp(self):

        Product.objects.create(name='Banana', price=3, stock=100)

        Product.objects.create(name='Manzana', price=3, stock=100)

    def test_product_exist(self):

        test_product = Product.objects.get(name='Banana')

        self.assertEqual(
            test_product.name, "Banana")
        self.assertEqual(
            test_product.stock, 100)

    def test_product_exist(self):

        test_product = Product.objects.get(name='Banana')

        self.assertEqual(
            test_product.name, "Banana")
        self.assertEqual(
            test_product.stock, 100)
