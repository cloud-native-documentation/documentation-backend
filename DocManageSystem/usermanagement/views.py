from django.db import models
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from .serializers import CustomUserSerializer, LoginSerializer
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken




@api_view(['POST'])
def user_login(request):
    """
    user login
    @param request:
    @return:
    """
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data
    refresh = RefreshToken.for_user(data['user'])
    return Response({
        'status': 'success',
        # 'refresh': str(refresh),
        'token': 'jwt ' + str(refresh.access_token),
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
def user_register(request):
    """
    user register
    @param request:
    @return:
    """
    User = get_user_model()
    serializer = CustomUserSerializer(data=request.data)
    if serializer.is_valid():
        password = make_password(serializer.validated_data['password'])

        User.objects.create(
            username=serializer.validated_data['username'],
            department=serializer.validated_data['department'],
            password=password
        )
        user = User.objects.get(username=serializer.validated_data['username'])
        data = {"status": "success", 'id': user.id}
        return Response(data=data, status=status.HTTP_201_CREATED)
    data = {"status": "fail"}
    return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def user_logout(request):
    data = {"status": "success"}
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
def user_list(request):
    """
    list user information
    """
    users = User.objects.all()
    serializer = CustomUserSerializer(users, many=True)

    users_list = []
    for user in serializer.data:
        info = {"username": user["username"], "department": user["department"]}
        users_list.append(info)
        data = {"status": "success", "userlist": users_list}
    return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'])
def user_me(request):
    """
    user me
    @param request:
    @return:
    """
    user = request.META.get('user')
    serializer = CustomUserSerializer(user)
    data = {"status": "success", "user": serializer.data}
    return Response(data, status=status.HTTP_200_OK)
