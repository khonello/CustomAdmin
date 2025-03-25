from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.backends import BaseBackend
from django.http.request import HttpRequest
from app.models import CustomUser

class CustomBackend(BaseBackend):

    def authenticate(self, request: HttpRequest, username, password, **kwargs):

        try:
            obj = CustomUser.objects.get(username= username)
            if obj.check_password(password):
                return obj
            else:
                return None
            
        except CustomUser.DoesNotExist:
            return None