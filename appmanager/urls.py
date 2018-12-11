from django.urls import path, re_path
from appmanager import views, jenkins_operate, gitlab_operate, appinfo_check, openstack_operate

urlpatterns = [
    re_path(r'^$', views.show_app_info),
    re_path(r'^ShowAppInfo/$', views.show_app_info),
    re_path(r'^AddAppForm/$', views.add_app_form),
    re_path(r'^AddFeForm/$', views.add_fe_form),
    re_path(r'^BuildJob/$', jenkins_operate.build_job),
    re_path(r'^CheckJob/$', jenkins_operate.check_job),
    re_path(r'^CheckAppName/$', appinfo_check.check_app_name),
    re_path(r'^CheckAppPort/$', appinfo_check.check_app_port),
    re_path(r'^SaveApply/$', views.save_apply),
    re_path(r'^CheckOperate/$', views.check_operate),
    re_path(r'^GetBranch/$', gitlab_operate.get_branch),
    re_path(r'^ShowCheckInfo/', views.show_check_info),
    re_path(r'^GetConsoleOut/', jenkins_operate.get_consoleout),
    re_path(r'^ShowConsoleOut/', views.show_consoleout),
    re_path(r'^AddServerApply/', openstack_operate.add_server_apply),
    re_path(r'^CreateServer/', openstack_operate.create_server),
    re_path(r'^CheckServerName/', openstack_operate.check_name),
    re_path(r'^ShowServerInfo/', openstack_operate.show_server_info),
]