from django.contrib.auth.backends import BaseBackend
from .models import User as CustomUser  

class CustomAuthenticationBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = CustomUser.objects.get(username=username)
            
            if user.check_password(password):
                return user  
        except CustomUser.DoesNotExist:
            pass 

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None
