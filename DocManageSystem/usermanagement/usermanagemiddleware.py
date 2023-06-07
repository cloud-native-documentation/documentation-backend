from django.http import JsonResponse
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
import datetime
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings

User = get_user_model()

exlude_path = ['/user/login', '/user/register', '/user/logout', '/user/refresh', 'admin']
def should_exclude(path):
    for p in exlude_path:
        if p in path:
            return True
    return False

class JWTMiddleware:
    """
    use request.META.get('user') to get user info
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if should_exclude(request.path):
            return self.get_response(request)

        authorization = request.META.get('HTTP_AUTHORIZATION')
        if not authorization:
            return JsonResponse({'error': 'Authorization header is missing'}, status=401)

        try:
            token = authorization.split(' ')[1]
            validated_token = JWTAuthentication().get_validated_token(token)
            user_id = validated_token['user_id']
            request.META['user'] = User.objects.get(id=user_id)
        except (InvalidToken, IndexError):
            return JsonResponse({'error': 'Invalid or expired token'}, status=401)

        return self.get_response(request)


class AddTokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if should_exclude(request.path):
            return self.get_response(request)

        response = self.get_response(request)
        user = request.META.get('user')
        if user.is_authenticated:
            token = RefreshToken.for_user(user)
            response['Authorization'] = f"jwt {str(token.access_token)}"

        return response
