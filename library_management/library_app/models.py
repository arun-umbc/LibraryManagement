from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from library_app.manager import AppUserManager
from utilities.constants import ROLE_TYPES, DEPARTMENTS, STUDY_LEVEL, REQUEST_STATUS, REQUEST_FOR, RESERVE_STATUS


class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.CharField(max_length=200, primary_key=True)
    role = models.CharField(max_length=100, choices=ROLE_TYPES.choices(), db_index=True)
    request = models.ManyToManyField("Book", through="Request", related_name='user_request')
    department = models.CharField(max_length=100, choices=DEPARTMENTS.choices(), db_index=True)
    study_level = models.CharField(max_length=100, choices=STUDY_LEVEL.choices(), db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AppUserManager()

    USERNAME_FIELD = 'user_id'

    class Meta:
        db_table = 'users'


class Book(models.Model):
    book_id = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=300, null=True, blank=True)
    author = models.CharField(max_length=300, null=True, blank=True)
    total_copies = models.IntegerField(default=0)
    copies_available_rent = models.IntegerField(default=0)
    copies_available_sale = models.IntegerField(default=0)
    fine = models.FloatField(default=0)
    price = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'book'


class Request(models.Model):
    request_id = models.CharField(max_length=200, primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name="request_user")
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name="request_book")
    request_status = models.CharField(max_length=100, choices=REQUEST_STATUS.choices())
    request_for = models.CharField(max_length=100, choices=REQUEST_FOR.choices())
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'request'


class Reserve(models.Model):
    reserve_id = models.CharField(max_length=200, primary_key=True)
    request = models.ForeignKey('Request', on_delete=models.CASCADE)
    rented_date = models.DateTimeField(null=True, blank=True)
    return_date = models.DateTimeField(null=True, blank=True)
    returned_date = models.DateTimeField(null=True, blank=True)
    purchase_date = models.DateTimeField(null=True, blank=True)
    fine = models.FloatField(default=0)
    reserve_status = models.CharField(max_length=100, choices=RESERVE_STATUS.choices())
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'reserve'
