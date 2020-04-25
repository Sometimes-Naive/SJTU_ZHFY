#coding: utf-8
"""CourtDataVisualization overview module View Configuration

在此文件中定义模块中所有展示页面的视图，并将视图中所需要的
数据（context）打包进相应的模板文件（template）。
"""
from django.http import HttpResponse
from django.shortcuts import render
from . import managers


def index(request):

    manager = managers.DataManager()
    context = {
        'case_outline': manager.assemble_case_statistics(),
        'case_evaluation': managers.compose_case_details(),
        'CATE': '总体'
    }
    # print(context)
    return render(request,'overview/index.html',context)