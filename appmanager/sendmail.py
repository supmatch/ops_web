from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import HttpResponse

'''
发送邮件，返回邮件状态
'''


def send_email(email_title, email_message, email_send_list):
    email_title = email_title
    email_message = email_message
    email_send_list = email_send_list
    send_status = send_mail(email_title, email_message, settings.DEFAULT_FROM_EMAIL, email_send_list)
    return send_status


def test(request):
    email_title = '%s申请添加App' % request.user.username
    email_message = '请审核提交的表单信息'
    email_send_list = ['qianzhong@kingxunlian.com']
    email_html_message = '<h1>包含 html 标签且不希望被转义的内容</h1>'
    send_status = send_mail(email_title, email_message, settings.DEFAULT_FROM_EMAIL, email_send_list, email_html_message)
    return HttpResponse(send_status)


if __name__ == '__main__':
    send_email('test', 'test-message', 'qianzhong@kingxunlian.com')