from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from .models import User
import json
import redis
import uuid
#from django_redis import get_redis_connection
#from .redis_pool import POOL
#from .authen import LoginAuth
from .authen import tokenAuth
import random
from django.core.cache import cache
from django.contrib.auth import authenticate
from django.contrib.auth.backends import ModelBackend
from rest_framework.authentication import BasicAuthentication,SessionAuthentication,TokenAuthentication
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed

# Create your views here.

#注册用户功能
def register(request):
    if request.method=='POST':
            data = json.loads(request.body)
            #print(data)
            phone_num = data.get('phonenum', '')
            user_name=data.get('username','')
            pass_word=data.get('passwd','')
            #check电话号码有没有重复
            user = User.objects.filter(phonenum=phone_num)
            if len(user)==1:
                data={
                        'message':'该电话号码已注册'
                    }
                return JsonResponse(data)
            else:
                user=User.objects.create_user(username=user_name,password=pass_word,phonenum=phone_num)
                user.save()
                data={
                    'message':'已成功创建用户'
                }
                return JsonResponse(data)
                
    
    else:
        return HttpResponse("hello")



#登录功能

'''class Login(APIView):
    authentication_classes = (BasicAuthentication,TokenAuthentication)   # 使用基础的和token的验证方式
    permission_classes = (AllowAny,)    # 允许所有人访问'''
def login_view(request):
        if request.method=='POST':
            data = json.loads(request.body)
            phone_num = data.get('phonenum', '')
            pass_word = data.get('password', '')

            if User.objects.filter(phonenum=phone_num):
                #如果用户存在
            # 与数据库中的用户名和密码比对，django默认保存密码是以哈希形式存储，并不是明文密码，这里的password验证默认调用的是User类的check_password方法，以哈希值比较。
                user = authenticate(request, phone=phone_num, password=pass_word)
            # 验证如果用户不为空
                if user:
                    #login方法登录
                        #auth.login(request, user)
                        try:
                             #conn = redis.Redis(connection_pool=POOL)
                             conn = redis.Redis(host='localhost',port=6379,db=0,password=None)
                             token=uuid.uuid4()
                             #print(token)
                             try:
                                conn.set(str(token), str(user.uid),ex=6000)
                                #print(user.uid)
                             except redis.RedisError as e:
                                print("设置",str(e))
                             data={
                                    'msg':'登录成功',
                                    'token':str(token)
                                }
                        except:
                             data={
                                  'msg':'创建令牌失败',
                             }
                        return JsonResponse(data)
                        
                #密码和手机号码不匹配
                else:
                    data={
                            "status": status.HTTP_403_FORBIDDEN,
                            "msg": "用户名或密码错误",
                        }
                return JsonResponse(data)
                
            #用户不存在
            else:
                data={
                    'message':'该用户不存在，手机号码未注册'
                }
                return JsonResponse(data)
        

def getuserInfo(request):
    usernow=tokenAuth.tokenauthenticate(request)
    if usernow:
         username=usernow.username
         uid=usernow.uid
         data={
              'msg':'成功得到用户信息',
              'uid':uid,
              'username':username,
         }
    else:
         data={
              'msg':'用户未登录',
         }
    return JsonResponse(data)

def loginOut(request):
    usernow=tokenAuth.tokenauthenticate(request)
    if usernow:
        try:
            conn = redis.Redis(host='localhost',port=6379,db=0,password=None)
            token = request.META.get('HTTP_TOKEN', '')
            conn.delete(str(token))
            data={
                 'msg':'退出成功'
            }
        except:
             data={
                  'msg':'token删除失败，未能成功退出'
             }       
        return JsonResponse(data)
    else:
         data={
              'msg':'用户token已失效'
         }
         return JsonResponse(data)