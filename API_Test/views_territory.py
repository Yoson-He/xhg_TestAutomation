# -*- coding: utf-8 -*-
# @Time    : 2018/4/24 15:48
# @Author  : Yoson
# @File    : views_territory.py
# @Software: PyCharm

from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from common.common import str_clean
from django.views.decorators.csrf import csrf_exempt

from common.db_handler.mysql_engine import MySQLEngine


def territory_manage(request):
    return render(request, 'API_Test/territory_manage.html')


def territory_form(request):
    return render(request, 'API_Test/territory_form.html')


def territory_add(request):
        if request.method == 'POST':
            sql = "INSERT INTO territory("
            sql_values = ') VALUES( '
            for key in request.POST:
                value = str_clean(request.POST.get(key))
                if value != '':
                    sql += "%s," % key
                    sql_values += "'%s'," % value
                elif key in ['territory_name', 'host']:
                    return HttpResponse(key)
            sql = sql[:-1] + sql_values[:-1] + ")"  # 先去掉最后的逗号，再拼接
            res = MySQLEngine().my_execute('insert', sql)
            return JsonResponse(res)


def territory_update(request):
        if request.method == 'POST':
            sql = "UPDATE territory SET "
            for key in request.POST:
                value = str_clean(request.POST.get(key))
                if key in ['territory_name', 'host'] and value == '':
                    return HttpResponse(key)
                elif value == '':
                    sql += "%s=null," % key
                else:
                    sql += "%s='%s'," % (key, value)
            sql = sql[:-1] + " WHERE id=%s" % request.POST.get('id')  # 先去掉最后的逗号，再拼接where
            print(sql)
            res = MySQLEngine().my_execute('update', sql)
            return JsonResponse(res)


def territory_query(request):
        if request.method == 'GET':
            id = request.GET.get('id')
            sql = "SELECT * FROM territory"
            if id is not None and id != '':
                sql += " WHERE id = '%s'" % id
            data = MySQLEngine().my_execute("query", sql)
            data.reverse()
            res = {"data": data}
            return JsonResponse(res)


def territory_del(request):
        if request.method == 'POST':
            sql = "DELETE FROM territory WHERE "
            for key in request.POST:
                value = str_clean(request.POST.get(key))
                if value != '':
                    sql += "%s = '%s'" % (key, value)
            res = MySQLEngine().my_execute('delete', sql)
            return JsonResponse(res)

