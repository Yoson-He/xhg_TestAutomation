# -*- coding: utf-8 -*-
# @Time    : 2018/4/25 16:29
# @Author  : Yoson
# @File    : views_api.py
# @Software: PyCharm
import json
import re

import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import markdown
from common.common import str_clean
from common.db_handler.mysql_engine import MySQLEngine


def api_request(request):
    url = request.POST["host"] + request.POST["path"]
    method = request.POST["method"]
    data = request.POST["body_param"]
    if method == "GET":
        data = request.POST["query_param"]
    res = requests.request(method, url, data=data, headers={"Content-Type": "application/json"})
    print(res.url)
    print(res.raise_for_status())
    return JsonResponse({"data": res.text})


def debug_form(request):
    res = requests.post("http://10.10.10.201:801/showdoc/server/index.php?s=/api/page/info",
                        data={'page_id': request.GET["page_id"]})
    page_content = json.loads(res.text)["data"]["page_content"]

    api_name = re.search(r'\*\*简要描述：\*\* \n\n- (.*?)\n\n', page_content, re.S)
    if api_name is not None:
        api_name = api_name.group(1)

    path = re.search(r'\*\*请求URL：\*\* \n- `(.*?)`\n', page_content, re.S)
    if path is not None:
        path = "/" + request.GET["app"] + str_clean(path.group(1))

    method = re.search(r'\*\*请求方式：\*\*\n-(.*?)\n', page_content, re.S)
    if method is not None:
        method = str_clean(method.group(1))

    if method == "POST":
        body_param = re.search(r'\*\*请求示例\*\*\n\n``` \n(.*?)\n```', page_content, re.S)
        if body_param is not None:
            body_param = body_param.group(1)
            body_param = body_param.replace("&quot;", '')
    elif method == "GET":
        qurey_param = {}


    return JsonResponse({"api_name": api_name, "path": path, "method": method, "body_param": body_param})


def get_nodes(request):
    nodes=[]
    if request.GET["app"] == "merchant":
        res = requests.post("http://10.10.10.201:801/showdoc/server/index.php?s=/api/item/info", data = {'item_id':17,'default_page_id':0})
        for i in json.loads(res.text)["data"]["menu"]["catalogs"][0]["catalogs"]:
            children = []
            for j in i["pages"]:
                children.append({"name": j["page_title"], "page_id": j["page_id"]})
            nodes.append({"name": i["cat_name"], "children": children})
    return JsonResponse({"data": nodes})


def get_api(request):
    res = requests.post("http://10.10.10.201:801/showdoc/server/index.php?s=/api/page/info", data = {'page_id':request.GET["page_id"]})
    page_content = json.loads(res.text)["data"]["page_content"]
    #page_content = markdown.markdown(page_content, ['codehilite', 'extra'])
    return JsonResponse({"data": page_content})


def api_doc(request):
    return render(request, 'API_Test/api_doc.html')


def api_debug(request):

    return render(request, 'API_Test/api_debug.html')


def api_manage(request):
    return render(request, 'API_Test/api_manage.html')


def group_form(request):
        return render(request, 'API_Test/group_form.html')


def nodes_query(request):
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


def group_add(request):
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


def group_query(request):
    if request.method == 'GET':
        sql = "SELECT * FROM api_group"
        for key in request.GET:
            value = str_clean(request.GET.get(key))
            if value is not None and value != '':
                sql += " WHERE %s = '%s'" % (key, value)
        data = MySQLEngine().my_execute("query", sql)
        res = {"data": data}
        return JsonResponse(res)


def group_update(request):
    if request.method == 'POST':
        sql = "UPDATE api_group SET "
        for key in request.POST:
            value = str_clean(request.POST.get(key))
            if key in ['group_name'] and value == '':
                return HttpResponse(key)
            elif value == '':
                sql += "%s=null," % key
            else:
                sql += "%s='%s'," % (key, value)
        sql = sql[:-1] + " WHERE id=%s" % request.POST.get('id')  # 先去掉最后的逗号，再拼接where
        res = MySQLEngine().my_execute('update', sql)
        return JsonResponse(res)


def group_del(request):
    if request.method == 'POST':
        sql = "DELETE FROM api_group WHERE "
        for key in request.POST:
            value = str_clean(request.POST.get(key))
            if value != '':
                sql += "%s = '%s'" % (key, value)
        res = MySQLEngine().my_execute('delete', sql)
        return JsonResponse(res)


def api_form(request):
    return render(request, 'API_Test/api_form.html')



def api_add(request):
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


def api_query(request):
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


def api_del(request):
    if request.method == 'POST':
        sql = "DELETE FROM api WHERE "
        for key in request.POST:
            value = str_clean(request.POST.get(key))
            if value != '':
                sql += "%s = '%s'" % (key, value)
        res = MySQLEngine().my_execute('delete', sql)
        print(res)
        return JsonResponse(res)

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
