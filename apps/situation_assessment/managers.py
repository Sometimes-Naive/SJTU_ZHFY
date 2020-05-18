#coding: utf-8
"""CourtDataVisualization situation assessment module data manager

在此文件中定义模块中数据的处理业务逻辑，是整个模块的功能核心所在。
在视图页面需要的数据通过调用本文件中的函数获取，也可以将处理后的结果存入文件使用loaders读取；
同时本文件负责从模型（models）中利用drivers获取原始数据。

可以直接定义数据处理函数，再遇到复杂逻辑时建议定义Manager类统筹管理。
定义类时需要注意访问控制，同时为保证每一个函数的易读性，每个函数长度不超过30行。

**************************************************************************
主要变动：
1、将mongoengine链接包装成了装饰器，使用时在需要访问数据库的函数上使用即可；
2、将整个处理逻辑分为 预处理、 处理、 加载 三个部分，加载部分逻辑挪到loaders.py文件中处理；
3、类与函数中常量、变量的命名，保存处理结果的文件名等进行了重命名，相关常量统一放进constants.py；

todos：
页面中在总览与三种案件四个页面切换的超链接按钮失灵；
页面下方显示案件标题常有串行混淆，其html结构需要优化；

运行数据预处理与处理命令：python manage.py schedule
具体可参照 ./management/commands/schedule.py

为了便于调试，有两处限制了处理的数据量，请查找“用于测试”；

由于缺少行政案件案由文档，行政案件案由使用旧数据。
2020.05.03 by stein
**************************************************************************
"""

import re
import os
import copy
import xlrd
import pandas as pd
from fuzzywuzzy import process

from .models import *
from .temp_data import *
from .utils import *
from .constants import * 
from core.drivers import connect_mongo

@connect_mongo('court')
def compose_case_details(id):
    case_info = AllData.objects(id=id)

    case = {
        'id':[],
        'title':[],
        'category':[],
        'personnel':[],
        'header':[],
        'trial':[],
        'judgement':[],

    }
    for i in case_info:
        case['id'] = (str(i.id))
        case['title'] = (i.头部信息[0].split('-')[0])
        # print(i.头部信息[0])=
        case['category'] = info2str(i.案件类别)
        case['header'] = info2str(i.头部信息[1:])
        case['personnel'] = info2str(i.人员信息)
        case['trial'] = info2str(i.案件过程)
        case['judgement'] = info2str(i.判决信息)
    return case


class DataProcessManager(object):

    def __init__(self, name, url):
        self.name = name
        self.url = url

    #得到地区的排名信息，输入需要得到的排名名称
    def get_region_score(self):
        #立案管理排名，审判办理排名，结案管理排名
        data = xlrd.open_workbook(self.url)
        table = data.sheet_by_name(self.name)
        region = table.col_values(0,1)
        score = table.col_values(2,1)
        region = [x+'区' for x in region]
        score = {
            'name': self.name,
            'data': score,
        }
        return region, score

    #得到总的排名，由于展示地区进行数量限制，单写一个函数
    def get_region_score1(self):
        #总排名
        data = xlrd.open_workbook(self.url)
        table = data.sheet_by_name(self.name)
        region = table.col_values(0,1,8)
        score = table.col_values(2,1,8)
        score = [float(format(x, '.3f')) for x in score]
        region = [x+'区' for x in region]
        score = {
            'name': self.name,
            'data': score,
        }
        return region, score

    #得到地图排名数据，数据格式[{'name':$$$, 'value':%% },{},{}]
    def get_map_data(self):
        map_data = []

        data = xlrd.open_workbook(self.url)
        table = data.sheet_by_name(self.name)
        region = table.col_values(0, 1)
        score = table.col_values(2, 1)
        score = [float(format(x, '.3f')) for x in score]
        for i in range(len(region)):
            map_meta_data = {}
            map_meta_data['name'] = region[i] + '区'
            map_meta_data['value'] = score[i]
            map_data.append(map_meta_data)
        return map_data

    #得到饼状图数据
    def get_pie_data(self):
        name = self.name
        pie_data = []
        data = xlrd.open_workbook(self.url)
        table = data.sheet_by_name(name)
        region = table.col_values(0, 2)
        score = table.col_values(7, 2)
        for i in range(len(region)):
            pie_meta_data = {}
            pie_meta_data['name'] = region[i] + '区'
            pie_meta_data['y'] = score[i]
            pie_data.append(pie_meta_data)
        return pie_data

    #得到柱状图数据，输入为指标在数据表的位置和图表名称
    def get_his_data(self, start, end, his_name):
        pie_data = []
        data = xlrd.open_workbook(self.url)
        table = data.sheet_by_name(self.name)
        region = table.col_values(0, 2)
        index = []
        for i in range(start, end+1):
            index.append(table.col_values(i))
        region = [x + '区' for x in region]
        h_data = []
        for i in index:
            h_meta_data = {}
            meta_data = {}
            h_meta_data['name'] = i[0]
            meta_data['name'] = i[0]
            meta_data['y'] = i[1]
            i[2:] = [float(format(x, '.3f')) for x in i[2:]]
            h_meta_data['data'] = i[2:]
            h_data.append(h_meta_data)
            pie_data.append(meta_data)
        hdata = {
            'name': his_name,
            'region': region,
            'data': h_data,
        }
        return hdata, pie_data


#排名数据
url_result = DATA_PATH + 'result.xls'
url_data = DATA_PATH + 'data.xls'
zzx_region, zzx_score = DataProcessManager('总排名', url_result).get_region_score1()
lagl_region, lagl_score = DataProcessManager('立案管理排名', url_result).get_region_score()
spbl_region, spbl_score = DataProcessManager('审判办理排名', url_result).get_region_score()
jagl_region, jagl_score = DataProcessManager('结案管理排名', url_result).get_region_score()
XXgl_region, XXgl_score = [0,0]
map_data = DataProcessManager('总排名', url_result).get_map_data()
#饼图数据
lasl_data = DataProcessManager('全部地区', url_data).get_pie_data()
#柱状图数据
ysxg_hdata, yszs_data = DataProcessManager('全部地区', url_data).get_his_data(14, 15, '一审效果指数')
jazx_hdata, jazx_data = DataProcessManager('全部地区', url_data).get_his_data(21, 24, '结案与执行指数')
