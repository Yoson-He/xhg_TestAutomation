# -*- coding: utf-8 -*-
# @Time    : 2018/4/16 10:53
# @Author  : Yoson
# @File    : views_project.py
# @Software: PyCharm
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from common.db_handler import mysql_engine
# Create your views here.


def login(request):
    if request.session.session_key:
        return render(request, 'index.html')

    elif request.method == 'POST':
        username = request.POST.get('Username', '')
        password = request.POST.get('Password', '')

        '''
        sql = "select * from sys_user where username='%s' and password='%s'" % (username, password)
        user = mysql_engine.MySQLEngine.execute("query", sql)
        '''
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return render(request, 'index.html')
            #response.set_cookie('user', username, 86400)  # 添加浏览器Cookie
            request.session['user'] = username  # 添加session
            return response
        else:
            return render(request, 'login.html', {'error': '用户名或密码错误!'})
    else:
        return render(request, 'login.html')


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")


def main(request):
    return render(request, 'main.html')
