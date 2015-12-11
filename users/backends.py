from users.models import User
from django.core.validators import validate_email

class BasicBackend:

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

class EmailBackend(BasicBackend):

    def authenticate(self, username=None, is_teacher=None, password=None):
        try:         
            validate_email(username)
            try:
                print(is_teacher)
                user = User.objects.get(email=username, is_teacher=is_teacher)
            except User.DoesNotExist:
                return None
        except:
            try:
                print(is_teacher)
                user = User.objects.get(username=username, is_teacher=is_teacher)
            except User.DoesNotExist:
                return None
        if user.check_password(password):
            return user