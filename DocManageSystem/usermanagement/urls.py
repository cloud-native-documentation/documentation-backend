from django.urls import path
from .views import user_register, user_list, user_login, user_logout, user_me
urlpatterns = [
 path('me', user_me),
 path('login', user_login),
 path('register', user_register),
 path('logout', user_logout),
 path('list', user_list)
]