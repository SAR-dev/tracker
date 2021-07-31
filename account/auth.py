from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
User = get_user_model()

class EmailOrUsernameModelBackend(object):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = get_user_model()

        if username is None:
            username = kwargs.get(user_model.USERNAME_FIELD)
        users = user_model._default_manager.filter(
            Q(**{user_model.USERNAME_FIELD: username}) | Q(email__iexact=username)
        )
        for user in users:
            if user.check_password(password):
                return user
        if not users:
            user_model().set_password(password)
            
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
            
            
# ANOTHER APPROACH
# class EmailOrUsernameModelBackend(object):
#     def authenticate(self, username=None, password=None):
#         if '@' in username:
#             kwargs = {'email': username}
#         else:
#             kwargs = {'username': username}
#         try:
#             user = get_user_model().objects.get(**kwargs)
#             if user.check_password(password):
#                 return user
#         except User.DoesNotExist:
#             return None

#     def get_user(self, username):
#         try:
#             return get_user_model().objects.get(pk=username)
#         except get_user_model().DoesNotExist:
#             return None