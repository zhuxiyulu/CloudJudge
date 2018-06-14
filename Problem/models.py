from django.db import models

# Create your models here.
from mongoengine import *
import datetime

# 题目信息表
class Problem(models.Model):
    title = models.CharField('title', max_length=100)  # 标题
    problemUrl = models.CharField('problemUrl', max_length=255)  # 题目在原oj的 url
    source = models.CharField('source', max_length=100, null=True)  # 题目在原oj的来源
    sourceUrl = models.CharField('sourceUrl', max_length=255, null=True)  # 题目在原oj来源的url
    originalOJ = models.CharField('originalOJ', max_length=10)  # 原oj名
    originalProblem = models.CharField('originalProblem', max_length=20)  # 原oj题号
    updateTime = models.DateTimeField('updateTime', auto_now=True)  # 最近更新时间
    overallAttempted = models.IntegerField('overallAttempted', default=0)  # 总提交量
    overallAccepted = models.IntegerField('overallAccepted', default=0)  # 总解决量

    def __str__(self):
        return self.title
    # 定义表名
    class Meta:
        db_table = "Problem"


# 题目描述
class Description(Document):

    meta = {
        # 数据库中显示的名字
        'collection': 'Description',
    }
    problemId = IntField(unique=True)  # 该题目在mysql数据库中Problem表的Id
    title = StringField(max_length=100)  # 标题
    originalOJ = StringField(max_length=10)  # 原oj名称
    originalProblem = StringField(max_length=20)  # 原oj题号
    problemUrl = StringField(max_length=255)  # 在原oj的url
    timeLimit = StringField(max_length=20)  # 时间限制
    memoryLimit = StringField(max_length=20)  # 内存限制
    content = StringField()  # 描述
    imageSource = StringField(max_length=200, null=True)  # 题目描述中包含的图标地址
    problemInput = StringField()  # input
    problemOutput = StringField()  # output
    sampleInput = StringField()  # 样例输入
    sampleOutput = StringField()  # 样例输出
    hint = StringField(null=True)  # 提示
    updateTime = DateTimeField(default=datetime.datetime.now)  # 最近更新时间

