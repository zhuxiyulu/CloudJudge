# coding:utf-8

from django.shortcuts import render

# Create your views here.

# 异常
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from Authentication.models import User
import json
from django.http import JsonResponse
# csrf验证保护或者取消
from django.views.decorators.csrf import csrf_exempt, csrf_protect
# 加密
from django.contrib.auth.hashers import make_password, check_password
#redis 缓存
from django.views.decorators.cache import cache_page
from Authentication.setRedis import *
# 发送邮件
from Authentication.tasks import send_register_email
# 获取token
from django.middleware.csrf import get_token
from django.http import HttpResponse
# 多字段查询
from django.db.models import Q
# 加密
import hashlib
import CloudJudge.info as info

BackMessageCode = info.getBackMessage()

@csrf_exempt
# 用户登录
def login(request):

    message = {}

    if request.method == 'POST':

        data_str = ((request.body).decode('utf-8'))
        data = json.loads(data_str)

        # content-type:json

        if 'Email' in data:
            email = data['Email']
            if email == "":
                message['Code'] = BackMessageCode['Username_Empty']
                return HttpResponse(json.dumps(message), content_type="application/json")
        else:
            message['Code'] = BackMessageCode['Username_Empty']
            return HttpResponse(json.dumps(message), content_type="application/json")

        if 'Password' in data:
            password = data['Password']
            if password == "":
                message['Code'] = BackMessageCode['Password_Empty']
                return HttpResponse(json.dumps(message), content_type="application/json")
        else:
            message['Code'] = BackMessageCode['Password_Empty']
            return HttpResponse(json.dumps(message), content_type="application/json")

        # 获取的表单与数据库比较

        user = User.objects.filter(email=email)
        if user:
            password_list = list(user.values('password'))
            nickname_list = list(user.values('nickname'))
            iconUrl_list = list(user.values('iconUrl'))
            encrypt_password = password_list[0]['password']
            nickname = nickname_list[0]['nickname']
            iconUrl = iconUrl_list[0]['iconUrl']

            if check_password(password, encrypt_password):
                if nickname:
                    message['Username'] = nickname
                else:
                    message['Username'] = email

                request.session['email'] = email
                token = get_token(request)
                message['Code'] = 0
                message['Token'] = token
                message['IconUrl'] = iconUrl

                return HttpResponse(json.dumps(message), content_type="application/json")
            else:
                message['Code'] = BackMessageCode['Username_NotEqual_Password']
                return HttpResponse(json.dumps(message), content_type="application/json")
        else:
            message['Code'] = BackMessageCode['Username_NotEqual_Password']
            return HttpResponse(json.dumps(message), content_type="application/json")

    return HttpResponse(status=400)


# 用户登出
def logout(request):
    message = {}
    if request.method == 'GET':
        try:
            del request.session['email']
            message['Code'] = 0
            return HttpResponse(json.dumps(message), content_type="application/json")
        except KeyError:
            message['Code'] = BackMessageCode['LogoutFailed']
            return HttpResponse(json.dumps(message), content_type="application/json")
    else:
        return HttpResponse(status=400)


@csrf_exempt
# 用户注册
def register(request):
    message = {}

    if request.method == 'POST':

        data_str = ((request.body).decode('utf-8'))
        data = json.loads(data_str)

        if 'Email' in data:
            email = data['Email']
            if email == "":
                message['Code'] = BackMessageCode['Username_Empty']
                return HttpResponse(json.dumps(message), content_type="application/json")
        else:
            message['Code'] = BackMessageCode['Username_Empty']
            return HttpResponse(json.dumps(message), content_type="application/json")

        if 'Password' in data:
            password = data['Password']
            if password == "":
                message['Code'] = BackMessageCode['Password_Empty']
                return HttpResponse(json.dumps(message), content_type="application/json")
        else:
            message['Code'] = BackMessageCode['Password_Empty']
            return HttpResponse(json.dumps(message), content_type="application/json")

        if 'Vercode' in data:
            captcha = data['Vercode']
            if captcha == "":
                message['Code'] = BackMessageCode['Captcha_Empty']
                return HttpResponse(json.dumps(message), content_type="application/json")
            register_captcha = read_from_cache(email)
            if register_captcha is None:
                message['Code'] = BackMessageCode['Captcha_Wrong']
                return HttpResponse(json.dumps(message), content_type="application/json")
            elif captcha != register_captcha:
                message['Code'] = BackMessageCode['Captcha_Wrong']
                return HttpResponse(json.dumps(message), content_type="application/json")
            else:
                pass
        else:
            message['Code'] = BackMessageCode['Captcha_Empty']
            return HttpResponse(json.dumps(message), content_type="application/json")

        # 该用户是否存在
        try:
            user = User.objects.get(email=email)
        # 查询到>=两个对象
        except MultipleObjectsReturned:
            message['Code'] = BackMessageCode['User_Exists']
            return HttpResponse(json.dumps(message), content_type="application/json")
        # 没有该对象
        except ObjectDoesNotExist:
            pass
        # 有一个对象
        else:
            message['Code'] = BackMessageCode['User_Exists']
            return HttpResponse(json.dumps(message), content_type="application/json")

        if not message['msg']:
            user = User()
            user.email = email
            encrypt_password = make_password(password)
            user.password = encrypt_password
            user.iconUrl = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
            user.save()

            message['Code'] = 0
            return HttpResponse(json.dumps(message), content_type="application/json")
    else:
        return HttpResponse(status=400)


# 注册时获取验证码
@csrf_exempt
@cache_page(20)  # 在需要缓存的视图上添加装饰器, 参数是设置timeout 超时时间， 单位是秒，
def verifyCode(request):
    message = {}

    if request.method == 'POST':
        data_str = ((request.body).decode('utf-8'))
        data = json.loads(data_str)

        if 'Email' in data:
            email = data['Email']
            if email == "":
                message['Code'] = BackMessageCode['Username_Empty']
                return HttpResponse(json.dumps(message), content_type="application/json")
            '''发送邮件获取验证码，有效期5分钟，缓存'''
            send_register_email.delay(email, "register")
            message['Code'] = 0
            return HttpResponse(json.dumps(message), content_type="application/json")

        else:
            message['Code'] = BackMessageCode['Username_Empty']
            return HttpResponse(json.dumps(message), content_type="application/json")
    else:
        return HttpResponse(status=400)


# 显示用户信息
def profile(request):
    message={}
    message['code'] = 1
    message['msg'] = None
    if request.method == 'GET':
        try:
            email = request.session['email']
            user = User.objects.get(email=email)
            message['nickname'] = user.nickname
            message['QQ'] = user.QQ
            message['school'] = user.school
            message['email'] = user.email
            message['overallAttempted'] = user.overallAttempted
            message['overallSolved'] = user.overallSolved
            message['iconUrl'] = user.iconUrl
            message['code'] = 0
            return HttpResponse(json.dumps(message), content_type="application/json")
        except KeyError:
            message['msg'] = 'Please login first!'
            return HttpResponse(json.dumps(message), content_type="application/json")
    else:
        return HttpResponse(status=400)

@csrf_exempt
# 修改用户信息
def saveUser(request):
    message = {}
    message['code'] = 1
    message['msg'] = None
    try:
        email = request.session['email']
        if request.method == "POST":

            if not request.POST.get('original_password'):
                message['msg'] = 'Original Password can not be empty'
                return JsonResponse(message)
            else:
                original_password = request.POST.get('original_password')

            if not request.POST.get('password'):
                message['msg'] = 'Password can not be empty'
                return JsonResponse(message)
            else:
                password = request.POST.get('password')

            if not request.POST.get('password_two'):
                message['msg'] = 'Two passwords are not the same!'
                return JsonResponse(message)
            else:
                password_two = request.POST.get('password_two')

            # 两次密码是否相同
            if password_two != password:
                message['msg'] = 'Two passwords are not the same!'
                return JsonResponse(message)

            nickname = request.POST.get('nickname')

            school = request.POST.get('school')

            QQ = request.POST.get('QQ')

            user = User.objects.get(email=email)
            pwd = user.password
            if pwd != original_password:
                message['msg'] = 'Original password is wrong!'
                return JsonResponse(message)

            if not message['msg']:
                user.password = make_password(password)
                user.nickname = nickname
                user.school = school
                user.QQ = QQ
                user.save()
                message['msg'] = 'Save profile information success'
                message['code'] = 0
                return JsonResponse(message)
        else:
            return HttpResponse(status=400)

    except KeyError:
        message['msg'] = 'Please login first!'
        return JsonResponse(message)

@csrf_exempt
# 按照邮箱、昵称模糊搜索用户
def searchUser(request):
    message = {}
    message['code'] = 1
    message['search_result'] = {}
    email = None
    nickname = None
    school = None

    if request.method == 'POST':
        if 'email' in request.POST:
            email = request.POST['email']

        if 'nickname' in request.POST:
            nickname = request.POST['nickname']

        if 'school' in request.POST:
            school = request.POST['school']

        if email and nickname and school:
            user = User.objects.filter(Q(email__icontains=email)
                                       & Q(nickname__icontains=nickname)
                                       & Q(school__icontains=school))

        elif email is None and nickname and school:
            user = User.objects.filter(nickname__icontains=nickname).filter(school__icontains=school)
        elif email and nickname is None and school:
            user = User.objects.filter(email__icontains=email).filter(school__icontains=school)
        elif email and nickname and school is None:
            user = User.objects.filter(email__icontains=email).filter(nickname__icontains=nickname)
        elif email and nickname is None and school is None:
            user = User.objects.filter(email__icontains=email)
        elif email is None and nickname and school is None:
            user = User.objects.filter(nickname__icontains=nickname)
        elif email is None and nickname is None and school:
            user = User.objects.filter(school__icontains=school)
        else:
            message['msg'] = "No such search result!"
            return JsonResponse(message)
        search_result = {}
        if user:
            user_values = user.all().values('email', 'nickname', 'school', 'overallAttempted', 'overallSolved').\
                order_by('-overallSolved')

            user_list = list(user_values)
            for i in range(len(user_list)):
                email = user_list[i]['email']
                nickname = user_list[i]['nickname']
                school = user_list[i]['school']
                overallAttempted = user_list[i]['overallAttempted']
                overallSolved = user_list[i]['overallSolved']

                search_result['email'] = email
                search_result['nickname'] = nickname
                search_result['school'] = school
                search_result['overallAttempted'] = overallAttempted
                search_result['overallSolved'] = overallSolved
                message['search_result'][i] = search_result

            message['code'] = 0
            return JsonResponse(message)
        else:
            message['msg'] = "No such search result!"
            return JsonResponse(message)

    else:
        return HttpResponse(status=400)
