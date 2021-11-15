#! -.- coding: utf-8 -.-

import datetime
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
from django.conf import settings


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new User"""
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Tag(models.Model):
    """Tag to be used for a recipe"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Product(models.Model):
    """Save product"""

    id = models.AutoField(primary_key=True, help_text="Unique id")
    name = models.CharField(max_length=250, blank=True, help_text="Product name")
    price = models.FloatField(default=0, blank=True, help_text="Product price")
    stock = models.IntegerField(default=0, help_text="Product stock")


class Order(models.Model):
    id = models.AutoField(primary_key=True, help_text="Unique id")
    date_time = models.DateTimeField(blank=True, editable=True, help_text="Order date time")

    def get_date_time(self):
        date_time = datetime.datetime.strptime(str(self.date_time).replace('/', '-')[:19], '%Y-%m-%d %H:%M:%S')
        return date_time.strftime('%Y-%m-%d %H:%M:%S')


class OrderDetail(models.Model):
    order = models.ForeignKey('Order', related_name='OrderDetailOrder', on_delete=models.CASCADE,
                              null=True)
    cuantity = models.IntegerField(default=0, help_text="Order detail  cuantity")
    product = models.ManyToManyField(Product, help_text='Select a product for this order')
