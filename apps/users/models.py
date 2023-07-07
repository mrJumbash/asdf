from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    USERNAME_FIELD = 'username'
    image = models.ImageField(upload_to='user_photo', default='user_photo/default.jpg')
    email = models.EmailField(verbose_name='Почта', max_length=150, unique=True)
    about_me = models.TextField(blank=True, max_length=280, default='')
    timezone = models.CharField(max_length=50, blank=True, null=True)


class ConfirmCode(models.Model):
    username = models.CharField(max_length=150, unique=True)
    code = models.CharField(max_length=10)


class ResetPasswordCode(models.Model):
    code = models.CharField(max_length=6)
    email = models.EmailField(unique=True)
