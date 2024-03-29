from django.contrib.auth.backends import BaseBackend
from .models import OASuser

class OASuserBackend(BaseBackend):
    def authenticate(self, request, username=None, userPass=None):
        try:
            user = OASuser.objects.get(username=username)
            if user.check_password(userPass):
                return user
            else:
                return None
        except OASuser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return OASuser.objects.get(pk=user_id)
        except OASuser.DoesNotExist:
            return None
