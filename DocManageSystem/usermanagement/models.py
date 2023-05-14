from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator


class CustomUserManager(BaseUserManager):
    """
    create user
    """

    def create_user(self, username, department, password=None):
        if not department:
            raise ValueError('The Department field must be set')
        if not username:
            raise ValueError('The Username field must be set')

        user = self.model(
            username=self.normalize_username(username),
            department=department
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def normalize_username(self, username):
        """
        Disable username normalization, so that usernames are not forced to be unique
        """
        return username


class User(AbstractUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    username_validator = UnicodeUsernameValidator

    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[username_validator]
    )
    department = models.CharField(max_length=150)
    date_joined = models.DateTimeField(auto_now_add=True)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['department']
    objects = CustomUserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        db_table = 'custom_user'

    def __str__(self):
        return self.username
