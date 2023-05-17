from django.urls import path
from .views import doc_list
urlpatterns = [
 path('list', doc_list), 
 path('view', doc_view), 
 path('create', doc_create), 
 path('delete', doc_delete), 
 path('commit', doc_commit)
]