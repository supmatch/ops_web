import os
from appmanager.gitlab_operate import add_ansible_file


'''
创建hosts文件并添加yml
'''


def make_host_file(env, app_name, app_ip, app_port, proxy_state):
    file_path = 'inventories/{}'.format(env)
    if os.path.exists(file_path) is False:
        os.makedirs(file_path)
    if app_name.find('.com') != -1:
        app_name = app_name.split('.')[0] + '.' + env + '.kingxunlian.com'
    file_name = '{}/{}'.format(file_path, app_name)
    data = '[' + app_name + ']' + '\n' + app_ip
    message = 'add a new {}-{}-{}'.format(app_name, env, file_name)
    add_ansible_file(file_name, data, message)
    make_yaml_file(env, app_name, app_port, app_ip, proxy_state)


'''
创建group_vars/*.yml文件
如果没有编译命令，说明是后端服务
根据是否需要反代域名来添加后续配置
'''


def make_yaml_file(env, app_name, app_port, app_ip, proxy_state='False'):
    file_path = 'inventories/{}/group_vars'.format(env)
    if os.path.exists(file_path) is False:
        os.makedirs(file_path)
    yaml_file_name = '{}/{}.yml'.format(file_path, app_name)

    if app_name.find('.com') == -1 :
        port_content = '---\n' + '  app_port: {} \n'.format(app_port)
        params_content = '  jvm_option: "-Xms512m -Xmx512m -XX:PermSize=258M -XX:MaxPermSize=512m"\n' + '  java_option_before: ""\n' + '  java_option_after: ""\n' + '  project_name_config: ""\n'

        if proxy_state == 'True':
            proxy_url = app_name + '.' + env + '.kingxunlian.com'
            proxy_params = '  http_port: "80"\n' + '  https_port: "443"\n' + '  denied_proxy: true\n' + '  rule_access: false\n'
            proxy_url_content = '  proxy_url:\n' + '    - "{}"\n'.format(proxy_url)
            proxy_host_content = '  proxy_hosts:\n' + '    - "{}"\n'.format(app_ip)
            proxy_content = proxy_params + proxy_url_content + proxy_host_content
        else:
            proxy_content = ''
        content = port_content + params_content + proxy_content

    else:
        '''
        如果只是前端，只需要生成前端的配置文件即可
        '''
        proxy_params = '---\n' + '  http_port: "80"\n' + '  https_port: "443"\n' + '  denied_proxy: true\n' + '  rule_access: false\n'
        proxy_url_content = '  proxy_url:\n' + '    - "{}"\n'.format(app_name)
        proxy_host_content = '  proxy_hosts:\n' + '    - "{}"\n'.format(app_ip)
        content = proxy_params + proxy_url_content + proxy_host_content
    message = 'add a new {}-{}-{}'.format(app_name, env, yaml_file_name)
    add_ansible_file(yaml_file_name, content, message)

