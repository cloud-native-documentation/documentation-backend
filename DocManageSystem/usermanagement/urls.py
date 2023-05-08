from django.urls import path
from .views import user_list
urlpatterns = [
 path('create', user_list)
]