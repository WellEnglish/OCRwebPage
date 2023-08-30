from django.urls import path

from . import views

app_name = 'ocrService'
urlpatterns = [
    path('ocr', views.ocr, name='ocr'),
    path('regex',views.regex,name='regex'),
]