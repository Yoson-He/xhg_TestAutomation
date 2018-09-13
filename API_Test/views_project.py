import json

from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from common.common import str_clean
from django.views.decorators.csrf import csrf_exempt

from common.db_handler.mysql_engine import MySQLEngine

# Create your views here.


def project_manage(request):
    #if request.session.session_key:
    #   return render(request, 'API_Test/project_manage.html')
    #else:
    #    return HttpResponseRedirect('/')
    return render(request, 'API_Test/project_manage.html')


def project_form(request):
    return render(request, 'API_Test/project_form.html')


def project_query(request):
    if request.method == 'GET':
            project_name = request.GET.get('project_name')
            sql = "SELECT * FROM project"
            if project_name is not None and project_name != '':
                sql += " WHERE project_name = '%s'" % project_name
            data = MySQLEngine().my_execute("query", sql)
            res = {"data": data}
            return JsonResponse(res)


def project_update(request):
    if request.method == 'POST':
            sql = "UPDATE project SET "
            for key in request.POST:
                value = str_clean(request.POST.get(key))
                if key in ['project_name'] and value == '':
                    return HttpResponse(key)
                else:
                    sql += "%s='%s'," % (key, value)
            sql = sql[:-1] + " WHERE id=%s" % request.POST.get('id')  # 先去掉最后的逗号，再拼接where
            res = MySQLEngine().my_execute('update', sql)
            return JsonResponse(res)


def project_add(request):
    if request.method == 'POST':
            sql = "INSERT INTO project("
            sql_values = ') VALUES( '
            for key in request.POST:
                value = str_clean(request.POST.get(key))
                if value != '':
                    sql += "%s," % key
                    sql_values += "'%s'," % value
                elif key in ['project_name']:
                    return HttpResponse(key)
            sql = sql[:-1] + sql_values[:-1] +")"  # 先去掉最后的逗号，再拼接
            res = MySQLEngine().my_execute('insert', sql)
            return JsonResponse(res)


def project_del(request):
    if request.method == 'POST':
            sql = "DELETE FROM project WHERE "
            for key in request.POST:
                value = str_clean(request.POST.get(key))
                if value != '':
                    sql += "%s = '%s'" % (key, value)
            res = MySQLEngine().my_execute('delete', sql)
            return JsonResponse(res)
