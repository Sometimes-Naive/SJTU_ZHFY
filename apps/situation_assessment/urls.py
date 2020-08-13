#coding: utf-8
"""CourtDataVisualization situation assessment module URL Configuration

在此文件中配置当前模块中的所有视图（views）对应的URL路径
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('indicator-description', views.get_indicator_description_scope, name='situation_assessment.description'),
    path('indicator-application', views.get_indicator_application_scope, name='situation_assessment.application'),
    path('index-system-tree', views.get_index_system_tree, name='situation_assessment.tree'),

    path('bussiness-environment', views.get_bussiness_environment_scope, name='situation_assessment.bussiness'),
    path('indicator-relationship', views.get_indicator_relationship_scope, name='situation_assessment.relationship'),
]
