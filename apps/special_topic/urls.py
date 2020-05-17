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

    path('civil/', include([
        path('loan_dispute/', views.show_civil_loan_dispute, name='loan_dispute')
    ])),

    path('civil/', include([
        path('labor_dispute/', views.show_civil_labor_dispute, name='labor_dispute')
    ])),

    path('civil/', include([
        path('product_dispute/', views.show_civil_product_dispute, name='product_dispute')
    ])),

    path('civil/', include([
        path('inherit_dispute/', views.show_civil_inherit_dispute, name='inherit_dispute')
    ])),

    path('criminal/', include([
        path('dangerous-driving/', views.show_criminal_dangerous_driving, name='dangerous_driving')
    ])),

    path('criminal/', include([
        path('theft/', views.show_criminal_theft, name='theft')
    ])),

    path('criminal/', include([
        path('drug_trafficking/', views.show_criminal_drug_trafficking, name='drug_trafficking')
    ]))
]
