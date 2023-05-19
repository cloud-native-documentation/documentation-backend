from django.db import models
from django.contrib.auth.models import AbstractDoc


# Create your models here.

class Project(models.Model):
    # Fields
    id = models.AutoField(primary_key=True)
    projectname = models.CharField(max_length=50)
    department = models.CharField(max_length=50)

    # Metadata
    class Meta:
        ordering = ['id', 'projectname', 'department']
        verbose_name = 'project'
        verbose_name_plural = 'projects'
        db_table = 'project'

    # Methods
    def __str__(self):
        return self.projectname


class Dir(models.Model):
    id = models.AutoField(primary_key=True)
    dirname = models.CharField(max_length=50)
    project = models.ForeignKey('Project')

    # Metadata
    class Meta:
        ordering = ['id', 'dirname', 'project']
        verbose_name = 'dir'
        verbose_name_plural = 'dirs'
        db_table = 'directory'

    # Methods
    def __str__(self):
        return self.dirname


class Doc(models.Model):
    # Fields
    id = models.AutoField(primary_key=True)
    docname = models.CharField(max_length=50)
    directory = models.CharField(max_length=100, default=None)
    project = models.ForeignKey('Project')
    owner = models.ForeignKey('User')
    public = models.BooleanField(default=False)
    private = models.BooleanField(default=False)
    content = models.CharField(max_length=50000)

    # Metadata
    class Meta:
        ordering = ['id', 'docname', 'directory', 'project', 'owner', 'public', 'private', 'content']
        verbose_name = 'doc'
        verbose_name_plural = 'docs'
        db_table = 'document'

    # Methods
    def __str__(self):
        return self.docname
