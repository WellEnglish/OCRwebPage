from django.db import models
import uuid
from django.contrib.postgres.fields import ArrayField
# Create your models here.
class ocrHistory(models.Model):
    time=models.DateTimeField(auto_now_add=True,verbose_name="记录时间")
    uid =models.IntegerField("verbose_name='用户id'")
    picLocation=models.CharField(max_length=70,verbose_name="图片存储的位置")
    ocr_Result=models.TextField(verbose_name="ocr识别出的文字结果")
    score=models.DecimalField(max_digits=17, decimal_places=16,verbose_name='准确度得分')
    resPath=models.CharField(max_length=70,verbose_name="结果图片存储的位置")

    
    class Meta():
        # 为这个类定义一个说明
        verbose_name = 'ocrhistory'
        # 不加这个的话在我们的verbose_name在admin里面会被自动加上s
        verbose_name_plural = verbose_name	

class regexHistory(models.Model):
    time=models.DateTimeField(auto_now_add=True,verbose_name="记录时间")
    uid =models.IntegerField("verbose_name='用户id'")
    picLocation=models.CharField(max_length=70,verbose_name="图片存储的位置")
    is_Regex=models.BooleanField(verbose_name="正则有无命中")
    regexResult=models.TextField(verbose_name="命中的结果文字")
    score=models.DecimalField(max_digits=17, decimal_places=16,verbose_name='准确度得分')
    resPath=models.CharField(max_length=100,verbose_name="结果图片存储的位置")

    class Meta():
        # 为这个类定义一个说明
        verbose_name = 'regexHistory'
        # 不加这个的话在我们的verbose_name在admin里面会被自动加上s
        verbose_name_plural = verbose_name	

#历史记录，一个星期清除一次
#from .history.models import ocrHistory,regexHistory
#ocrhistory=ocrHistory.objects.create(uid=usernow.uid,picLocation=path,ocr_Result=res)
#ocrhistory.save()
#conn = redis.Redis(host='localhost',port=6379,db=0,password=None，db=1)
#conn.set(md5,res)

