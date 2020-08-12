#coding: utf-8
"""CourtDataVisualization situation assessment module URL Configuration

在此文件中配置当前模块中的所有视图（views）对应的URL路径
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('assessment', views.show_assessment_scope, name='situation_assessment.assessment'),
    path('index-system-tree', views.get_index_system_tree, name='tree'),
    # path('index', views.show_index, name='situation_assessment.index'),
    path('bussiness-environment', views.get_bussiness_environment_scope, name='situation_assessment.bussiness'),
    path('indicator-relationship', views.get_indicator_relationship_scope, name='situation_assessment.indicator'),
]
