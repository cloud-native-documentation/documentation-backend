from rest_framework import serializers
from .models import Doc, Dir, Project


class DocSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doc

class DirSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dir
        
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
