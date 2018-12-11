# -*-coding:utf-8 -*-
from django.shortcuts import render, redirect, render_to_response
from appmanager.models import AppInfo, CheckInfo
from appmanager import models
from appmanager.jenkins_operate import make_config_file, create_new_job
from appmanager.ansible_operate import make_host_file
from appmanager.gitlab_operate import create_project_hook
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
import logging
# Create your views here.


logger = logging.getLogger('django')


'''
展示app信息
'''


def show_app_info(request):
    apps = AppInfo.objects.all()
    return render(request, 'appmanager/index.html', {'apps': apps})


def add_app_form(request):
    return render(request, 'appmanager/addapp_form.html')


def add_fe_form(request):
    return render(request, 'appmanager/addfe_form.html')


#提交申请，等待审批
def save_apply(request):
    if request.method == 'POST':
        apply_user = request.user.username
        git_url = request.POST['git_url']
        app_name = request.POST['app_name']
        app_port = request.POST['app_port']
        app_ip_test = request.POST['app_ip_test']
        app_ip_dev = request.POST['app_ip_dev']
        app_ip_demo = request.POST['app_ip_demo']
        build_cmd_test = request.POST['build_cmd_test']
        build_cmd_dev = request.POST['build_cmd_dev']
        build_cmd_demo = request.POST['build_cmd_demo']
        build_cmd_uat = request.POST['build_cmd_uat']
        env_list = {'test': build_cmd_test, 'dev': build_cmd_dev, 'demo': build_cmd_demo, 'uat': build_cmd_uat}
        final_env_list = json.dumps(env_list)
        proxy_state = request.POST['proxy']
        try:
            models.CheckInfo.objects.update_or_create(App_name=app_name, App_port=app_port, App_ip_dev=app_ip_dev, App_ip_test=app_ip_test, App_ip_demo=app_ip_demo, Git_Url=git_url, Env_list=final_env_list, Proxy_state=proxy_state, Apply_user=apply_user)
        except:
            return render(request, 'appmanager/error.html')
        return render(request, 'appmanager/success.html')


#展示申请信息
def show_check_info(request):
    try:
        result = CheckInfo.objects.get_queryset().order_by('id')
    except models.CheckInfo.DoesNotExist:
        result = ''
        logger.debug('结果为空')
    paginator = Paginator(result, 10)
    page = request.GET.get('page')
    try:
        check_infos = paginator.page(page)
    except PageNotAnInteger as e:
        check_infos = paginator.page(1)
        logger.info(e)
    except EmptyPage as e:
        check_infos = paginator.page(paginator.num_pages)
        logger.info(e)

    return render(request, 'appmanager/check.html', {"check_infos": check_infos})


'''
404页面
'''


def page_not_found(request):
    return render_to_response('appmanager/404.html')


'''
审批后续操作
添加app并创建job和hook，相应信息存入数据库
'''


def check_operate(request):
    if request.method == 'POST':
        apply_user = request.POST['apply_user']
        git_url = request.POST['git_url']
        app_name = request.POST['app_name']
        app_port = request.POST['app_port']
        app_ip_dev = request.POST['app_ip_dev']
        app_ip_test = request.POST['app_ip_test']
        app_ip_demo = request.POST['app_ip_demo']
        env_list = json.loads(request.POST['env_list'].replace("'", "\""))
        status = request.POST['status']
        remarks = request.POST['remarks']
        proxy_state = request.POST['proxy_state']
        apply_date = request.POST['apply_date']
        env_ip = {'test':app_ip_test, 'dev':app_ip_dev, 'demo':app_ip_demo}
        if status == "True":
            if proxy_state == 'False':
                proxy_url = ''
            elif proxy_state == 'True' and env_list['test'] == '':
                proxy_url = app_name + '.kingxunlian.com'
            else:
                proxy_url = app_name
            for env in env_list:
                make_config_file(env, git_url, app_name, env_list[env])
                create_new_job(env, app_name)
                create_project_hook(env, app_name, git_url)
                if env != 'uat':
                    make_host_file(env, app_name, env_ip[env], app_port, proxy_state)
            models.AppInfo.objects.update_or_create(App_name=app_name,
                                                    App_port=app_port,
                                                    App_ip_dev=app_ip_dev,
                                                    App_ip_test=app_ip_test,
                                                    App_ip_demo=app_ip_demo,
                                                    Git_Url=git_url,
                                                    Proxy_Url=proxy_url,
                                                    Apply_date=apply_date,
                                                    Apply_user=apply_user)
            CheckInfo.objects.filter(App_name=app_name).delete()
        else:
            msg = "审核不通过，请根据提示重新填写"
            CheckInfo.objects.filter(App_name=app_name).update(remarks=remarks)
            print("send email"+msg)
        return redirect('/appmanager/ShowAppInfo/')


def show_consoleout(request):
    return render(request, 'appmanager/job_build_info.html')