from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import RegisterView, UserView

urlpatterns = [
    path('token', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('register', RegisterView.as_view(), name='auth_register'),
    path('', UserView.as_view(), name='auth_user'),
]