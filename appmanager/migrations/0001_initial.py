# Generated by Django 2.0.7 on 2018-10-17 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AppInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('App_name', models.CharField(max_length=50, unique=True)),
                ('App_port', models.IntegerField()),
                ('App_ip_dev', models.CharField(max_length=12)),
                ('App_ip_test', models.CharField(max_length=12)),
                ('App_ip_demo', models.CharField(max_length=12)),
                ('Git_Url', models.CharField(max_length=200, verbose_name='项目git地址')),
                ('Apply_date', models.DateTimeField(verbose_name='申请时间')),
                ('Access_date', models.DateTimeField(auto_now_add=True, verbose_name='审核通过时间')),
                ('Apply_user', models.CharField(max_length=50, verbose_name='申请人')),
            ],
            options={
                'verbose_name': '项目管理表',
            },
        ),
        migrations.CreateModel(
            name='Check_Info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('App_name', models.CharField(max_length=50, unique=True)),
                ('App_port', models.IntegerField()),
                ('App_ip_dev', models.CharField(max_length=12)),
                ('App_ip_test', models.CharField(max_length=12)),
                ('App_ip_demo', models.CharField(max_length=12)),
                ('Env_list', models.CharField(max_length=200)),
                ('Apply_date', models.DateTimeField(auto_now_add=True, verbose_name='申请时间')),
                ('Git_Url', models.CharField(max_length=200, verbose_name='项目git地址')),
                ('Apply_user', models.CharField(max_length=50, verbose_name='申请人')),
                ('status', models.BooleanField(default=False, verbose_name='是否通过审批')),
                ('remarks', models.TextField(blank=True, null=True, verbose_name='备注')),
            ],
            options={
                'verbose_name': '审核状态表',
            },
        ),
    ]