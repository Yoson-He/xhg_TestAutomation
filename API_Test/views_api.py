# -*- coding: utf-8 -*-
# @Time    : 2018/4/25 16:29
# @Author  : Yoson
# @File    : views_api.py
# @Software: PyCharm
import re

from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from common.common import str_clean
from django.views.decorators.csrf import csrf_exempt

from common.db_handler.mysql_engine import MySQLEngine


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
                elif key in ['group_name']:
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
                if value != '':
                    sql += "%s='%s'," % (key, value)
                elif key in ['group_name']:
                    return HttpResponse(key)
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


def api_details(request):
    if request.session.session_key:
        return render(request, 'API_Test/api_details.html')
    else:
        return HttpResponseRedirect('/')


def api_document(request):
    if request.session.session_key:
        return render(request, 'API_Test/api_document.html')
    else:
        return HttpResponseRedirect('/')


def api_add(request):
    if request.session.session_key:
        if request.method == 'POST':
            sql1 = "INSERT INTO api("
            sql2 = "INSERT INTO api_params(api_id,param_type,param_key,description,required,data_type,sample)VALUES"
            sql1_values = ') VALUES( '
            sql2_values = []
            temp = {"param_type": '', "key": '', "description": '', "required": '', "data_type": '', "sample": ''}
            for key in request.POST:
                if key == 'project_id':
                    continue
                value = str_clean(request.POST.get(key))

                if re.match('header_key', key) is not None:
                    temp["param_type"] = 1
                    temp["key"] = value
                    continue
                if re.match("uri_key", key) is not None:
                    temp["param_type"] = 2
                    temp["key"] = value
                    continue
                if re.match("query_key", key) is not None:
                    temp["param_type"] = 3
                    temp["key"] = value
                    continue
                if re.match("body_key", key) is not None:
                    temp["param_type"] = 4
                    temp["key"] = value
                    continue
                if re.match("response_key", key) is not None:
                    temp["param_type"] = 5
                    temp["key"] = value
                    continue
                if (re.match("uri_description", key) is not None) or (
                        re.match("query_description", key) is not None) or (
                        re.match("body_description", key) is not None) or (
                        re.match("response_description", key) is not None):
                    temp["description"] = value
                    continue
                if (re.match("query_required", key) is not None) or (
                        re.match("body_required", key) is not None) or (
                        re.match("response_required", key) is not None):
                    temp["required"] = value
                    continue
                if (re.match("body_type", key) is not None) or (
                        re.match("response_type", key) is not None):
                    temp["data_type"] = value
                    continue
                if (re.match("header_value", key) is not None) or (
                        re.match("uri_sample", key) is not None) or (
                        re.match("response_sample", key) is not None) or (
                        re.match("query_sample", key) is not None) or (
                        re.match("body_sample", key) is not None):
                    temp["sample"] = value
                    sql2_values.append(temp)
                    temp = {"param_type": '', "key": '', "description": '', "required": '', "data_type": '',
                            "sample": ''}

                elif value != '':
                    sql1 += "%s," % key
                    sql1_values += "'%s'," % value
                elif key in ['api_name', 'protocol', 'path', 'method']:
                    return HttpResponse(key)
            sql1 = sql1[:-1] + sql1_values[:-1] + ")"  # 先去掉最后的逗号，再拼接
            res = MySQLEngine().my_execute('insert', sql1)

            api_id = res["insert_id"]
            for each in sql2_values:
                if each["key"] == '':
                    sql2_values.remove(each)
                else:
                    sql2 += "(" + str(api_id) + "," + str(each["param_type"]) + ",'" + str(each["key"]) + "','" + str(each[
                        "description"]) + "','" + str(each["required"]) + "','" + str(each["data_type"]) + "','" + str(each[
                                "sample"]) + "'),"
            if sql2[-1] != "S":
                sql2 = sql2[:-1]
                MySQLEngine().my_execute('insert', sql2)
            return JsonResponse(res)
    else:
        return HttpResponseRedirect('/')


def api_query(request):
    if request.session.session_key:
        if request.method == 'GET':
            sql = "SELECT * FROM api"
            for key in request.GET:
                value = str_clean(request.GET.get(key))
                if value is not None and value != '':
                    sql += " WHERE %s = '%s'" % (key, value)
                data = MySQLEngine().my_execute("query", sql)
                data.reverse()
                res = {"data": data}
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





def api_del(request):
    if request.session.session_key:
        if request.method == 'POST':
            sql = "DELETE FROM api WHERE "
            for key in request.POST:
                value = str_clean(request.POST.get(key))
                if value != '':
                    sql += "%s = '%s'" % (key, value)
            res = MySQLEngine().my_execute('delete', sql)
            return JsonResponse(res)
    else:
        return HttpResponseRedirect('/')
'''
