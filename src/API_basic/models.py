from django.db import models


import uuid
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin

# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# Todo lo relacionado al usuario

class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None):

        if username is None:
            raise TypeError('Users should have a username')

        if email is None:
            raise TypeError('El usuario debe tener un email')

        user = self.model(username=username, email=self.normalize_email(email))

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password=None):

        if password is None:
            raise TypeError('Users should have a password')

        user = self.create_user(username, email, password)

        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractUser, PermissionsMixin):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)

    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email' # Solicita el email en vez del username
    REQUIRED_FIELDS = ['username']

    objects = UserManager() # Tell django how to manage objects of these types

    def __str__(self):
        return self.email

    def tokens(self):
        return ''

    
