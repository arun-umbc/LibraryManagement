from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from library_app.manager import AppUserManager
from utilities.constants import ROLE_TYPES


class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.CharField(max_length=200, primary_key=True)
    email = models.EmailField(unique=True, db_index=True)
    role = models.CharField(max_length=100, choices=ROLE_TYPES.choices(), db_index=True)
    first_name = models.CharField(max_length=300, null=True, blank=True)
    last_name = models.CharField(max_length=300, null=True, blank=True)
    request = models.ManyToManyField("Book", through="Request", related_name='user_request')
    reserve = models.ManyToManyField("Book", through="Reserve", related_name='user_reserve')
    is_active = models.BooleanField(default=True, db_index=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AppUserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        db_table = 'users'


class Book(models.Model):
    book_id = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=300, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'book'


class Request(models.Model):
    request_id = models.CharField(max_length=200, primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name="request_user")
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name="request_book")
    request_status = models.CharField(max_length=100, choices=ROLE_TYPES.choices())
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'request'


class Reserve(models.Model):
    reserve_id = models.CharField(max_length=200, primary_key=True)
    request = models.ForeignKey('Request', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name="reserve_user")
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name="reserve_book")
    rented_date = models.DateTimeField(null=True, blank=True)
    return_date = models.DateTimeField(null=True, blank=True)
    returned_date = models.DateTimeField(null=True, blank=True)
    fine = models.ForeignKey('Fine', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'reserve'


class Renew(models.Model):
    renew_id = models.CharField(max_length=200, primary_key=True)
    reserve = models.ForeignKey('Reserve', on_delete=models.CASCADE)
    renewed_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'renew'


class Fine(models.Model):
    fine_id = models.CharField(max_length=200, primary_key=True)
    amount = models.FloatField(null=True, blank=True)
    fine_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'fine'
