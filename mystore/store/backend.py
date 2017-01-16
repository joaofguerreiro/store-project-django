from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User


class EmailBackend(object):

    def authenticate(self, email=None, password=None):
        try:
            user = User.objects.get(email=email)
            pwd_valid = check_password(password, user.password)
            if user.is_active and pwd_valid:
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

