from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Doc, Dir
from .serializers import DocSerializer, DirSerializer


@api_view(['POST'])
def project_create(request):
    projects = Project.objects.all()
    serializer = 
    return Response(serializer.data)


@api_view(['POST'])
def project_delete(request):
    projects = Project.objects.all()
    serializer = 
    return Response(serializer.data)


@api_view(['GET'])
def project_list(request):
    projects = Project.objects.all()
    serializer = 
    return Response(serializer.data)


# @api_view(['GET'])
# def project_permission_list(request):
#     return Response(serializer.data)


@api_view(['POST'])
def dir_create(request):
    dirs = Dir.objects.all()
    serializer = 
    return Response(serializer.data)


@api_view(['POST'])
def dir_delete(request):
    dirs = Dir.objects.all()
    serializer = 
    return Response(serializer.data)


@api_view(['GET'])
def doc_list(request):
    docs = Doc.objects.all()
    serializer = 
    # document list, status
    return Response(serializer.data)


@api_view(['GET'])
def doc_view(request):
    docs = Doc.objects.all()
    serializer = 
    # content, status code
    return Response(serializer.data)


@api_view(['POST'])
def doc_create(request):
    docs = Doc.objects.all()
    serializer = 
    return Response(serializer.data)


@api_view(['POST'])
def doc_delete(request):
    docs = Doc.objects.all()
    serializer = 
    return Response(serializer.data)


@api_view(['POST'])
def doc_commit(request):
    docs = Doc.objects.all()
    serializer = 
    return Response(serializer.data)
