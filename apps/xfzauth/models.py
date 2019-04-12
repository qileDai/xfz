#encoding:utf-8

from django.contrib.auth.models import AbstractBaseUser,\
    PermissionsMixin,BaseUserManager
from shortuuidfield import ShortUUIDField
from django.db import models

class UserManager(BaseUserManager):
    def _create_user(self,telephone,username,password,**kwargs):
        if not telephone:
            raise ValueError("请输入手机号码")
        if not username:
            raise ValueError("请输入用户名")
        if not password:
            raise ValueError("请输入密码")
        user = self.model(telephone=telephone,username=username,**kwargs)
        user.set_password(password)
        user.save()
        return user
    def create_user(self,telephone,username,password,**kwargs):
        kwargs['is_superuser'] = False
        return self._create_user(telephone,username,password,**kwargs)

    def create_superuser(self,telephone,username,password,**kwargs):
        kwargs['is_superuser'] = True
        kwargs['is_staff'] = True
        return self._create_user(telephone,username,password,**kwargs)

class User(AbstractBaseUser,PermissionsMixin):
    uid = ShortUUIDField(primary_key=True)
    telephone = models.CharField(max_length=11,unique=True)
    email = models.EmailField(unique=True,null=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    data_joined = models.DateTimeField(auto_now_add=True)

    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'telephone'
    EMAIL_FIELD = 'email'
    objects = UserManager()

    def get_fullname(self):
        return self.username
    def get_shortname(self):
        return self.username


