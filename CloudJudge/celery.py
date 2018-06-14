from __future__ import absolute_import
import django
import os
from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CloudJudge.settings')
django.setup()

app = Celery('Authentication')
# 从Django的设置文件中导入CELERY设置
app.config_from_object('django.conf:settings')
# 从所有已注册的app中加载任务模块
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)