import datetime

from django.test import TestCase

from core.models import Order


class OrderTest(TestCase):
    """ Test module for Product model """

    def setUp(self):

        ejemplo = str(datetime.datetime.now())[:19]
#        date_time = datetime.datetime.strptime(ejemplo, '%Y-%m-%d %H:%M:%S')

        Order.objects.create(date_time="2001-12-31 00:00:00")

    def test_product_exist(self):

        test_order = Order.objects.all()

        test_date = "2001-12-31 00:00:00+00:00"

        self.assertEqual(test_date, str(test_order[0].date_time))


