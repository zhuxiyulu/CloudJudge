from __future__ import unicode_literals
from django.db import models

# Create your models here.

from django.utils.encoding import python_2_unicode_compatible
# 时间
import django.utils.timezone as timezone

# 用户信息

@python_2_unicode_compatible
class User(models.Model):

    email = models.CharField('email', max_length=50)  # 邮箱
    password = models.CharField('password', max_length=200)  # 密码
    nickname = models.CharField('nickname', max_length=30)  # 昵称
    school = models.CharField('school', max_length=50, null=True)  # 学校
    QQ = models.CharField('QQ', max_length=20, null=True)  # QQ
    iconUrl = models.CharField('iconUrl', max_length=300, null=True)
    overallAttempted = models.IntegerField('overallAttempted', default=0)  # 总提交量
    overallSolved = models.IntegerField('overallSolved', default=0)  # 总解决量
    is_superuser = models.IntegerField('is_superuser', default=0)  # 是否为管理员
    date_joined = models.DateTimeField('date_joined', default=timezone.now)  # 注册时间
    last_login = models.DateTimeField('last_login', auto_now=True)  # 最近登录的时间

    def __str__(self):
        return self.username
    # 定义表名
    class Meta:
        db_table = "User"
