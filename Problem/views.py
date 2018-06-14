# coding:utf-8
from django.shortcuts import render

# Create your views here.
from Problem.models import Description, Problem
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import json

# 时间
from django.utils import timezone
import signal

# 获取题目描述
@csrf_exempt
def viewDescription(request):
    message = {}
    message['code'] = 0
    message['msg'] = None

    if request.method == 'GET':
        if 'problemId' in request.GET:
            problemId = int(request.GET['problemId'])
            description = Description.objects(problemId=problemId).first()
            # 现有数据库中有这个题目的描述
            if description:
               message['code'] = 1
               message['title'] = description.title
               message['originalOJ'] = description.originalOJ
               message['originalProblem'] = description.originalProblem
               message['problemUrl'] = description.problemUrl
               message['timeLimit'] = description.timeLimit
               message['memoryLimit'] = description.memoryLimit
               message['content'] = description.content
               message['imageSource'] = description.imageSource
               message['problemInput'] = description.problemInput
               message['problemOutput'] = description.problemOutput
               message['sampleInput'] = description.sampleInput
               message['sampleOutput'] = description.sampleOutput
               message['hint'] = description.hint
               return JsonResponse(message)
            # 现有数据库中没有该题目的描述，给爬虫提交任务，爬去题目描述
            else:
                problemUrl = request.GET['problemUrl']
                '''设定时间，超过时间显示获取失败'''
            description = spiderDescription(problemId, problemUrl)

            if description is None:
                message['msg'] = u'题目获取失败'
                return JsonResponse(message)
            else:
                message['code'] = 1
                message['title'] = description.title
                message['originalOJ'] = description.originalOJ
                message['originalProblem'] = description.originalProblem
                message['problemUrl'] = description.problemUrl
                message['timeLimit'] = description.timeLimit
                message['memoryLimit'] = description.memoryLimit
                message['content'] = description.content
                message['imageSource'] = description.imageSource
                message['problemInput'] = description.problemInput
                message['problemOutput'] = description.problemOutput
                message['sampleInput'] = description.sampleInput
                message['sampleOutput'] = description.sampleOutput
                message['hint'] = description.hint
                return JsonResponse(message)

        else:
            message['msg'] = u'题目获取失败'
            return JsonResponse(message)
    else:
        message['msg'] = u'题目获取失败'
        return JsonResponse(message)


# 给爬虫提交爬取题目的任务
def spiderDescription(porblemId,problemUrl):
    description = {}

    if problemUrl is None:
       problem = Problem.objects.get(id=porblemId)
       if problem:
           problemUrl = problem.problemUrl
           '''调用爬虫接口'''
           pass

    else:
        '''调用爬虫借口'''
        pass

    return description


# 用过户后台添加题目描述
@csrf_exempt
def addDescription(request):
    message = {}
    message['code'] = 0
    message['msg'] = None
    if request.method == 'POST':

        if 'problemId' in request.POST:
            problemId = int(request.POST['problemId'])
        else:
            message['msg'] = "The problemId can not be empty!"
            return JsonResponse(message)
        if 'title' in request.POST:
            title = request.POST['title']
        else:
            message['msg'] = "The title can not be empty!"
            return JsonResponse(message)
        if 'originalOJ' in request.POST:
            originalOJ = request.POST['originalOJ']
        else:
            message['msg'] = "The originalOJ can not be empty!"
            return JsonResponse(message)
        if 'originalProblem' in request.POST:
            originalProblem = request.POST['originalProblem']
        else:
            message['msg'] = "The originalProblem can not be empty!"
            return JsonResponse(message)
        if 'problemUrl' in request.POST:
            problemUrl = request.POST['problemUrl']
        else:
            message['msg'] = "The problemUrl can not be empty!"
            return JsonResponse(message)
        if 'timeLimit' in request.POST:
            timeLimit = request.POST['timeLimit']
        else:
            message['msg'] = "The timeLimit can not be empty!"
            return JsonResponse(message)
        if 'memoryLimit' in request.POST:
            memoryLimit = request.POST['memoryLimit']
        else:
            message['msg'] = "The memoryLimit can not be emnpty!"
            return JsonResponse(message)
        if 'content' in request.POST:
            content = request.POST['content']
        else:
            message['msg'] = "The description can not be empty!"
            return JsonResponse(message)
        '''imageSource'''
        if 'problemInput' in request.POST:
            problemInput = request.POST['problemInput']
        else:
            message['msg'] = "The problemInput can not be empty!"
            return JsonResponse(message)
        if 'problemOutput' in request.POST:
            problemOutput = request.POST['problemOutput']
        else:
            message['msg'] = "The problemOutput can not be empty!"
            return JsonResponse(message)
        if 'sampleInput' in request.POST:
            sampleInput = request.POST['sampleInput']
        else:
            message['msg'] = "The sampleInput can not be empty!"
            return JsonResponse(message)
        if 'sampleOutput' in request.POST:
            sampleOutput = request.POST['sampleOutput']
        else:
            message['msg'] = "The sampleOutput can not be empty!"
            return JsonResponse(message)
        hint = request.POST['hint']

        '''新建文档'''
        description = Description.objects(problemId=problemId)
        if description:
            message['msg'] = "The document is already exists"
            return JsonResponse(message)
        else:
            description = Description(problemId=problemId)

        description.title = title
        description.originalOJ = originalOJ
        description.originalProblem = originalProblem
        description.problemUrl = problemUrl
        description.timeLimit = timeLimit
        description.memoryLimit = memoryLimit
        description.content = content
        description.problemInput = problemInput
        description.problemOutput = problemOutput
        description.sampleInput = sampleInput
        description.sampleOutput = sampleOutput
        description.hint = hint
        description.updateTime = timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M:%S")
        description.save()
        message['code'] = 1
        message['msg'] = "Insert document successful!"
        return JsonResponse(message)

    else:
        message['msg'] = "Add problem description failed!"
        return JsonResponse(message)

# 请求更新题目
def updateProblem(request):
    pass


'''
功能（显示的）
查看题目列表（通过题目名字模糊查找，按照AC、提交量、源OJ的ID排序，通过OJ筛选） mysql 

提交代码（多种语言提交，代码编辑器）
全局提交状态列表，选择显示几条（20,40,60,80,100）（可以通过用户名，运行结果、语言筛选，根据时间排序）
获取单独的一个提交状态。
获取源OJ当前状态。
收藏一道题。

管理员后台
获取前端服务器、API服务器，爬虫服务器的CPU负载和内存占用。
用户管理（添加、删除、冻结、查找，修改）
题目管理（请求更新题目）
查看某一题的提交情况（WA、RE、AC每种结果的数量，每种语言的使用数量，并且可以把所有对应提交的全都显示出来，可筛选）
查看一个用户的提交情况（WA、RE、AC每种结果的数量，每种语言的使用数量，并且可以把所有对应提交的全都显示出来，可筛选）
'''