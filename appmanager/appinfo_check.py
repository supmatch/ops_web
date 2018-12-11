from django.shortcuts import HttpResponse
from appmanager.models import AppInfo
from appmanager import models
from appmanager.jenkins_operate import check_job

'''
检查用户名
'''


def check_app_name(request):
    app_name = request.GET['app_name']
    try:
        result = AppInfo.objects.get(App_name=app_name)
    except models.AppInfo.DoesNotExist:
        result = ''
    result2 = check_job(app_name)
    if result == '' and result2 == '':
        return HttpResponse('true')
    else:
        return HttpResponse('false')


'''
检查端口
'''


def check_app_port(request):
    app_port = request.GET['app_port']
    try:
        AppInfo.objects.get(App_port=app_port)
    except models.AppInfo.DoesNotExist:
        return HttpResponse('true')
    return HttpResponse('false')


