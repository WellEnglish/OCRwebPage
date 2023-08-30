from django.shortcuts import render
from .models import ocrHistory,regexHistory
from django.http import JsonResponse
from ..user.authen import tokenAuth
# Create your views here.
def showOcrHistory(request):
    if request.method=='GET':
        usernow=tokenAuth.tokenauthenticate(request)
        if usernow:
            uid=usernow.uid
            historylist=ocrHistory.objects.filter(uid=uid)
            data=[]
            for i in historylist:
                each={'time':i.time,'id':i.id,'picLocation':i.picLocation,'ocr_Result':i.ocr_Result,'score':i.score,'resPath':i.resPath}
                data.append(each)
        else:
            data={'msg':'用户token已过期，请重新登陆后查看历史记录'}
        print('data',data)
        return JsonResponse(data,safe=False)
        

def showRegexHistory(request):
    if request.method=='GET':
        usernow=tokenAuth.tokenauthenticate(request)
        if usernow:
            uid=usernow.uid
            historylist=regexHistory.objects.filter(uid=uid)
            data=[]
            for i in historylist:
                each={'time':i.time,'id':i.id,'picLocation':i.picLocation,'is_Regex':i.is_Regex,'regexResult':i.regexResult,'score':i.score,'resPath':i.resPath}
                data.append(each)
        else:
            data={'msg':'用户token已过期，请重新登陆后查看历史记录'}
        return JsonResponse(data,safe=False)