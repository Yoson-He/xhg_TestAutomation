# -*- coding: utf-8 -*-
# @Time    : 2018/4/25 16:29
# @Author  : Yoson
# @File    : views_api.py
# @Software: PyCharm
import re

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from common.common import str_clean
from django.views.decorators.csrf import csrf_exempt

from common.db_handler.mysql_engine import MySQLEngine


def api_doc(request):
    if request.session.session_key:
        return render(request, 'API_Test/api_doc.html')
    else:
        return HttpResponseRedirect('/')


def api_manage(request):
    if request.session.session_key:
        return render(request, 'API_Test/api_manage.html')
    else:
        return HttpResponseRedirect('/')


def group_form(request):
    if request.session.session_key:
        return render(request, 'API_Test/group_form.html')
    else:
        return HttpResponseRedirect('/')


def nodes_query(request):
    if request.session.session_key:
        if request.method == 'GET':
            sql = "SELECT api_group.id, group_name, project_id, project_name FROM api_group inner join project on api_group.project_id = project.id  order by project.id,api_group.id"
            data = MySQLEngine().my_execute("query", sql)
            name = []
            i = []
            nodes = []
            # 拼接树节点并返回给前端
            for each in data:
                if each["project_name"] not in name:
                    name.append(each["project_name"])
                    i.append({"name": each["project_name"], "id": each["project_id"]})
            for item in i:
                j = []
                for each in data:
                    if item["name"] == each["project_name"]:
                        j.append({"name": each["group_name"], "id": each["id"]})
                item["children"] = j
                item["spread"] = True  # 节点是否默认展开
                nodes.append(item)
            res = {"data": nodes}
            return JsonResponse(res)
    else:
        return HttpResponseRedirect('/')


def group_add(request):
    if request.session.session_key:
        if request.method == 'POST':
            sql = "INSERT INTO api_group("
            sql_values = ') VALUES( '
            for key in request.POST:
                value = str_clean(request.POST.get(key))
                if value != '':
                    sql += "%s," % key
                    sql_values += "'%s'," % value
                elif key in ['group_name', 'project_id']:
                    return HttpResponse(key)
            sql = sql[:-1] + sql_values[:-1] + ")"  # 先去掉最后的逗号，再拼接
            res = MySQLEngine().my_execute('insert', sql)
            return JsonResponse(res)
    else:
        return HttpResponseRedirect('/')


def group_query(request):
    if request.session.session_key:
        if request.method == 'GET':
            sql = "SELECT * FROM api_group"
            for key in request.GET:
                value = str_clean(request.GET.get(key))
                if value is not None and value != '':
                    sql += " WHERE %s = '%s'" % (key, value)
            data = MySQLEngine().my_execute("query", sql)
            res = {"data": data}
            return JsonResponse(res)
    else:
        return HttpResponseRedirect('/')


def group_update(request):
    if request.session.session_key:
        if request.method == 'POST':
            sql = "UPDATE api_group SET "
            for key in request.POST:
                value = str_clean(request.POST.get(key))
                if key in ['group_name'] and value == '':
                    return HttpResponse(key)
                else:
                    sql += "%s='%s'," % (key, value)
            sql = sql[:-1] + " WHERE id=%s" % request.POST.get('id')  # 先去掉最后的逗号，再拼接where
            res = MySQLEngine().my_execute('update', sql)
            return JsonResponse(res)
    else:
        return HttpResponseRedirect('/')


def group_del(request):
    if request.session.session_key:
        if request.method == 'POST':
            sql = "DELETE FROM api_group WHERE "
            for key in request.POST:
                value = str_clean(request.POST.get(key))
                if value != '':
                    sql += "%s = '%s'" % (key, value)
            res = MySQLEngine().my_execute('delete', sql)
            return JsonResponse(res)
    else:
        return HttpResponseRedirect('/')


def api_form(request):
    if request.session.session_key:
        return render(request, 'API_Test/api_form.html')
    else:
        return HttpResponseRedirect('/')


def api_add(request):
    if request.session.session_key:
        sql = "INSERT INTO api("
        sql_values = ') VALUES( '
        for key in request.POST:
            value = str_clean(request.POST.get(key))
            if value != '':
                sql += "%s," % key
                sql_values += "'%s'," % value
            elif key in ['api_name', 'protocol', 'method', 'path']:
                return HttpResponse(key)
        sql = sql[:-1] + sql_values[:-1] + ")"  # 先去掉最后的逗号，再拼接
        res = MySQLEngine().my_execute('insert', sql)
        return JsonResponse(res)
    else:
        return HttpResponseRedirect('/')


def api_query(request):
    if request.session.session_key:
        if request.method == 'GET':
            sql = "SELECT * FROM api"
            for key in request.GET:
                value = str_clean(request.GET.get(key))
                if key =='page':
                    page = value
                elif key =='limit':
                    limit = value
                elif value is not None and value != '':
                    sql += " WHERE %s = '%s'" % (key, value)
            sql += " ORDER BY id DESC LIMIT " + str((int(page) - 1) * int(limit)) + "," + str(limit)
            data = MySQLEngine().my_execute("query", sql)
            count = MySQLEngine().my_execute("query",  "SELECT COUNT(*) FROM api")
            return JsonResponse({'code': 0, 'msg': 'ok', 'count': count[0]["COUNT(*)"], 'data': data})
        else:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')


def api_del(request):
    if request.session.session_key:
        if request.method == 'POST':
            sql = "DELETE FROM api WHERE "
            for key in request.POST:
                value = str_clean(request.POST.get(key))
                if value != '':
                    sql += "%s = '%s'" % (key, value)
            res = MySQLEngine().my_execute('delete', sql)
            print(res)
            return JsonResponse(res)
    else:
        return HttpResponseRedirect('/')
'''
def api_update(request):
    if request.session.session_key:
        if request.method == 'POST':
            sql = "UPDATE api SET "
            for key in request.POST:
                value = str_clean(request.POST.get(key))
                if value != '':
                    sql += "%s='%s'," % (key, value)
                elif key in ['api_name', 'project_id', 'host']:
                    return HttpResponse(key)
            sql = sql[:-1] + " WHERE id=%s" % request.POST.get('id')  # 先去掉最后的逗号，再拼接where
            res = MySQLEngine().my_execute('update', sql)
            return JsonResponse(res)
    else:
        return HttpResponseRedirect('/')






'''
