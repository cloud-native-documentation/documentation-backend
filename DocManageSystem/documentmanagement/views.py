from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Doc, Dir, Project
from .serializers import DocSerializer, DirSerializer, ProjectSerializer


@api_view(['POST'])
def project_create(request):
    projects = Project.objects.all()
    return Response()


@api_view(['POST'])
def project_delete(request):
    projects = Project.objects.all()
    return Response()


@api_view(['GET'])
def project_list(request):
    projects = Project.objects.all()
    return Response()


# @api_view(['GET'])
# def project_permission_list(request):
#     return Response()


@api_view(['POST'])
def dir_create(request):
    dirs = Dir.objects.all()
    return Response()


@api_view(['POST'])
def dir_delete(request):
    dirs = Dir.objects.all()
    return Response()


@api_view(['GET'])
def doc_list(request):
    docs = Doc.objects.all()

    # document list, status
    docs_list = []
    
    data = {"status": "success", "document_list": docs_list}
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
def doc_view(request):
    docs = Doc.objects.all()
    # content, status code
    return Response()


@api_view(['POST'])
def doc_create(request):
    docs = Doc.objects.all()
    return Response()


@api_view(['POST'])
def doc_delete(request):
    docs = Doc.objects.all()
    return Response()


@api_view(['POST'])
def doc_commit(request):
    docs = Doc.objects.all()
    return Response()
