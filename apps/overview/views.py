#coding: utf-8
"""CourtDataVisualization overview module View Configuration

在此文件中定义模块中所有展示页面的视图，并将视图中所需要的
数据（context）打包进相应的模板文件（template）。
"""
from django.http import HttpResponse
from django.shortcuts import render
from . import managers
from . import loaders
import json

def show_overall_scope(request):

    loader = loaders.ResultLoader()
    context = {
        'case_outline': loader.load_case_basic_result('overall'),
        'case_evaluation': loader.load_case_evaluation_title('overall'),
    }
    # print(context)
    return render(request,'overview/overall.html', context)

def show_civil_scope(request):

    loader = loaders.ResultLoader()
    context = {
        'case_outline': [
            loader.load_case_basic_result('civil'),
            loader.load_case_cause_result('civil')[0],
            loader.load_case_cause_result('civil')[1]
        ],
        'case_evaluation': loader.load_case_evaluation_title('civil'),
        'case_cause': loader.load_case_evaluation_title('civil')['key_list'],
    }
    return render(request, 'overview/civil.html', context)

def show_criminal_scope(request):

    loader = loaders.ResultLoader()
    context = {
        'case_outline': [
            loader.load_case_basic_result('criminal'),
            loader.load_case_cause_result('criminal')[0],
            loader.load_case_cause_result('criminal')[1]
        ],
        'case_evaluation': loader.load_case_evaluation_title('criminal'),
        'case_cause': loader.load_case_evaluation_title('criminal')['key_list'],
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

def ajax_add(request):
    # print(request)
    loader = loaders.ResultLoader()
    tag = request.POST.get("dropdown")
    tag_ok = tag.split('\n')[3].replace(' ','')
    cate = tag.split('\n')[0]
    cate_ok = ''
    if cate == '刑事案由':
        cate_ok = 'criminal'
    elif cate == '民事案由':
        cate_ok = 'civil'
    elif cate == '行政案由':
        cate_ok = 'administrative'
    test_data = json.dumps(loader.load_case_evaluation_title(cate_ok)[tag_ok])
    # print(test_data)
    return HttpResponse(test_data)



from django.template.defaulttags import register
@register.filter
def get_dict(my_dict, key):
    return my_dict.get(key)

@register.filter
def get_list(my_list, index):
    return my_list[index]
