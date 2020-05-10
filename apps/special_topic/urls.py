#coding: utf-8
"""CourtDataVisualization special topic module URL Configuration

在此文件中配置当前模块中的所有视图（views）对应的URL路径
"""
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('civil/', include([
        path('divorce-dispute/', views.show_civil_divorce_dispute, name='divorce_dispute')
    ])),

    path('criminal/', include([
        path('dangerous-driving/', views.show_criminal_dangerous_driving, name='dangerous_driving')
    ]))
]
