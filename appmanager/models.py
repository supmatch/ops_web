from django.db import models

# Create your models here.


class AppInfo(models.Model):
    App_name = models.CharField(max_length=50, unique=True)
    App_port = models.IntegerField()
    App_ip_dev = models.CharField(max_length=12)
    App_ip_test = models.CharField(max_length=12)
    App_ip_demo = models.CharField(max_length=12)
    Git_Url = models.CharField(max_length=200, verbose_name="项目git地址")
    Proxy_Url = models.CharField(max_length=200, blank=True, null=True, verbose_name="域名")
    Apply_date = models.DateTimeField(verbose_name="申请时间")
    Access_date = models.DateTimeField(auto_now_add=True, verbose_name="审核通过时间")
    Apply_user = models.CharField(max_length=50, verbose_name="申请人")

    class Meta:
        verbose_name = "项目管理表"

    def __str__(self):
        return self.App_name


class CheckInfo(models.Model):
    App_name = models.CharField(max_length=50, unique=True)
    App_port = models.IntegerField()
    App_ip_dev = models.CharField(max_length=12)
    App_ip_test = models.CharField(max_length=12)
    App_ip_demo = models.CharField(max_length=12)
    Env_list = models.CharField(max_length=200)
    Apply_date = models.DateTimeField(auto_now_add=True, verbose_name="申请时间")
    Git_Url = models.CharField(max_length=200, verbose_name="项目git地址")
    Proxy_state = models.BooleanField(default=False, verbose_name="是否需要域名")
    Apply_user = models.CharField(max_length=50, verbose_name="申请人")
    status = models.BooleanField(default=False, verbose_name="是否通过审批")
    remarks = models.TextField(blank=True, null=True, verbose_name="备注")

    class Meta:
        verbose_name = "审核状态表"

    def __str__(self):
        return self.App_name






