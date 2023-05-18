from django.db import models
from django.contrib.auth.models import AbstractDoc


# Create your models here.

class Project(models.Model):
    # Fields
    projectname = models.CharField(max_length=50)
    permission_list = 


class Dir(models.Model):
    dirname = models.CharField(max_length=50)
    dirpath = models.CharField(max_length=50)
    project = models.ForeignKey('Project')


class Doc(models.Model):
    # Fields
    docname = models.CharField(max_length=50)
    docpath = models.CharField(max_length=50)
    content = models.CharField(max_length=50000)
    project = models.ForeignKey('Project')

    # Metadata
    class Meta:
        ordering = ['id', 'docname', 'docpath', 'content']
        verbose_name = 'doc'
        verbose_name_plural = 'docs'
        db_table = 'document'

    # Methods
    def __str__(self):
        return self.docname
