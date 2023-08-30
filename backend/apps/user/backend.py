from .models import User
from django.contrib.auth.backends import ModelBackend
 
class CustomBackend(ModelBackend):
 
    def authenticate(self,
                     request,username=None,
                     phone=None,
                     password=None,
                     **kwargs):
        # 支持后台登录功能，因为admin登录提交的时候会发送username字段
        try:
                user = User.objects.get(phonenum=phone)
                if user.check_password(password):
                    return user
        except User.DoesNotExist:
            return None
        return None
 
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None