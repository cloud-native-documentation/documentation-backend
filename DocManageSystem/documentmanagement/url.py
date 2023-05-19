from django.urls import path
from .views import doc_list
urlpatterns = [
 path('create_project', project_create), 
 path('delete_project', project_delete), 
 path('project_list', project_list), 
 path('permission_list', project_permission_list), 
 path('create_directory', dir_create), 
 path('delete_directory', dir_delete),
 path('list', doc_list), 
 path('view', doc_view), 
 path('create', doc_create), 
 path('delete', doc_delete), 
 path('commit', doc_commit)
]