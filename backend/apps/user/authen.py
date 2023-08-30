'''try:
            user = User.objects.get(phonenum=phonenum)  # 输入phonenum查询到用户
            if user.check_password(password):  # 校验密码
                return user
        except Exception as e:
            return None'''
import redis
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .redis_pool import POOL
import redis
from .models import User
from django_redis import get_redis_connection
import redis
import uuid


class tokenAuth(BaseAuthentication):
    def tokenauthenticate(request):
        # 从请求头中获取前端带过来的token
        token = request.META.get('HTTP_TOKEN', '')
        #print(token)
        if not token:
            #raise AuthenticationFailed('没有携带token')
            return None
        # 去redis进行比较
        conn = redis.Redis(host='localhost',port=6379,db=0,password=None)
        uid = conn.get(str(token))
        if not uid:
            #raise AuthenticationFailed('token已过期')
            return None
        else:
            print(type(uid))
            uid1=int(uid)
            user_obj = User.objects.filter(uid=uid1)[0]
            return user_obj


