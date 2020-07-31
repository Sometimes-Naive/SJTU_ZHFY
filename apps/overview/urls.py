#coding: utf-8
"""CourtDataVisualization overview module URL Configuration

在此文件中配置当前模块中的所有视图（views）对应的URL路径
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('overall', views.show_overall_scope, name='overall'),
    path('civil', views.show_civil_scope, name='civil'),
    path('criminal', views.show_criminal_scope, name='criminal'),
    path('administrative', views.show_administrative_scope, name='administrative'),
    path('detail/<str:case_id>', views.show_case_details, name='detail'),
    path('ajax_add/', views.ajax_add, name='ajax_add'),
<<<<<<< HEAD
    path('civil_case_situation', views.show_civil_case_situation_scope, name='civil_case_situation'),
    path('criminal_case_situation', views.show_criminal_case_situation_scope, name='criminal_case_situation'),
    path('administrative_case_situation', views.show_administrative_case_situation_scope, name='administrative_case_situation'),


=======
>>>>>>> c6581c444fdcd55f1f18e304eb79e0c0089944fb
]
