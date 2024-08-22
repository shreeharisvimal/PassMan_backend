from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin

# Create your models here.

class Manager(BaseUserManager):

    def checkMailOrPhone(self, data):
     return True if '@gmail.com' in data else False	

    def create_user(self, credential, **extra_fields):
        if self.checkMailOrPhone(credential):
            credential = self.normalize_email(credential)
            extra_fields.setdefault('is_email', True)
        user = self.model(credential=credential, **extra_fields)
        user.save(using=self._db)
        return user

    def create_superuser(self, credential, password,  **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if password is None:
            raise ValueError('Superuser must have a password')
        return self.create_user(credential, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    credential = models.CharField(max_length=120, unique=True, null=False, blank=True)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_email = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)

    objects = Manager()

    USERNAME_FIELD = 'credential'

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        refresh['user_cred'] = str(self.credential)
        refresh['user_id'] = str(self.id)
        refresh['isAdmin'] = str(self.is_superuser)

        return {
            'RefreshToken': str(refresh),
            'AccessToken': str(refresh.access_token)
        }

    def __str__(self):
        return str(self.credential)
    