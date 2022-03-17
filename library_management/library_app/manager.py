import time
from hashlib import md5

from django.contrib.auth.base_user import BaseUserManager


class AppUserManager(BaseUserManager):
    use_in_migrations = True

    @staticmethod
    def create_user_id():
        user_id_hash = md5()
        user_id_hash.update(str(time.time()).encode())
        key = user_id_hash.hexdigest()
        return key

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('user_id', self.create_user_id())
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_id', self.create_user_id())
        extra_fields.setdefault('role', '')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

    def get_by_natural_key(self, username):
        return self.get(**{f'{self.model.USERNAME_FIELD}__iexact': username})
