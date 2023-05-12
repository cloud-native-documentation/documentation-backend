from django.db import models
from django.contrib.auth.models import AbstractDoc


# Create your models here.

class Doc(models.Model):
    docname = models.CharField(max_length=50)
    docpath = models.CharField(max_length=50)
    content = models.CharField(max_length=50000)
    
class Dir(models.Model):
    dirname = models.CharField(max_length=50)
    dirpath = models.CharField(max_length=50)
