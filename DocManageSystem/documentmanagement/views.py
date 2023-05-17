from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Doc, Dir
from .serializers import DocSerializer, DirSerializer

@api_view(['GET'])
def dir_list(request):
    dirs = Dir.objects.all()
    serializer = DirSerializer(dirs, many=True)
    # document list, status
    return Response(serializer.data)
        

@api_view(['GET'])
def doc_view(request):
    docs = Doc.objects.all()
    serializer = DocSerializer(docs, many=True)
    # content, status code
    return Response(serializer.data)
        

@api_view(['POST'])
def doc_create(request):
    return Response(serializer.data)

@api_view(['POST'])
def doc_delete(request):
    return Response(serializer.data)

@api_view(['POST'])
def doc_commit(request):
    return Response(serializer.data)
