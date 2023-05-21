from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Doc, Dir, Project
import os
root_dir = './files'
os.system(f'mkdir {root_dir}')

@api_view(['POST'])
def project_create(request):
    projectname=request.data['projectname']
    project = Project.objects.filter(projectname=projectname)
    
    if project is not []:
        data = {"status": "fail"}
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
    projectname=request.data['projectname']
    project = Project.objects.filter(projectname=projectname)
    
    if project == []:
        data = {"status": "fail"}
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
       
    project=project[0] 
    user = request.META.get('user')
    if project.owner != user.owner:
        data = {"status": "fail"}
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
    projectname = request.data['project']
    dirname = request.data['directoryname']
    
    dir = Dir.objects.filter(project=projectname, dirname=dirname)
    if dir is not []:
        data = {"status": "fail"}
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    
    projectpath = f'{root_dir}/{projectname}'
    dirpath = f'{projectpath}/{dirname}'
    
    os.popen(f'mkdir {projectpath}')
    os.popen(f'mkdir {dirpath}')
    
    user = request.META.get('user')
    instance = Dir(
            dirname=dirname,
            project=projectname,
            owner=user.username
        )
    instance.save()
    
    data = {"status": "success"}
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def dir_delete(request):
    projectname = request.data['project']
    dirname = request.data['directoryname']
    
    dir = Dir.objects.filter(project=projectname, dirname=dirname)
    if dir == []:
        data = {"status": "fail"}
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    
    dir = dir[0]
    
    user = request.META.get('user')
    if dir.owner != user.owner:
        data = {"status": "fail"}
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    
    dir.delete()
    
    data = {"status": "success"}
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
def doc_list(request):
    projectname=request.data['project']
    dirname=request.data['directory']
    
    docs_list = []
    if dirname == '/':
        """may have directories"""
        dirs = Dir.objects.filter(project=projectname)
        docs_list = [directory.dirname for directory in dirs]
    
    docs = Doc.objects.filter(project=projectname)
    for doc in docs:
        if '/' not in doc.docpath:
            docs_list.append(doc.docpath)

    data = {"status": "success", "documentlist": docs_list}
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
def doc_view(request):
    filepath=request.data['filepath']
    projectname=request.data['project']
    doc = Doc.objects.filter(project=projectname, docpath=filepath)
    
    filepath = (f'{root_dir}/{projectname}/{filepath}')
    file = open(filepath, "r")
    content = file.read()
    file.close()
    
    data = {"status": "success", "content": content}
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def doc_create(request):
    filepath=request.data['filepath']
    projectname=request.data['project']
    public=request.data['public']
    private=request.data['private']
    
    doc = Doc.objects.filter(project=projectname, docpath=filepath)
    if doc is not []:
        data = {"status": "fail"}
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    
    user = request.META.get('user')
    instance = Doc(
            docpath=filepath, 
            project=projectname,
            owner=user.username, 
            public=public,
            private=private,
            content=""
        )
    instance.save()
    
    data = {"status": "success"}
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def doc_delete(request):
    filepath=request.data['filepath']
    projectname=request.data['project']
    doc = Doc.objects.filter(project=projectname, docpath=filepath)
    
    if doc == []:
        data = {"status": "fail"}
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        
    doc = doc[0]
    user = request.META.get('user')
    
    if doc.owner != user.username:
        data = {"status": "fail"}
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        
    doc.delete()
    
    data = {"status": "success"}
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def doc_commit(request):
    filepath=request.data['filepath']
    projectname=request.data['project']
    doc = Doc.objects.filter(project=projectname, docpath=filepath)
    
    if doc == []:
        data = {"status": "fail"}
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        
    doc = doc[0]
    user = request.META.get('user')
    project = Project.objects.filter(projectname=projectname)
    project = project[0]
    if doc.private == True or (doc.public == False and project.department != user.department):
        """cannot edit, permission error"""
        data = {"status": "fail"}
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

    content = request.data['content']
    
    filepath = (f'{root_dir}/{projectname}/{filepath}')
    file = open(filepath, "w")
    file.write(content)
    file.close()
    
    data = {"status": "success"}
    return Response(data, status=status.HTTP_200_OK)
