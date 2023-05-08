from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    department = models.CharField(max_length=100)
