#coding: utf-8
"""CourtDataVisualization special topic module View Configuration

在此文件中定义模块中所有展示页面的视图，并将视图中所需要的
数据（context）打包进相应的模板文件（template）。
"""
from django.http import HttpResponse
from django.shortcuts import render
from . import loaders


# def index(request):

#     manager = managers.DataManager()
#     context = {
#         'case_outline': manager.assemble_case_statistics(),
#         'case_evaluation': managers.compose_case_details(),
#         'CATE': '总体'
#     }
#     # print(context)
#     return render(request,'overview/index.html',context)


def show_civil_divorce_dispute(request):

    loader = loaders.ResultLoader()
    context={
        'msay_info': '',
        'quantity': loader.load_quantity_result('civil', 'divorce_dispute'),
        'party': loader.load_party_result('civil', 'divorce_dispute'),
        'topic': loader.load_topic_result('civil', 'divorce_dispute'),
    }
    return render(request, 'special_topic/divorce_dispute.html',context)


def show_criminal_dangerous_driving(request):

    loader = loaders.ResultLoader()
    context = {
        'AY_INFO': '',
        'quantity': loader.load_quantity_result('criminal', 'dangerous_driving'),
        'accused': loader.load_party_result('criminal', 'dangerous_driving'),
        'topic': loader.load_topic_result('criminal', 'dangerous_driving'),
    }
    return render(request, 'special_topic/dangerous_driving.html',context)