from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Doc, Dir, Project
import os
root_dir = './files/'
os.system(f'mkdir {root_dir}')

@api_view(['POST'])
def project_create(request):
    projectname=request.data['projectname']
    project = Project.objects.filter(projectname=projectname)
    
    if project is not []:
        data = {"status": "fail"}
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    
    department = request.META.get('user').department
    instance = Project(projectname=projectname, department=department)
    instance.save()
    
    data = {"status": "success"}
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def project_delete(request):
    projectname=request.data['projectname']
    projects = Project.objects.filter(projectname=projectname)
    
    if projects == []:
        data = {"status": "fail"}
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        
    projects[0].delete()
    
    data = {"status": "success"}
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
def project_list(request):
    projects = Project.objects.all()
    project_list = [project.projectname for project in projects]
    data = {"status": "success", "projectlist": project_list}
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def dir_create(request):
    """get user name"""
    projectpath = f'{root_dir}{request.data["project"]}'
    dirpath = f'{projectpath}/{request.data["directoryname"]}'
    str = os.popen(f'mkdir {projectpath}')
    os.popen(f'mkdir {dirpath}')
    return Response({"status": "fail"}, status=status.HTTP_200_OK)


@api_view(['POST'])
def dir_delete(request):
    
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
