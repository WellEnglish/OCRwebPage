from django.db import models
import uuid
# Create your models here.

from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager

class UserManager(BaseUserManager):
    def _create_user(self,username,password,phonenum,**kwargs):
        if not username:
            raise ValueError("请传入用户名！")
        if not password:
            raise ValueError("请传入密码！")
        if not phonenum:
            raise ValueError("请传入电话号码！")
        user = self.model(username=username,phonenum=phonenum,**kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self,username,password,phonenum,**kwargs):
        kwargs['is_superuser'] = False
        return self._create_user(username,password,phonenum,**kwargs)

    def create_superuser(self,username,password,phonenum,**kwargs):
        kwargs['is_superuser'] = True
        kwargs['is_staff'] = True
        return self._create_user(username,password,phonenum,**kwargs)

class User(AbstractBaseUser,PermissionsMixin): # 继承AbstractBaseUser，PermissionsMixin
    uid = models.AutoField(primary_key=True,verbose_name='用户id')
    username = models.CharField(max_length=15,verbose_name="用户名")
    phonenum =models.CharField(max_length=11,null=True,blank=True,verbose_name="手机号码",unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'uid'
    REQUIRED_FIELDS = ['phonenum']
    PHONENUM_FIELD = 'phonenum'

    objects = UserManager()

    def get_username(self):
        return self.username

    def get_userphone(self):
        return self.phonenum

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name
