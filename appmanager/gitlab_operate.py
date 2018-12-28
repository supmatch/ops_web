from django.shortcuts import HttpResponse
from urllib.parse import urlencode
from urllib import request
from urllib import error
import json
import gitlab
from appmanager.models import AppInfo
import logging
logger = logging.getLogger('django')


private_token = {"PRIVATE-TOKEN": "PRIVATE-TOKEN"}
token = token
gitlab_Url = "http://gitlab.testdomain.com"
query_Uri = "/api/v4/projects?search="

'''
获取git项目对应id
添加hook、拉取分支等都需要id进行精确定位
'''


def get_project_id(app_name, git_url):
    final_url = request.Request(gitlab_Url + query_Uri + app_name, headers=private_token)
    html = request.urlopen(final_url)
    data = json.loads(html.read())
    for dict in data:
        if dict['http_url_to_repo'] == git_url:
            logger.info("获取到该项目的git--id {}".format(dict['id']))
            return dict['id']


'''
添加hook
'''


def create_project_hook(env, app_name, git_url):
    project_id = get_project_id(app_name, git_url)
    if app_name.find('.com') == -1:
        add_webhook_data = {"id": project_id, "url": "http://yourjenkins.com/project/" + env + "-" + app_name,
                            "enable_ssl_verification": "true", "token": "jenkins_token"}
    elif env != 'uat':
        job_name = app_name.split('.')[0]+'.'+ env + '.testdomain.com'
        add_webhook_data = {"id": project_id, "url": "http://yourjenkins.com/project/" + job_name,
                            "enable_ssl_verification": "true", "token": "jenkins_token"}
    else:
        add_webhook_data = {"id": project_id, "url": "http://yourjenkins.com/project/" + app_name,
                            "enable_ssl_verification": "true", "token": "jenkins_token"}
    req = request.Request(gitlab_Url + "/api/v4/projects/" + str(project_id) + "/hooks",
                          urlencode(add_webhook_data).encode(), headers=private_token)
    print(app_name, project_id)
    try:
        html = request.urlopen(req)
        final_code = html.read()
        print(final_code.decode('utf-8'))
        if html.getcode() == '201':
            logger.info("添加-- {} --的hook成功".format(app_name))
            return True

    except error.HTTPError as e:
        logger.error(e)
        return False


'''
拉取分支信息
'''


def get_branch(request):
    app_name = request.GET['app_name']
    env = app_name.split('-')[0]
    try:
        final_name = app_name.split(env + '-')[1]
    except:
        return HttpResponse("false")
    gl = gitlab.Gitlab(gitlab_Url, token)
    try:
        app_info = AppInfo.objects.get(App_name=final_name)
    except AppInfo.DoesNotExist:
        branches = ''
        return branches
    project_id = get_project_id(final_name, app_info.Git_Url)
    project_info = gl.projects.get(project_id)
    branches = project_info.branches.list()
    if branches == '':
        return HttpResponse("false")
    else:
        a = []
        for branche in branches:
            a.append(branche.name)
        a.append(env)
        return HttpResponse(json.dumps(a), content_type='application/json')


'''
添加ansible文件到gitlab
本项目目前只应用到ops/ansible
553是其git对应的id
    之后如果要应用到其他gitlab项目
    添加git地址变量
    使用上面的get_project_id获取id
'''


def add_ansible_file(filename, content, message, operate='create'):
    gl = gitlab.Gitlab(gitlab_Url, token)
    project = gl.projects.get(553)
    data = {
        'branch': 'master',
        'commit_message': message,
        'actions': [
            {
                'action': operate,
                'file_path': filename,
                'content': content
            }
        ]
    }
    project.commits.create(data)
