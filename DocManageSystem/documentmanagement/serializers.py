from rest_framework import serializers
from .models import Doc, Dir


class DocSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doc
        fields = ('id', 'docname', 'docpath', 'content')

class DirSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dir
        fields = ('id', 'dirname', 'dirpath', 'list')
