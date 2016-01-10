from django.core.validators import validate_email

from users.models import User


class BasicBackend:

    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None


class EmailBackend(BasicBackend):

    def authenticate(self, username=None, password=None):
        try:
            validate_email(username)
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                return None
        except:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return None
        if user.check_password(password):
            return user