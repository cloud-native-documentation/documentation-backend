from django.db import models

# Create your models here.

class Project(models.Model):
    # Fields
    id = models.AutoField(primary_key=True)
    projectname = models.CharField(max_length=150)
    department = models.CharField(max_length=150)
    owner = models.CharField(max_length=150)
    description = models.CharField(max_length=1500)


class Dir(models.Model):
    id = models.AutoField(primary_key=True)
    dirname = models.CharField(max_length=150)
    project = models.CharField(max_length=150)
    owner = models.CharField(max_length=150)


class Doc(models.Model):
    # Fields
    id = models.AutoField(primary_key=True)
    file = models.CharField(max_length=150)
    directory = models.CharField(max_length=150)
    project = models.CharField(max_length=150)
    owner = models.CharField(max_length=150)
    public = models.CharField(max_length=1)
    private = models.CharField(max_length=1)
    cnt = models.IntegerField()
    department = models.CharField(max_length=150)
    isDelete = models.BooleanField()


class HistoryAction(models.Model):
    id = models.AutoField(primary_key=True)
    project = models.CharField(max_length=150)
    directory = models.CharField(max_length=150, null=True)
    file = models.CharField(max_length=150, null=True)
    fileid = models.IntegerField(null=True)
    username = models.CharField(max_length=150)
    action = models.CharField(max_length=150)
    modify_date = models.DateTimeField(auto_now_add=True)
    version = models.IntegerField()
    isFile = models.BooleanField()