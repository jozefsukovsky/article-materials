from typing import Optional
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailBackend(ModelBackend):

    def authenticate(self, request, username: Optional[str] = None, password: Optional[str] = None, **kwargs):
        if not username or not password:
            return None
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
