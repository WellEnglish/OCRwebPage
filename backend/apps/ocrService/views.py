from django.http import JsonResponse
import os
import imagehash
from PIL import Image
import json
from ..utils.paddleOCR_API import print_res
import redis
import re
from urllib import parse
from ..history.models import ocrHistory,regexHistory
from ..user.authen import tokenAuth

# Create your views here.

def uploadImge(request):
    # 由前端指定的name获取到图片数据
        print("ASSSS")
        img = request.FILES.get('file')
        path = './static/uploads'
        files = os.listdir(path)
        #获取服务器已经存储的图片数量
        i = len(files)
        # 从配置文件中载入图片保存路径
        img_path = f'./static/uploads/{i+1}.png'
        # 写入文件
        with open(img_path, 'ab') as fp:
            # 如果上传的图片非常大，就通过chunks()方法分割成多个片段来上传
            for chunk in img.chunks():
                fp.write(chunk)
        #print('img_path',img_path)
        #img_path=img_path[9:]
        return img_path

def ocrBase(img_path):
    #将收到的图片转换为hash值
        highfreq_factor = 1
        hash_size = 8
        img_hash = imagehash.phash(Image.open(img_path),hash_size=hash_size,highfreq_factor=highfreq_factor)
        
        print('hash',img_hash)
        #在redis中寻找有无对应hash值
        #try:
        #conn = redis.Redis(connection_pool=POOL)
        conn = redis.Redis(host='localhost',port=6379,db=1,password=None)
        print('conn',conn)
        pastRes=conn.get(str(img_hash))
        print('pastRes',pastRes)
        PastSCore=conn.get(str('socre'+str(img_hash)))
        PastPath=conn.get(str('resPath'+str(img_hash)))
        print('PastScore',PastSCore)
        print('pastPath',PastPath)
        #如果不存在一样的hash值
        if  b'None' in [pastRes,PastPath,PastSCore] or None in [pastRes,PastPath,PastSCore]:
            print('1 直接ocr')
            print('imgpath',img_path)
            ocrRes,scores,resPath=print_res(img_path)
            s=0
            for i in scores:
                s=s+float(i)
            score=s/len(scores)
            #print('1 ocrres',ocrRes)
            #print('1 scores',scores)
            if ocrRes:
                conn.set(str(img_hash),str(ocrRes))
                #scoreKey=str('socre'+str(img_hash))
                conn.set(str('socre'+str(img_hash)),str(score))
                #resPathKey=str('resPath'+str(img_hash))
                conn.set(str('resPath'+str(img_hash)),str(resPath))
                #print(ocrRes)
            #存在一样的hash值
        else:
            print('2 redis中找到了！')
            strPastRes=str(pastRes, encoding = "utf-8")
            strPastScore=str(PastSCore, encoding = "utf-8")
            strPastPath=str(PastPath, encoding = "utf-8")
            ocrRes=strPastRes
            score=strPastScore
            resPath=strPastPath
        print('ocrRes',ocrRes)
        return ocrRes,score,resPath
        #except:
         #   return None

def ocr(request):
    if request.method == "POST":
        img_path=uploadImge(request)#'./static/uploads/{i+1}.png'
        print('path',img_path)
        userImg_path=img_path[9:]#uploads/53.png
        print(img_path)
        imgRes,score,resPath=ocrBase(img_path)
        print('typeOfImgRes',type(imgRes))
        print(imgRes)


        if not imgRes:
            data={
                'img_path':userImg_path,
                'msg':'ocr识别失败'
            }
        else:
            usernow=tokenAuth.tokenauthenticate(request)
            if usernow:
                uid=usernow.uid
                ocrhistory=ocrHistory.objects.create(uid=uid,picLocation=img_path,ocr_Result=imgRes,score=score,resPath=resPath)
                ocrhistory.save()
                print('###成功save到数据库#####')
                data={
                'img_path':userImg_path,
                'ocrRes':imgRes,
                'score':score,
                'resPath':resPath
            }
            else:
                 data={
                      'img_path':userImg_path,
                      'ocrRes':imgRes,
                      'score':score,
                      'resPath':resPath,
                      'msg':'识别成功，但请先登录，否则无法记录使用情况'
                 }
        return JsonResponse(data)
    
     

def regex(request):
    if request.method=='POST':
            usernow=tokenAuth.tokenauthenticate(request)
            #print('request.POST',request.POST)
            #print('########################################')

            img_path=uploadImge(request)
            userImg_path=img_path[9:]#uploads/53.png
            txt_string,score,resPath=ocrBase(img_path)

            #print('requestBody',request.body)
            #data = json.loads(request.body)
            #regex = data.get('regex', '')
            '''regex = request.POST.get('regex')
            print(type(regex))
            print(regex)'''
            regex = request.POST.get('regex')
            #print(regex)
            #print(type(regex))
            #print("##########33######")

            s=''
            for i in txt_string:
                 s=s+str(i)
            #print('#####REGEX###')
            #print('s',s)
            #print('regex',regex)
            # regex="r'"+regex+"'"
            # print('regex',regex)
            regex1 = re.compile(regex)
            #print(regex1)
            #search() 方法查找匹配项时，它只会在给定的字符串中寻找 第一个符合条件的匹配项。
            # 如果需要查找所有的匹配项，则可以使用 findall() 方法。
            regexRes = regex1.findall(s)  #使用正则表达式匹配,结果是一个列表
            #print('regexRes',regexRes)
            #print('###########')
            if regexRes != []:
                is_Regex=True
            else:
                is_Regex=False
            if usernow:
                uid=usernow.uid
                regexhistory=regexHistory.objects.create(uid=uid,picLocation=img_path,is_Regex=is_Regex,regexResult=regexRes,score=score,resPath=resPath)
                regexhistory.save()
                print('###成功save到数据库')
                data={
                        'img_path':userImg_path,
                        'is_Regex':is_Regex,
                        'regexRes':regexRes,
                        'score':score,
                        'resPath':resPath
                    }
            else:
                 data={'img_path':userImg_path,
                        'is_Regex':is_Regex,
                        'regexRes':regexRes,
                        'score':score,
                        'resPath':resPath,
                        'msg':'识别成功，但请先登录，否则无法记录使用情况'}
            return JsonResponse(data)
            

        