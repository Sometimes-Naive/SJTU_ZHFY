#coding: utf-8
"""CourtDataVisualization situation prediction module URL Configuration

在此文件中配置当前模块中的所有视图（views）对应的URL路径
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('receive-close-prediction', views.show_receive_and_close_case_prediction, name='receive_close_prediction'),
]
