from django.urls import path

from . import views

app_name = 'history'
urlpatterns = [
    path('showOcrHistory', views.showOcrHistory, name='ocrHistory'),
    path('showRegxHistory', views.showRegexHistory, name='regexHistory'),
]