"""VirtualJudge URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Authentication import views as authen
from Problem import views as problem
from ErrorPage import views as error_page
from MessageCode import views as message

handler403 = error_page.permission_denied
handler404 = error_page.page_not_found
handler500 = error_page.page_error

urlpatterns = [

    # path('admin/', admin.site.urls),  # 管理员
    path('register/', authen.register, name='register'),
    path('verifyCode/', authen.verifyCode, name='verifyCode'),
    path('login/', authen.login, name='login'),
    path('logout/', authen.logout, name='logout'),
    path('profile/', authen.profile, name='profile'),
    path('saveUser/', authen.saveUser, name='saveUser'),
    path('searchUser/', authen.searchUser, name='searchUser'),
    path('viewDescription/', problem.viewDescription, name='viewDescription'),
    path('addDescription/', problem.addDescription, name='addDescription'),
    path('getCode/', message.getFrontMessageCode, name='getFrontMessageCode'),

]
