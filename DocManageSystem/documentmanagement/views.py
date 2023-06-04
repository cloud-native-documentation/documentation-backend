from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Doc, Dir, Project, HistoryAction
from usermanagement.models import User
import os
root_dir = os.path.join(os.getcwd() + '/', './store/files')
try:
    os.makedirs(root_dir)
except OSError as e:
    pass

@api_view(['POST'])
def project_create(request):
    projectname=request.data['project']
    description=request.data.get('description')
    project = Project.objects.filter(projectname=projectname)
    if description == None:
        description = ""
    
    if len(project) != 0:
        data = {"status": "fail, already exist"}
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        os.makedirs(os.path.join(root_dir, projectname))
    except OSError as e:
        pass
    
    user = request.META.get('user')
    instance = Project(
            projectname=projectname, 
            department=user.department,
            owner=user.username,
            description=description
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
    
    project_list = []
    for project in projects:
        show = False
        if project.department == request.META.get('user').department:
            show = True
        else:
            docs = Doc.objects.filter(project=project.projectname)
            for doc in docs:
                if doc.public == '1':
                    show = True
        
        if show:
            project_list.append({'name': project.projectname, 'description': project.description})

    data = {"status": "success", "projectlist": project_list}
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def dir_create(request):
    projectname = request.data['project']
    dirname = request.data['directory']
    
    if dirname == '':
        data = {"status": "fail, directory cannot be empty"}
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    if dirname == '/':
        data = {"status": "fail, directory cannot be '/'"}
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    
    dir = Dir.objects.filter(project=projectname, dirname=dirname)
    if len(dir) != 0:
        data = {"status": "fail, already exist"}
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    
    projectpath = os.path.join(root_dir, projectname)
    dirpath = os.path.join(projectpath, dirname)
    
    try:
        os.makedirs(projectpath)
    except OSError as e:
        pass
    
    try:
        os.makedirs(dirpath)
    except OSError as e:
        pass

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
    dirname = request.data['directory']
    
    dir = Dir.objects.filter(project=projectname, dirname=dirname)
    if len(dir) == 0:
        data = {"status": "fail, no such directory"}
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    
    dir = dir[0]
    
    user = request.META.get('user')
    if dir.owner != user.username:
        data = {"status": "fail, you are not owner"}
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    
    dir.delete()
    
    data = {"status": "success"}
    return Response(data, status=status.HTTP_200_OK)

"""
type ProjectFileType = {
  name: string;
  isFile: boolean;
  children?: { name: string }[];
};

type ProjectFilesType = ProjectFileType[];

[{name: string, isFile: boolean, children: [{name: string}, {name: string}]}...]

"""

# @api_view(['GET'])
# def doc_list(request):
    
#     def setname(item, dirname):
#         item['name'] = dirname
#         return item
#     def setisFile(item, bo):
#         item['isFile'] = bo
#         return item
#     def addchildren(item, doc):
#         item['children'].append({'id': doc.id, 'name': doc.file})
#         return item
    
#     projectname=request.GET['project']
#     # dirname=request.GET['directory']
    
#     project = Project.objects.filter(projectname=projectname)
#     if len(project) == 0:
#         data = {"status": "fail, no such project"}
#         return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    
#     docs_list = []
#     dirs = Dir.objects.filter(project=projectname)
#     for directory in dirs:
#         item = {'children': []}
#         item = setname(item, directory.dirname)
#         item = setisFile(item, False)
        
#         docs = Doc.objects.filter(project=projectname, directory=directory.dirname)
#         for doc in docs:
#             item = addchildren(item, doc)
#         docs_list.append(item)

    
#     docs = Doc.objects.filter(project=projectname, directory='/')
#     for doc in docs:
#         item = {}
#         item = setname(item, doc.file)
#         item = setisFile(item, True)
#         docs_list.append(item)

#     data = {"status": "success", "documentlist": docs_list}
#     return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
def doc_list(request):
    projectname=request.GET['project']
    dirname=request.GET.get('directory')
    if dirname == None:
        dirname = '/'
    
    docs_list = []
    if dirname == '/':
        dirs = Dir.objects.filter(project=projectname)
        for dir in dirs:
            docs_list.append({'name': dir.dirname, 'isFile': False, 'id': 0})
    
    docs = Doc.objects.filter(project=projectname, directory=dirname)
    for doc in docs:
        owner = doc.owner
        department = User.objects.filter(username=owner)[0].department
        if owner == request.META.get('user').username or \
            (doc.private == '0' and department == request.META.get('user').department) or \
            doc.public == '1':
            docs_list.append({'name': doc.file, 'isFile': True, 'id': doc.id})
    
    data = {"status": "success", "documentlist": docs_list}
    return Response(data, status=status.HTTP_200_OK)
    

@api_view(['GET'])
def doc_view(request):
    id=request.GET['id']
    doc = Doc.objects.filter(id=id)
    
    if len(doc) == 0:
        data = {"status": "fail, no such file"}
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    
    doc=doc[0]
    filename=doc.file
    directory=doc.directory
    projectname=doc.project
    version=request.GET.get('version')
    
    if directory == None:
        directory = '/'
    if version == None:
        version = doc.cnt
    
    user = request.META.get('user')
    project = Project.objects.filter(projectname=projectname)
    project = project[0]
    if (doc.private == '1' and doc.owner != user.username) or \
        (doc.public == '0' and project.department != user.department):
        data = {"status": "fail, permission denied"}
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    
    filepath = (f'{root_dir}/{projectname}/{directory}/{filename}__{version}')
    file = open(filepath, "r")
    content = file.read()
    file.close()
    
    data = {"status": "success", "content": content}
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def doc_create(request):
    filename=request.data['file']
    projectname=request.data['project']
    public=request.data['public']
    private=request.data['private']
    directory=request.data.get('directory')
    if directory == None:
        directory = '/'
    
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
    if directory != '/' and len(dir) == 0:
        data = {"status": "fail, no such directory"}
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

    projectpath = os.path.join(root_dir, projectname)
    if directory != '/':
        dirpath = os.path.join(projectpath, directory)
    else:
        dirpath = projectpath
    filepath = os.path.join(dirpath, filename)
    print(filepath)
    
    try:
        os.makedirs(projectpath)
    except OSError as e:
        pass
    try:
        os.makedirs(dirpath)
    except OSError as e:
        pass
    with open(filepath + "__1", 'w') as _:
        pass
    
    user = request.META.get('user')
    instance = Doc(
            file=filename, 
            directory=directory, 
            project=projectname,
            owner=user.username, 
            public=public,
            private=private,
            cnt=1
        )
    instance.save()
    
    doc = Doc.objects.filter(
        project=projectname, directory=directory, file=filename)
    doc = doc[0]
    
    action_save(projectname, directory, filename, doc.id, user.username, 'create', 1)
    
    data = {"status": "success"}
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def doc_delete(request):
    id=request.data['id']
    doc = Doc.objects.filter(id=id)
    
    if len(doc) == 0:
        data = {"status": "fail, no such file"}
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    
    doc=doc[0]
    filename=doc.file
    directory=doc.directory
    projectname=doc.project
    
    if directory == None:
        directory = '/'
    
    user = request.META.get('user')
    
    if doc.owner != user.username:
        data = {"status": "fail, you are not owner"}
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        
    doc.cnt += 1
    doc.save()
    action_save(projectname, directory, filename, doc.id, user.username, 'delete', doc.cnt)
    
    doc.delete()
    
    data = {"status": "success"}
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def doc_commit(request):
    id=request.data['id']
    doc = Doc.objects.filter(id=id)
    
    if len(doc) == 0:
        data = {"status": "fail, no such file"}
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    
    doc=doc[0]
    filename=doc.file
    directory=doc.directory
    projectname=doc.project
    
    if directory == None:
        directory = '/'
    
    user = request.META.get('user')
    project = Project.objects.filter(projectname=projectname)
    project = project[0]
    if (doc.private == '1' and doc.owner != user.username) or \
        (doc.public == '0' and project.department != user.department):
        data = {"status": "fail, permission denied"}
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

    content = request.data['content']
    doc.cnt += 1
    doc.save()
    
    filepath = (f'{root_dir}/{projectname}/{directory}/{filename}__{doc.cnt}')
    file = open(filepath, "w")
    file.write(content)
    file.close()
    
    action_save(projectname, directory, filename, doc.id, user.username, 'commit', doc.cnt)
    
    data = {"status": "success"}
    return Response(data, status=status.HTTP_200_OK)


def action_save(project, directory, file, fileid, user, action, version):
    action = HistoryAction(
        project=project,
        directory=directory,
        file=file,
        fileid=fileid,
        username=user,
        action=action,
        version=version
    )
    action.save()
    
@api_view(['POST'])
def get_his_act(request):
    id = request.data.get('id')
    # if id != None:
    #     doc = Doc.objects.filter(id=id)
    #     if len(doc) == 0:
    #         data = {"status": "fail, no such file"}
    #         return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    
    if id == None:
        histories = HistoryAction.objects.all()
    else:
        histories = HistoryAction.objects.filter(fileid=id)
    
    action = []
    for his in histories:
        action.append(
            {"filename": his.file, "type":his.action, "time":his.modify_date, "user":his.username, "version": his.version}) 

    data = {"status": "success", "actions": action}
    return Response(data=data, status=status.HTTP_200_OK)