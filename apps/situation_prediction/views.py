#coding: utf-8
"""CourtDataVisualization situation prediction module View Configuration

在此文件中定义模块中所有展示页面的视图，并将视图中所需要的
数据（context）打包进相应的模板文件（template）。



案后监督那一块数据没有 对应managers里面  XXgl_region, XXgl_score = [0,0]
"""
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from . import managers
from . import loaders
from .temp_data import *
from .managers import *
from .utils import json_data_r
import json

# def show_overall_scope(request):

#     loader = loaders.ResultLoader()
#     context = {
#         'case_outline': loader.load_case_basic_result('overall'),
#         'case_evaluation': loader.load_case_evaluation_title('overall'),
#     }
#     # print(context)
#     return render(request,'overview/overall.html', context)

# def show_civil_scope(request):

#     loader = loaders.ResultLoader()
#     context = {
#         'case_outline': [
#             loader.load_case_basic_result('civil'),
#             loader.load_case_cause_result('civil')[0],
#             loader.load_case_cause_result('civil')[1]
#         ],
#         'case_evaluation': loader.load_case_evaluation_title('civil'),
#         'case_cause': loader.load_case_evaluation_title('civil')['key_list'],
#     }
#     return render(request, 'overview/civil.html', context)

# def show_criminal_scope(request):

#     loader = loaders.ResultLoader()
#     context = {
#         'case_outline': [
#             loader.load_case_basic_result('criminal'),
#             loader.load_case_cause_result('criminal')[0],
#             loader.load_case_cause_result('criminal')[1]
#         ],
#         'case_evaluation': loader.load_case_evaluation_title('criminal'),
#         'case_cause': loader.load_case_evaluation_title('criminal')['key_list'],
#     }
#     return render(request, 'overview/criminal.html', context)

# def show_administrative_scope(request):

#     loader = loaders.ResultLoader()
#     context = {
#         'case_outline': [
#             loader.load_case_basic_result('administrative'),
#             loader.load_case_cause_result('administrative')
#         ],
#         'case_evaluation': loader.load_case_evaluation_title('administrative'),
#     }
#     return render(request, 'overview/administrative.html', context)

# def show_case_details(request, case_id):

#     return render(request,'overview/detail.html', {
#         'details': managers.compose_case_details(case_id)
#     })

    #收结案态势预测模块函数
def show_receive_and_close_case_prediction(request):

    context = {
        #'date_data': date_data,
        #'region_data': region_data,
        'map_data' : sjayc_map_data,
        'line_data' : line_data,
        'his_data1' : his_data1,
        'his_sa' : his_sa, 
        'his_ja' : his_ja,
        'his_data2' : his_data2,
        'pie_data' : pie_data,
        'sa_predictions' : sa_predictions,
        'advice' : advice,
        'test': test,
        'region' : region
    }
    return render(request, 'situation_prediction/receive_close_case.html', context)


from django.template.defaulttags import register
@register.filter
def get_dict(my_dict, key):
    return my_dict.get(key)

@register.filter
def get_list(my_list, index):
    return my_list[index]
