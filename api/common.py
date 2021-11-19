import json
from abc import ABC
from pprint import pprint

import requests
from django.db.models import Func, IntegerField, CharField, QuerySet
from rest_framework.pagination import PageNumberPagination
import collections
from datetime import datetime

from rest_framework.response import Response

from api.product.serializers import ProductPagSerializer
from core.models import OrderDetail, Product


class PivoteDict:
    __datetime_format = '%b-%y'
    __datetime_format_out = ""
    __datetime_format_in = ""
    __data = []
    __group_by = []
    __list_result = []
    __order = []
    __pivot = ''
    __field_order = ''

    def __init__(self, data_info, group_by_info, date_format_out=None, order_list=None, field_order=None, pivot=None,
                 date_format_in=None):
        self.data = data_info
        self.group_by = group_by_info
        self.datetime_format_out = '%b-%y' if date_format_out is None else date_format_out
        self.datetime_format_in = "%Y-%m-%d %H:%M:%S+00:00" if date_format_in is None else date_format_in
        self.order = order_list
        self.field_order = field_order
        self.pivot = pivot
        self.__list_result = []

    @property
    def datetime_format_out(self):
        return self.__datetime_format_out

    @datetime_format_out.setter
    def datetime_format_out(self, value):
        if not isinstance(value, (str,)):
            raise TypeError('It must be a str object')
        self.__datetime_format_out = value

    @property
    def datetime_format_in(self):
        return self.__datetime_format_in

    @datetime_format_in.setter
    def datetime_format_in(self, value):
        if not isinstance(value, (str,)):
            raise TypeError('It must be a str object')
        self.__datetime_format_in = value

    @property
    def group_by(self):
        return self.__group_by

    @group_by.setter
    def group_by(self, value):
        if not isinstance(value, (list, str)):
            raise TypeError('It must be a str object')
        self.__group_by = value

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, value):
        if not isinstance(value, (list, QuerySet)):
            raise TypeError('It must be a str object or  QuerySet')
        self.__data = value

    @property
    def order(self):
        return self.__order

    @order.setter
    def order(self, value):
        if not isinstance(value, (list,)):
            raise TypeError('It must be a str object')
        self.__order = value

    @property
    def field_order(self):
        return self.__field_order

    @field_order.setter
    def field_order(self, value):
        if not isinstance(value, (str,)):
            raise TypeError('It must be a str object')
        self.__field_order = value

    @property
    def pivot(self):
        return self.__pivot

    @pivot.setter
    def pivot(self, value):
        if not isinstance(value, (str,)):
            raise TypeError('It must be a str object')
        self.__pivot = value

    @property
    def list_result(self):
        return self.__list_result

    @list_result.setter
    def list_result(self, value):
        if not isinstance(value, (list,)):
            raise TypeError('It must be a str object')
        self.__list_result = value

    def order_list(self, group_by, lista):
        order_list = self.order.copy()
        field_group = ''

        for elemento in lista:
            if elemento['name_media'] is not None:
                order_list[self.order.index(elemento['name_media'].lower())] = round(elemento['value'], 2)
        if isinstance(group_by, (datetime,)):
            field_group = datetime.strptime(str(group_by), self.datetime_format_in).strftime(self.datetime_format_out)

        order_list.insert(0, field_group)

        return order_list

    def group_by_list(self):

        grouped = collections.defaultdict(list)

        for item in self.data:
            grouped[item[self.group_by]].append(item)

        for model, group in grouped.items():
            self.order.index(item[self.field_order].lower())
            self.list_result.append(self.order_list(model, group))

    def result(self):
        self.group_by_list()
        return self.list_result


class Pagination(PageNumberPagination):
    page_size = 15

    def get_paginated_response(self, data):

        if 'page' in self.request.query_params:
            return Response({
                "prev_page_url": self.get_previous_link(),
                "from": self.page.paginator.page_range.start,
                "to": self.page.paginator.num_pages,
                "total": self.page.paginator.num_pages,
                "per_page": self.request.query_params['per_page'],
                "current_page": self.page.number,
                "last_page": (self.page.paginator.page_range.stop - 1),
                "next_page_url": self.get_next_link(),
                'data': data,
            })
        else:
            return Response({
                "prev_page_url": self.get_previous_link(),
                "from": 1,
                "to": self.page.paginator.num_pages,
                "total": self.page.paginator.num_pages,
                "per_page": 1,
                "current_page": self.page.number,
                "last_page": 1,
                "next_page_url": self.get_next_link(),
                'data': data,
            })


class Round(Func):
    function = 'ROUND'
    arity = 2


class Day(Func, ABC):
    function = 'EXTRACT'
    template = '%(function)s(DAY from %(expressions)s)'
    output_field = IntegerField()


class Month(Func, ABC):
    function = 'MONTHNAME'
    template = '%(function)s( %(expressions)s)'
    output_field = CharField()


class Week(Func, ABC):
    function = 'EXTRACT'
    template = '%(function)s(WEEK from %(expressions)s)'
    output_field = IntegerField()


def get_total_pesos(pk):
    total = 0.0

    order_detail = OrderDetail.objects.filter(order=pk)

    order_detail = order_detail.values("cuantity", "product_id__name", "product_id__price")

    for element in order_detail:
        total += float(element["product_id__price"])

    return round(total, 2)


def get_total_dolar(pk):
    url = "https://www.dolarsi.com/api/api.php?type=valoresprincipales"

    response = requests.get(url)

    response = json.loads(response.content)

    for element in response:
        if "Dolar Blue" == element["casa"]["nombre"]:
            float(element["casa"]["venta"].replace(",", "."))

    dolar = [float(element["casa"]["venta"].replace(",", ".")) for element in response if
             "Dolar Blue" == element["casa"]["nombre"]][0]

    return round(dolar * get_total_pesos(pk), 2)


def get_check_stock(pk):
    prod = Product.objects.filter(id=int(pk)).values()

    stock = prod[0]["stock"]

    flag = True if stock > 0 else False

    return flag


def get_check_product_in_order(id_product):

    order = OrderDetail.objects.filter(product=id_product)

    return True if len(order) > 0 else False

