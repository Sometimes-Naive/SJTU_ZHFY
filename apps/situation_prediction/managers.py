#coding: utf-8
"""CourtDataVisualization situation prediction module data manager

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
import time
import pandas as pd
import numpy as np
import xlrd
import statsmodels.api as sm

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

    sa_number = []
    ja_number = []
    region = []
    judge_number = []
    feature = []


    #处理表格文件数据得到收结案和地区信息，收结案可以看做矩阵
    def __init__(self): 
        
        for i in range(1, 10):
            url = XLSX_PATH + 'df0' + str(i) + '.xlsx'
            excel = xlrd.open_workbook(url)
            sheet = excel.sheet_by_name('Sheet1')
            sa_data = sheet.col_values(3, 1)
            ja_data = sheet.col_values(2, 1)
            self.sa_number.append(sa_data)
            self.ja_number.append(ja_data) 
            
        for i in range(10, 41):
            url = XLSX_PATH + 'df' + str(i) + '.xlsx'
            excel = xlrd.open_workbook(url)
            sheet = excel.sheet_by_name('Sheet1')
            sa_data = sheet.col_values(3, 1)
            ja_data = sheet.col_values(2, 1)
            self.sa_number.append(sa_data)
            self.ja_number.append(ja_data)
        self.region = sheet.col_values(1, 1)
        self.region = [x + '区' for x in self.region]
        self.judge_number = sheet.col_values(4, 1)
        for i in range(6, 9):
            f_data = sheet.col_values(i, 1)
            self.feature.append(f_data)

    
    #得到地图数据,show sa_number and ja_number of every region at last month
    def get_map_data(self):

        map_key = json_data_r(DATA_PATH + '/map_key')

        map_data = []
        for i in range(len(self.region)):
            map_meta_data = {}
            key = process.extractOne(self.region[i].split('区')[0], map_key)
            key_ok = key[0]
            map_meta_data['name'] = key_ok
            # map_meta_data['value'] = []
            map_meta_data['value'] = (self.sa_number[39][i])
            # map_meta_data['value'].append(self.ja_number[39][i])
            map_data.append(map_meta_data)

        return map_data
 
    
#get sa_number and ja_number of every region at last month
    def get_his_case_data(self):       

        his_sa_data = []
        for i in range(len(self.region)):
#            his_meta_data = {}
#            his_meta_data['name'] = self.region[i]
#            his_meta_data['data'] = self.sa_number[39][i]
            his_meta_data = []
            his_meta_data.append(self.region[i])
            his_meta_data.append(self.sa_number[39][i])
            his_sa_data.append(his_meta_data)
            inverse_sa_number = [-l for l in self.sa_number[39]]

        return his_sa_data, inverse_sa_number[0: 10], self.ja_number[39][0: 10]


    #get three judicial features of every region at last month
    def get_his_feature_data(self):
        
        feature_name = ['撤诉结案数', '调节结案数', '法定期限内结案数']
        his_data = []
        
        for i in range(len(feature_name)):
            his_meta_data = {}
            his_meta_data['name'] = feature_name[i]
            #his_meta_data['value'] = []
            #for j in range(len(self.region)):
            his_meta_data['data'] = self.feature[i]
            his_data.append(his_meta_data)
        
        return his_data

    
    #40 months sa_number and ja_number grouped by 28 regions, draw the line chart 
    def get_line_data(self):
                
        chart_date = [
            '2016-01', '2016-02', '2016-03', '2016-04',
            '2016-05', '2016-06', '2016-07', '2016-08',
            '2016-09', '2016-10', '2016-11', '2016-12',
            '2017-01', '2017-02', '2017-03', '2017-04',
            '2017-05', '2017-06', '2017-07', '2017-08',
            '2017-09', '2017-10', '2017-11', '2017-12',
            '2018-01', '2018-02', '2018-03', '2018-04',
            '2018-05', '2018-06', '2018-07', '2018-08',
            '2018-09', '2018-10', '2018-11', '2018-12',
            '2019-01', '2019-02', '2019-03', '2019-04'
        ]
        line_data = []
        
        for i in range(len(self.region)):
            line_meta_data = {}
            line_sa_number = []
            line_ja_number = []
            for j in range(len(self.sa_number)):
                line_sa_number.append(self.sa_number[j][i])
                line_ja_number.append(self.ja_number[j][i])
            line_meta_data['region'] = self.region[i]
            line_meta_data['chart_date'] = chart_date
            line_meta_data['chart_sa_number'] = line_sa_number
            line_meta_data['chart_ja_number'] = line_ja_number
            line_data.append(line_meta_data)
            
        return line_data

    def line_data_new(self, line_data):
        date_key_list = line_data[0]['chart_date']
        case_sa_number_dict = []
        case_ja_number_dict = []
        sa_data = []
        ja_data = []
        for i in range(7):
            data = line_data[i]
            case_sa_number_meta_dict = {}
            case_sa_number_meta_dict['name'] = data['region']
            case_sa_number_meta_dict['data'] = data['chart_sa_number']
            case_ja_number_meta_dict = {}
            case_ja_number_meta_dict['name'] = data['region']
            case_ja_number_meta_dict['data'] = data['chart_ja_number']
            case_sa_number_dict.append(case_sa_number_meta_dict)
            case_ja_number_dict.append(case_ja_number_meta_dict)

        sa_data.append(date_key_list)
        sa_data.append(case_sa_number_dict)
        ja_data.append(date_key_list)
        ja_data.append(case_ja_number_dict)
        return [sa_data, ja_data]
    
    #judge_number and its percentage of every region at last month
    def get_pie_data(self):
        
        pie_data = []
        judge_sum = 0
        
        for i in range(28):
            judge_sum += self.judge_number[i]
            
        for i in range(len(self.region)):
            pie_meta_data = {}
            pie_meta_data['name'] = self.region[i]
            # pie_meta_data['value'] = []
            pie_meta_data['y'] = self.judge_number[i]
            pie_meta_data['z'] = self.judge_number[i]/judge_sum
            pie_data.append(pie_meta_data)
        
        return pie_data
        

    #predict sa_number of next month and give corresponding advice
    def prediction(self):

        chart_date = [
            '2016-01', '2016-02', '2016-03', '2016-04',
            '2016-05', '2016-06', '2016-07', '2016-08',
            '2016-09', '2016-10', '2016-11', '2016-12',
            '2017-01', '2017-02', '2017-03', '2017-04',
            '2017-05', '2017-06', '2017-07', '2017-08',
            '2017-09', '2017-10', '2017-11', '2017-12',
            '2018-01', '2018-02', '2018-03', '2018-04',
            '2018-05', '2018-06', '2018-07', '2018-08',
            '2018-09', '2018-10', '2018-11', '2018-12',
            '2019-01', '2019-02', '2019-03', '2019-04', '2019-05'
        ]
        line_data = []
        #sa_predictions = []
        advice_set = ['预测未来收案数量较上个月会出现一个较大增幅，会出现法院在人力资源配置方面案件剧增与人员缓增的矛盾，需要对内部资源进行科学合理分配', 
                      '预测未来收案数量较上个月增幅较小，可视当地司法资源和公共管理水平进行灵活调整', 
                      '预测未来收案数量不会超过上个月的案件处理水平，司法资源配置充足']
        advice = []
        
        for i in range(len(self.region)):
            line_meta_data = {}
            line_sa_number = []
            for j in range(len(self.sa_number)):
                line_sa_number.append(self.sa_number[j][i])
            line_meta_data['region'] = self.region[i]
            line_meta_data['chart_date'] = chart_date
            line_meta_data['chart_sa_number'] = line_sa_number
            line_data.append(line_meta_data) 
        
        for i in range(len(self.region)):
            model = sm.tsa.AR(line_data[i]['chart_sa_number'])
            model_fit = model.fit()
            predictions = model_fit.predict(start=len(line_data[i]['chart_sa_number']), end=len(line_data[i]['chart_sa_number']), dynamic=False)
            #sa_predictions.append(predictions)
            line_data[i]['chart_sa_number'].append(predictions[0])
            if predictions[0] > (line_data[i]['chart_sa_number'][39] + 1000) :
                advice.append(advice_set[0])
            else:
                if predictions[0] > line_data[i]['chart_sa_number'][39] :
                    advice.append(advice_set[1])
                else:
                    advice.append(advice_set[2])
        
        return line_data, advice

    def test(self):
        data = {
            'region':[],
            'line_data':[]
        }
        for i in sa_predictions:
            data['region'].append(i['region'])
            data_list = []
            for j in range(len(i['chart_date'])):
                data_meta = []
                time1 = int(time.mktime(time.strptime(i['chart_date'][j],"%Y-%m")))*1000
                data_meta.append(time1)
                data_meta.append(i['chart_sa_number'][j])
                data_list.append(data_meta)
            data['line_data'].append(data_list)
            # print(data)

        return data

#test all the modules
real_chart = DataProcessManager()
region = real_chart.region
sjayc_map_data = real_chart.get_map_data()
line_data_pre = real_chart.get_line_data()
line_data = real_chart.line_data_new(line_data_pre)
his_data1, his_sa, his_ja = real_chart.get_his_case_data()
his_data2 = real_chart.get_his_feature_data()
region_part = region[0: 10]
pie_data = real_chart.get_pie_data()
sa_predictions, advice = real_chart.prediction()
test = real_chart.test()
