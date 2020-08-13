#coding: utf-8
"""CourtDataVisualization situation assessment module URL Configuration

在此文件中配置当前模块中的所有视图（views）对应的URL路径
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('index-app', views.index_app, name='situation_assessment.index-app'),
    path('index-system-tree', views.get_index_system_tree, name='tree'),
    path('index-pre', views.index_pre, name='situation_assessment.index-pre'),
    path('yshj', views.yshj1, name='situation_assessment.yshj'),
    path('yshj2', views.yshj2, name='situation_assessment.yshj2')
]
