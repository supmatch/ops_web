from django.shortcuts import HttpResponse, render
import jenkins

server = jenkins.Jenkins('http://ci.dev.kingxunlian.com', username='qianzhong', password='Aa123456')
xml_file = "/tmp/config.xml"


def check_job(app_name):
    env = 'dev'
    if server.job_exists('dev' + '-' + app_name):
        msg = 'true'
    elif server.job_exists(app_name.split('.')[0] + '.' + env + '.kingxunlian.com'):
        msg = 'true'
    else:
        msg = ''
    return msg


'''
读取模板的配置文件并生成新的job文件
'''


def make_config_file(env, git_url, app_name, build_cmd=''):
    if app_name.find('.com') == -1:
        template_job = 'templates-{}-compile'.format(env)
    else:
        template_job = 'templates-{}-npm'.format(env)
    xml_content = server.get_job_config(template_job)
    with open(xml_file, 'wb') as fw:
        fw.write(xml_content.encode('utf-8'))
    file = open(xml_file, 'rb')
    git_content = "<url>{}</url>\n".format(git_url)
    add_content = git_content.encode('utf-8')
    old_content = file.read()
    pos = old_content.find(b"</hudson.plugins.git.UserRemoteConfig>")
    file.close()
    if pos != -1:
        content = old_content[:pos] + add_content + old_content[pos:]
        file = open(xml_file, 'wb')
        file.write(content.decode('utf-8').encode('utf-8'))
        file.close()
        data = b''
        with open(xml_file, 'rb+') as f:
            for line in f.readlines():
                if line.find(b"npm run build xxx") == 0:
                    line = bytes(build_cmd+'\n', encoding='utf-8')
                data += line
        with open(xml_file, 'wb') as f:
            f.write(data)


'''
根据xml创建新的job
'''


def create_new_job(env, app_name):
    file = open(xml_file, 'rb')
    xml = file.read().decode('utf-8')
    if app_name.find('.com') == -1:
        server.create_job(env+'-'+app_name, xml)
    elif env != 'uat':
        job_name = app_name.split('.')[0]+'.'+ env + '.kingxunlian.com'
        server.create_job(job_name, xml)
    else:
        server.create_job(app_name, xml)


'''
构建job
'''


def build_job(request):
    if request.method == "POST":
        app_name = request.POST['app_name']
        branch = request.POST['branch']
        server.build_job(app_name, {'sha1': 'origin/' + branch, 'mbranch': branch})
        return HttpResponse(True)
    else:
        return render(request, "appmanager/build_job.html")


'''
获取job构建的console out
'''


def get_consoleout(request):
        app_name = request.GET['app_name']
        last_build_info = server.get_job_info(app_name)
        last_build_number = last_build_info['lastBuild']['number']
        results = server.get_build_console_output(app_name, last_build_number)
        return HttpResponse(results)
