#coding: utf-8
"""CourtDataVisualization situation assessment module View Configuration

在此文件中定义模块中所有展示页面的视图，并将视图中所需要的
数据（context）打包进相应的模板文件（template）。



案后监督那一块数据没有 对应managers里面  XXgl_region, XXgl_score = [0,0]
"""
from django.http import HttpResponse
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

def show_index(request):

    context = {
        'range_data': [
            {
                'name': '总质效排名',
                'region': zzx_region,
                'score': zzx_score,
            },
            {
                'name': '立案管理排名',
                'region': lagl_region,
                'score': lagl_score,
            },
            {
                'name': '审判办理排名',
                'region': spbl_region,
                'score': spbl_score,
            },
            {
                'name': '结案管理排名',
                'region': jagl_region,
                'score': jagl_score,
            },
            {
                'name': 'XX管理排名',
                'region': XXgl_region,
                'score': XXgl_score,
            },

        ],
        'map': map_data,
        'pie_data': [
            {
                'name': '立案数量',
                'data': lasl_data,
            },
            {
                'name': '一审效果指数',
                'data': yszs_data,
            },
            {
                'name': '结案与执行指数',
                'data': jazx_data,
            },
        ],
        'histogram_data': [ysxg_hdata, jazx_hdata],
        'rank_data': overall_rank,
        'line_data': overall_trend,
        'map_data': heatmap_data,
        'hist_data': indicator_trend,
        'pccl_data': pccl_score,
        'htzx_data': htzx_score,
        'spider_data': spidermap_data,
        'diff_data': diff_data,
    }
    return render(request, 'situation-assessment/index.html', context)

def get_index_system_tree(request):
    return json_data_r(DATA_PATH + 'tree.json')


from django.template.defaulttags import register
@register.filter
def get_dict(my_dict, key):
    return my_dict.get(key)

@register.filter
def get_list(my_list, index):
    return my_list[index]
