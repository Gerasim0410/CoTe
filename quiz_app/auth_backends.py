# quiz_app/auth_backends.py
from django.contrib.auth.backends import BaseBackend
from .models import Profile


class UserIDBackend(BaseBackend):
    def authenticate(self, request, user_id=None):
        user = Profile.objects.get(user_id=user_id)
        return user

    def get_user(self, user_id):
        return Profile.objects.get(pk=user_id)
