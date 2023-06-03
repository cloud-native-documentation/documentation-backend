from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Dir
import os

User = get_user_model()
root_dir = './store/files'

class DirSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dir
        fields = '__all__'
        read_only_fields = ('owner',)
        

    def create(self, validated_data):
        projectpath = f'{root_dir}/{ validated_data["project"]}'
        dirpath = f'{projectpath}/{ validated_data["dirname"] }'
        os.popen(f'mkdir -p {projectpath}')
        os.popen(f'mkdir -p {dirpath}')
        user = self.context['request'].user
        instance = Dir.objects.create(
            project=validated_data['project'],
            dirname=validated_data['dirname'],
            owner=user
        )
        instance.save()
        return instance
    
    def validate_dirname(self, dirname):
        if dirname == '/':
            raise serializers.ValidationError("directory cannot be '/'")
        return dirname

