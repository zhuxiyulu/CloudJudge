from CloudJudge.celery import app
from django.conf import settings
import random
import string
from Authentication.setRedis import *

# 单个邮件发送
from django.core.mail import send_mail
# HTML类型邮件发送
from django.core.mail import EmailMultiAlternatives

from django.template import Context, loader

EMAIL_FROM=settings.DEFAULT_FROM_EMAIL

# emial：to_addr，接受者邮箱地址，send_type 发送邮件的情况，默认是注册时，发送

# 邮箱验证
# 邮件
class EmailVerifyRecord():

    def ___init__(self):
        self.code = None
        self.email = None
        self.send_type = None

# 生成验证码
def random_str(k):
    code = ''
    for i in range(k):
        str_num = str(random.choice(string.ascii_uppercase + string.digits))
        code += str_num
    return code

# 发送邮件任务
@app.task
def send_register_email(email, send_type="register"):
    email_record = EmailVerifyRecord()
    if send_type == "update_email":
        code = random_str(6)
    else:
        code = random_str(8)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    '''email_record.save() 遗留扩展'''

    email_title = ""
    html_content = ""

    if send_type == "register":
        subject = "Cloud Judge"

        '''
        # 发送文本邮件
        # html_content = "Thank you for your register, the captcha is :{0}.\n".format(code)
        # html_content = html_content + "The valid time is 5 minutes."
        # send_status = send_mail(email_title, html_content, EMAIL_FROM, [email])
        
        '''
        # 一个纯文本(text/plain)的为默认的，另外再提供一个 html 版本的
        # 渲染HTML
        tmp = loader.get_template('captcha.html')
        html_content = tmp.render({'code': code})
        # text
        text_content = u'感谢你的注册，本次注册的验证码为： {0}.\n' \
                       u'请保护好你的验证码，不要告诉陌生人\n' \
                       u'此验证码将于5分钟后失效'.format(code)

        msg = EmailMultiAlternatives(subject, text_content, EMAIL_FROM, [email])
        msg.attach_alternative(html_content, "text/html")
        # msg.content_subtype = 'html'
        #  msg.attach()  # 添加附件
        write_to_cache(email, code)  # 写入缓存
        send_status = msg.send()
        if send_status:
            return code
    elif send_type == "forget":
        subject = "Cloud Judge"
        html_content = "Please click the link below to reset your password: http://************/reset/{0}".format(code)

        #send_status = send_mail(subject, html_content, EMAIL_FROM, [email])
        send_status = None
        if send_status:
            pass
    elif send_type == "update_email":
        subject = "Cloud Judge"
        html_content = "You are resetting the email, the captcha is: {0}".format(code)

        #send_status = send_mail(subject, html_content, EMAIL_FROM, [email])\
        send_status = None
        if send_status:
            pass
