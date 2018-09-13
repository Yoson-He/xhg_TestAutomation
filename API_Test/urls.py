# -*- coding: utf-8 -*-
# @Time    : 2018/2/2 10:04
# @Author  : Yoson
# @File    : url.py
# @Software: PyCharm

from django.urls import path
from API_Test import views_project,views_territory,views_api

urlpatterns = [
    # ---项目---- #
    path('project/', views_project.project_manage, name='project_manage'),
    path('project_add_form/', views_project.project_form, name='project_form'),
    path('project_query/', views_project.project_query, name='project_query'),
    path('project_update/', views_project.project_update, name='project_update'),
    path('project_add/', views_project.project_add, name='project_add'),
    path('project_del/', views_project.project_del, name='project_del'),

    # ---环境---- #
    path('territory_manage/', views_territory.territory_manage, name='territory_manage'),
    path('territory_form/', views_territory.territory_form, name='territory_form'),
    path('territory_add/', views_territory.territory_add, name='territory_add'),
    path('territory_update/', views_territory.territory_update, name='territory_update'),
    path('territory_query/', views_territory.territory_query, name='territory_query'),
    path('territory_del/', views_territory.territory_del, name='territory_del'),

    # ---接口---- #
    path('api_manage/', views_api.api_manage, name='api_manage'),
    path('api_doc/', views_api.api_doc, name='api_doc'),
    path('api_debug/', views_api.api_doc, name='api_doc'),
    path('nodes/', views_api.get_nodes, name='nodes'),
    path('api_form/', views_api.api_debug, name='api_debug'),
    path('api_add/', views_api.api_add, name='api_add'),
    #path('api_update/', views_api.api_update, name='api_update'),
    path('api_query/', views_api.api_query, name='api_query'),
    path('api_del/', views_api.api_del, name='api_del'),
    path('group_form/', views_api.group_form, name='group_form'),
    path('nodes_query/', views_api.nodes_query, name='nodes_query'),
    path('group_add/', views_api.group_add, name='group_add'),
    path('group_query/', views_api.group_query, name='group_query'),
    path('group_update/', views_api.group_update, name='group_update'),
    path('group_del/', views_api.group_del, name='group_del'),

]
