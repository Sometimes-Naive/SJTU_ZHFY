#coding: utf-8
"""CourtDataVisualization overview module View Configuration

在此文件中定义模块中所有展示页面的视图，并将视图中所需要的
数据（context）打包进相应的模板文件（template）。
"""
from django.http import HttpResponse
from django.shortcuts import render
from . import managers
from . import loaders

def show_overall_scope(request):

    loader = loaders.ResultLoader()
    context = {
        'case_outline': loader.load_case_basic_result('overall'),
        'case_evaluation': loader.load_case_evaluation_title('overall'),
    }
    print(context)
    return render(request,'overview/overall.html', context)

def show_civil_scope(request):

    loader = loaders.ResultLoader()
    context = {
        'case_outline': [
            loader.load_case_basic_result('civil'),
            loader.load_case_cause_result('civil')
        ],
        'case_evaluation': loader.load_case_evaluation_title('civil'),
    }
    return render(request, 'overview/civil.html', context)

def show_criminal_scope(request):

    loader = loaders.ResultLoader()
    context = {
        'case_outline': [
            loader.load_case_basic_result('criminal'),
            loader.load_case_cause_result('criminal')
        ],
        'case_evaluation': loader.load_case_evaluation_title('criminal'),
    }
    return render(request, 'overview/criminal.html', context)

def show_administrative_scope(request):

    loader = loaders.ResultLoader()
    context = {
        'case_outline': [
            loader.load_case_basic_result('administrative'),
            loader.load_case_cause_result('administrative')
        ],
        'case_evaluation': loader.load_case_evaluation_title('administrative'),
    }
    return render(request, 'overview/administrative.html', context)

def show_case_details(request, case_id):

    return render(request,'overview/detail.html', {
        'details': managers.compose_case_details(case_id)
    })




from django.template.defaulttags import register
@register.filter
def get_dict(my_dict, key):
    return my_dict.get(key)

@register.filter
def get_list(my_list, index):
    return my_list[index]
