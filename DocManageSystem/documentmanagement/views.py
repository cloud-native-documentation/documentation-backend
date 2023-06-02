from rest_framework import generics, viewsets, permissions, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Doc, Dir, Project
from .serializers import DirSerializer
import os
root_dir = './store/files'
os.system(f'mkdir -p {root_dir}')

@api_view(['POST'])
def project_create(request):
    projectname=request.data['project']
    project = Project.objects.filter(projectname=projectname)
    
    if len(project) != 0:
        data = {"status": "fail, already exist"}
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    
    projectpath = f'{root_dir}/{projectname}'
    os.popen(f'mkdir {projectpath}')
    
    user = request.META.get('user')
    instance = Project(
            projectname=projectname, 
            department=user.department,
            owner=user.username
        )
    instance.save()
    
    data = {"status": "success"}
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def project_delete(request):
    projectname=request.data['project']
    project = Project.objects.filter(projectname=projectname)
    
    if len(project) == 0:
        data = {"status": "fail, no such project"}
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
       
    project=project[0] 
    user = request.META.get('user')
    if project.owner != user.username:
        data = {"status": "fail, you are not owner"}
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        
    project.delete()
    
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
    pass

@api_view(['POST'])
def dir_delete(request):
    pass

class DirectoryViewSet(mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    queryset = Dir.objects.filter()
    serializer_class = DirSerializer
    permission_classes = (IsAuthenticated, )
    def perform_destroy(self, instance):
        if instance.owner != self.request.user:
            raise PermissionDenied
        super().perform_destroy(instance)

@api_view(['GET'])
def doc_list(request):
    projectname=request.data['project']
    dirname=request.data['directory']
    
    docs_list = []
    if dirname == '/':
        dirs = Dir.objects.filter(project=projectname)
        docs_list = [directory.dirname for directory in dirs]
    
    docs = Doc.objects.filter(project=projectname, directory=dirname)
    for doc in docs:
        docs_list.append(doc.file)

    data = {"status": "success", "documentlist": docs_list}
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
def doc_view(request):
    filename=request.data['file']
    directory=request.data['directory']
    projectname=request.data['project']
    
    doc = Doc.objects.filter(
        project=projectname, directory=directory, file=filename)
    
    if len(doc) == 0:
        data = {"status": "fail, no such file"}
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    
    filepath = (f'{root_dir}/{projectname}/{directory}/{filename}')
    file = open(filepath, "r")
    content = file.read()
    file.close()
    
    data = {"status": "success", "content": content}
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def doc_create(request):
    filename=request.data['file']
    directory=request.data['directory']
    projectname=request.data['project']
    public=request.data['public']
    private=request.data['private']
    
    doc = Doc.objects.filter(
        project=projectname, directory=directory, file=filename)
    if len(doc) != 0:
        data = {"status": "fail, file exist"}
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    
    project = Project.objects.filter(projectname=projectname)
    if len(project) == 0:
        data = {"status": "fail, no such project"}
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    
    dir = Dir.objects.filter(project=projectname, dirname=directory)
    if len(dir) == 0:
        data = {"status": "fail, no such directory"}
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    
    projectpath = f'{root_dir}/{projectname}'
    directorypath = f'{projectpath}/{directory}'
    filepath = f'{directorypath}/{filename}'
    print(filepath)
    
    os.popen(f'mkdir {projectpath}')
    os.popen(f'mkdir {directorypath}')
    os.popen(f'touch "{filepath}"')
    
    user = request.META.get('user')
    instance = Doc(
            file=filename, 
            directory=directory, 
            project=projectname,
            owner=user.username, 
            public=public,
            private=private
        )
    instance.save()
    
    data = {"status": "success"}
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def doc_delete(request):
    filename=request.data['file']
    directory=request.data['directory']
    projectname=request.data['project']
    doc = Doc.objects.filter(
        project=projectname, directory=directory, file=filename)
    
    if len(doc) == 0:
        data = {"status": "fail, no such file"}
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        
    doc = doc[0]
    user = request.META.get('user')
    
    if doc.owner != user.username:
        data = {"status": "fail, you are not owner"}
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        
    doc.delete()
    
    data = {"status": "success"}
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def doc_commit(request):
    filename=request.data['file']
    directory=request.data['directory']
    projectname=request.data['project']
    doc = Doc.objects.filter(
        project=projectname, directory=directory, file=filename)
    
    if len(doc) == 0:
        data = {"status": "fail, no such file"}
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        
    doc = doc[0]
    user = request.META.get('user')
    project = Project.objects.filter(projectname=projectname)
    project = project[0]
    if doc.private == '1' or (doc.public == '0' and project.department != user.department):
        data = {"status": "fail, permission denied"}
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

    content = request.data['content']
    
    filepath = (f'{root_dir}/{projectname}/{directory}/{filename}')
    file = open(filepath, "w")
    file.write(content)
    file.close()
    
    data = {"status": "success"}
    return Response(data, status=status.HTTP_200_OK)
