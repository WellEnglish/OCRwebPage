from django.urls import path

from . import views

app_name = 'user'
urlpatterns = [
    path('login', views.login_view, name='login'),
    path('register',views.register,name='register'),
    path('getuserInfo',views.getuserInfo,name='getuserInfo'),
    path('loginOut',views.loginOut,name='loginOut')
]