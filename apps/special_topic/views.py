#coding: utf-8
"""CourtDataVisualization special topic module View Configuration

在此文件中定义模块中所有展示页面的视图，并将视图中所需要的
数据（context）打包进相应的模板文件（template）。
"""
from django.http import HttpResponse
from django.shortcuts import render
from .temp_data import*
from . import loaders


def show_civil_divorce_dispute(request):

    context={
        'ay_info': ay_info,
        'overview_data': overview_data_divorce_dispute,
        'person_info': person_info_divorce_dispute,
        'analysis': analysis_divorce_dispute,
    }
    return render(request, 'special_topic/divorce_dispute.html',context)

def show_civil_loan_dispute(request):

    context={
        'ay_info': ay_info,
        'overview_data': overview_data_loan_dispute,
        'person_info': person_info_loan_dispute,
        'analysis': analysis_loan_dispute,
    }
    return render(request, 'special_topic/loan_dispute.html',context)

def show_civil_labor_dispute(request):
    context = {
        'ay_info': ay_info,
        'overview_data': overview_data_labor_dispute,
        'person_info': person_info_labor_dispute,
        'analysis': analysis_labor_dispute,
    }
    return render(request, 'special_topic/labor_dispute.html', context)

def show_civil_product_dispute(request):
    context = {
        'ay_info': ay_info,
        'overview_data': overview_data_product_dispute,
        'person_info': person_info_product_dispute,
        'analysis': analysis_product_dispute,
    }
    return render(request, 'special_topic/product_dispute.html', context)

def show_civil_inherit_dispute(request):
    context = {
        'ay_info': ay_info,
        'overview_data': overview_data_inherit_dispute,
        'person_info': person_info_inherit_dispute,
        'analysis': analysis_inherit_dispute,
    }
    return render(request, 'special_topic/inherit_dispute.html', context)

def show_criminal_dangerous_driving(request):

    context = {
        'AY_INFO': AY_info,
        'F_chart_data': F_chart_dangerous_driving_data,
        'S_chart_data': S_chart_dangerous_driving_data,
        'T_chart_data': T_chart_dangerous_driving_data,
    }
    return render(request, 'special_topic/dangerous_driving.html',context)

def show_criminal_theft(request):

    context = {
        'AY_INFO': AY_info,
        'F_chart_data': F_chart_theft_data,
        'S_chart_data': S_chart_theft_data,
        'T_chart_data': T_chart_theft_data,
    }
    return render(request, 'special_topic/theft.html',context)

def show_criminal_drug_trafficking(request):

    context = {
        'AY_INFO': AY_info,
        'F_chart_data': F_chart_drug_trafficking_data,
        'S_chart_data': S_chart_drug_trafficking_data,
        'T_chart_data': T_chart_drug_trafficking_data,
    }
    return render(request, 'special_topic/drug_trafficking.html',context)

