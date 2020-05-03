#coding: utf-8
"""CourtDataVisualization overview module data manager

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

    def __init__(self):
        self._case_info_collection = []


    def run(self):

        for idx in range(0, len(CASE_NAMES)):
            
            self._process_case_info(idx)

            self._process_case_cause_info(10, idx)

            self._process_case_evaluation(idx)

        self._process_overall_statistics(3)

        self._process_case_evaluation(3)
        return self

    @connect_mongo('court')
    def preprocess(self):

        for idx in range(0, len(CASE_NAMES)):
            # 案件数限制到100用于测试
            case = AllData.objects(省份=PROVINCE_ACTIVATED, 案件类别=CASE_NAMES[idx])[:100]
            # 输出直接可用json数据文件为preprocess_*.json
            self._preprocess_case_info(case, idx)
            #输出json文件为preprocess_*_case_cause.json
            self._preprocess_case_cause_info(case, idx)
        return self

    def _process_overall_statistics(self, type):
        # 读取数据
        self._case_info_collection = [
            self._load_case_info('civil'),
            self._load_case_info('criminal'), 
            self._load_case_info('administrative')
        ]

        statistics = {}
        # print(self._case_info_collection)
        pie_data = self._cal_pie_number()
        statistics['pie_case_number'] = pie_data[0]
        statistics['pie_people_number'] = pie_data[1]

        statistics['case_cause_distribution'] = self._cal_case_cause_distribution()
    
        statistics['case_region_number'] = self._cal_case_region_number()
        statistics['map_data'] = self._cal_map_data()

        statistics['case_date_number'] = self._cal_case_date_number()
        json_data_w(statistics, DATA_PATH + FILENAME_LIST[type] + JSON_TYPE_SUFFIX)


    def _load_case_info(self, category):

        return {
            'basic': json_data_r(DATA_PATH + FILENAME_LIST[CATEGORIES[category]] + JSON_TYPE_SUFFIX),
            'case_cause': json_data_r(DATA_PATH + FILENAME_LIST[CATEGORIES[category]] +
                CASE_CAUSE_FILENAME_SUFFIX + JSON_TYPE_SUFFIX)
        }  

    def _cal_pie_number(self):
        pie_data = [[], []]
        for i,info in enumerate(self._case_info_collection):
            pie_data[0].append({
                'name': CASE_NAMES[i],
                'y': info['basic']['case_number']
                })
            pie_data[1].append({
                'name': CASE_NAMES[i],
                'y': info['basic']['people_number']
                })
        return pie_data

    def _cal_case_cause_distribution(self):
        case_cause = []
        for idx, info in enumerate(self._case_info_collection):
            case_cause.append(info['case_cause'])
        return case_cause

    def _cal_case_region_number(self):

        case_info = copy.deepcopy(self._case_info_collection[0]['basic']['case_region_number'])

        for i in range(0, len(case_info[0])):
            if case_info[0][i] in self._case_info_collection[1]['basic']['case_region_number'][0]:
                index = self._case_info_collection[1]['basic']['case_region_number'][0].index(case_info[0][i])
                case_info[1][i] = case_info[1][i] + self._case_info_collection[1]['basic']['case_region_number'][1][index]
            if case_info[0][i] in self._case_info_collection[2]['basic']['case_region_number'][0]:
                index = self._case_info_collection[2]['basic']['case_region_number'][0].index(case_info[0][i])
                case_info[1][i] = case_info[1][i] + self._case_info_collection[2]['basic']['case_region_number'][1][index]
        return case_info

    def _cal_map_data(self):
        map_data_dict = {}
        msmap = list2dict(self._case_info_collection[0]['basic']['map'])
        xsmap = list2dict(self._case_info_collection[1]['basic']['map'])
        xzmap = list2dict(self._case_info_collection[2]['basic']['map'])
        for i in list(msmap.keys()):
            temp_criminal_case_map =  xsmap[i] if xsmap.__contains__(i) else 0
            temp_administrative_case_map = xzmap[i] if xzmap.__contains__(i) else 0
            map_data_dict[i] = msmap[i] + temp_criminal_case_map + temp_administrative_case_map
        map_data = dict2list(map_data_dict)
        return map_data

    def _cal_case_date_number(self):
        date_case_data = copy.deepcopy(self._case_info_collection[0]['basic']['case_date_number'])
        line_data = []
        for i in range(0, len(self._case_info_collection)):
            line_data.append(self._case_info_collection[i]['basic']['case_date_number'][1][0])
        date_case_data[1] = line_data
        return date_case_data


    @connect_mongo('court')
    def _process_case_info(self, type):
        
        # number = AllData.objects(省份=PROVINCE_ACTIVATED, 案件类别=CASE_NAMES[type]).count()
        # 用于测试
        number = 100
        case_map = self._map_data_replace(type)

        case_date_number = self._date_data_replace(type)
        case_info = {
            'case_number': number,
            'people_number': 2 * number,
            'map': case_map['map'],
            'case_region_number': case_map['case_region_number'],
            'case_date_number': case_date_number['case_date_number']
        }
        json_data_w(case_info, DATA_PATH + FILENAME_LIST[type] + JSON_TYPE_SUFFIX)
        return case_info

    def _map_data_replace(self, type):
        #file_name为存储predata的名字，输出存储为原文件名加'_map'，输出为修正地区名之后的地图数据和地区案件数据
        map_key = json_data_r(DATA_PATH + 'map_key')
        case_map = json_data_r(PREPROCESS_DATA_PATH + FILENAME_LIST[type] + JSON_TYPE_SUFFIX)['map']
        map_bak = {}
        for i in case_map.keys():
            map_re = process.extractBests(i, map_key, score_cutoff=60)
            if map_re:
                map_bak[map_re[0][0]] = case_map[i]
        map_data = []
        for i, j in map_bak.items():
            map_data_meta = {}
            map_data_meta['name'] = i
            map_data_meta['value'] = j
            map_data.append(map_data_meta)
        case_map, _ = dict_sorted(case_map, 1, True)
        region_case_number = [list(case_map.keys()), list(case_map.values())]
        case_map_info = {
            'map': map_data,
            'case_region_number': region_case_number
        }
        json_data_w(case_map_info, DATA_PATH + FILENAME_LIST[type] + '_map' + JSON_TYPE_SUFFIX)
        return case_map_info

    def _date_data_replace(self, type):
        date_pre_data = json_data_r(PREPROCESS_DATA_PATH + FILENAME_LIST[type] + JSON_TYPE_SUFFIX)['date_case_number']
        date_data = {}
        for i in list(date_pre_data.keys()):
            date = re.split('年|月|日', i)
            date.pop()
            for j in range(len(date)):
                if len(date[j]) < 2:
                    date[j] = '0' + date[j]
            date = date[0] + '-' + date[1] + '-' + date[2]
            date_pre_data[date] = date_pre_data.pop(i)

        date_data_miss, sorted_data = dict_sorted(date_pre_data, 0, False)
        start = sorted_data[0][0]
        end = sorted_data[-1][0]
        date_key_pre = pd.date_range(start, end)
        date_key = []
        for i in date_key_pre:
            key = str(i).split(' ')[0]
            date_data_miss[key] = date_data_miss.setdefault(key, 0)
        date_data, _ = dict_sorted(date_data_miss, 0, False)
        case_date_number = [list(date_data.keys()), [{
            'name': CASE_NAMES[type],
            'data': list(date_data.values())
        }]]
        case_date_info = {
            'case_date_number':case_date_number
        }
        json_data_w(case_date_info, DATA_PATH + FILENAME_LIST[type] + '_date' + JSON_TYPE_SUFFIX)
        return case_date_info

    def _process_case_cause_info(self, count_limit, type):
        # 处理main函数中案由部分处理结果，输出为限定数目下的案由信息
        # count_limit限制展示的案由数量
        a = json_data_r(PREPROCESS_DATA_PATH + FILENAME_LIST[type] +
            CASE_CAUSE_FILENAME_SUFFIX + JSON_TYPE_SUFFIX)
        b, _ = dict_sorted(a, 1, True)
        ay_info = {
            'name': CASE_NAMES[type],
            'data': []
        }
        count = 0

        for key, value in b.items():
            if count != count_limit:
                ay_meta = {}
                ay_meta['name'] = key
                ay_meta['value'] = value
                ay_info['data'].append(ay_meta)
                count += 1
            else:
                break
        json_data_w([ay_info], DATA_PATH + FILENAME_LIST[type] +
            CASE_CAUSE_FILENAME_SUFFIX + JSON_TYPE_SUFFIX)
        return ay_info

    @connect_mongo('court')
    def _process_case_evaluation(self, type = 3):
        #输入为案件类别信息，案件难度筛选（之后加）
        if type == 3:
            case_info = AllData.objects(省份=PROVINCE_ACTIVATED).limit(10)
        else:
            case_info = AllData.objects(省份=PROVINCE_ACTIVATED, 案件类别=CASE_NAMES[type]).limit(10)

        CASE = {
            'case_id': [],
            'case_title': [],
        }
        for i in case_info:
            CASE['case_id'].append(str(i.id))
            CASE['case_title'].append(i.头部信息[0].split('-')[0])
        json_data_w(CASE, DATA_PATH + FILENAME_LIST[type] +
            '_title' + JSON_TYPE_SUFFIX)
        return CASE

    def _preprocess_case_info(self, case, type):
        case_map = {}
        date_case_number = {}
        error_case = {}
        for i in case:
            try:
                region = re.findall(r'重庆(.*?)法院', i.法院名称)[0].replace('人民','').replace('市', '')
                date = i.年份 + i.日期
                # temp_data = i.头部信息[0]
                case_map[region] = case_map.setdefault(region, 0) + 1
                date_case_number[date] = date_case_number.setdefault(date, 0) + 1
            except Exception as error:
                error_case.append([str(i.id), error])
                print(i.法院名称)

        data = {
            'map':case_map,
            'date_case_number':date_case_number
        }
        json_data_w(data, PREPROCESS_DATA_PATH + FILENAME_LIST[type] +
            JSON_TYPE_SUFFIX)
        json_data_w(error_case, PREPROCESS_DATA_PATH + FILENAME_LIST[type] +
            '_error' + JSON_TYPE_SUFFIX)
        pass

    def _preprocess_case_cause_info(self, case, type):
        #读取网上搜索的相关分类案由信息，存储名为msay_key_2019.txt，输出为*_case_cause_key.json文件
        if type == 0:
            self._civil_cause_key_extract('msay_key_2019.txt', FILENAME_LIST[type] +
                CASE_CAUSE_FILENAME_SUFFIX + '_key' + JSON_TYPE_SUFFIX)
        elif type == 1: 
            self._cause_key_extract('xsay_key_2019.txt', FILENAME_LIST[type] +
                CASE_CAUSE_FILENAME_SUFFIX + '_key' + JSON_TYPE_SUFFIX)
        elif type == 2:
            json_data_w(temp_administrative_case_cause, PREPROCESS_DATA_PATH + FILENAME_LIST[type] +
            CASE_CAUSE_FILENAME_SUFFIX + JSON_TYPE_SUFFIX)
            return
            # 当前没有行政案件的案由文档，暂使用旧数据
            # self._cause_key_extract('xzay_key_2019.txt', FILENAME_LIST[type] +
            #     CASE_CAUSE_FILENAME_SUFFIX + '_key' + JSON_TYPE_SUFFIX)

        cause_key = json_data_r(PREPROCESS_DATA_PATH + FILENAME_LIST[type] +
                CASE_CAUSE_FILENAME_SUFFIX + '_key' + JSON_TYPE_SUFFIX)

        cause_info = {}
        error_case = []
        count = 0
        for i in case:
            count += 1
            try:
                temp_data = i.头部信息[0]
                temp_data = re.split('一审|二审|再审', temp_data)[0]
                # temp_data = re.split('与', temp_data)[-1]
                # print(temp_data)
                pre_ay = process.extractOne(temp_data, cause_key)[0]
                cause_info[pre_ay] = cause_info.setdefault(pre_ay, 0) + 1
                if '-' not in i.头部信息[0]:
                    i.头部信息[0] = i.头部信息[0] + '-' + pre_ay
                    i.save()
                # print(i.头部信息[0])
                if count % 1000 == 0:
                    print(count)
            except Exception as error:
                error_case.append([str(i.id), error])
                # print(i.头部信息, i.id)

        json_data_w(cause_info, PREPROCESS_DATA_PATH + FILENAME_LIST[type] +
            CASE_CAUSE_FILENAME_SUFFIX + JSON_TYPE_SUFFIX)
        json_data_w(error_case, PREPROCESS_DATA_PATH + FILENAME_LIST[type] +
            CASE_CAUSE_FILENAME_SUFFIX + '_error' + JSON_TYPE_SUFFIX)
        pass


    def _cause_key_extract(self, file_name, out_file_name):
        ay_key = []
        with open(DATA_PATH + file_name, 'r', encoding="utf-8") as f:
            a = f.readlines()
            # print(a)
            for i in a:
                crime_list = re.split('\n|\t', i)
                if len(crime_list[1]) > 0:
                    ay_key.append(crime_list[1])
        json_data_w(ay_key, PREPROCESS_DATA_PATH + out_file_name)
        return ay_key

    def _civil_cause_key_extract(self, file_name, out_file_name):
        ay_key = []
        with open(DATA_PATH + file_name, 'r', encoding="utf-8") as f:
            a = f.readlines()
            for i in a:
                extract = re.findall('[\u4e00-\u9fa5]+',i)
                if len(extract) > 1:
                    if re.findall('[一二三四五六七八九十]', extract[0]):
                        extract = extract[1:]
                    else:
                        pass
                if len(extract) == 0:
                    pass
                elif len(extract) > 1:
                    ay_key.append('、'.join(extract))
                else:
                    ay_key.append(extract[0])
        json_data_w(ay_key, PREPROCESS_DATA_PATH + out_file_name)
        return ay_key

# class DataManager(object):

#     categories = {'civil': 0, 'criminal':1, 'administrative':2}
#     category_names = ['民事案件', '刑事案件', '行政案件']
#     case_cause_names = ['民事案由', '刑事案由', '行政案由']

#     def __init__(self):
#         self._civil_case_info = {}
#         self._criminal_case_info = {}
#         self._administrative_case_info = {}
#         self._case_info_collection = []
#         pass


#     def assemble_case_statistics(self):
#         # 读取原始数据
#         if not self._civil_case_info:
#             self._load_case_info('civil')
#         if not self._criminal_case_info:
#             self._load_case_info('criminal')
#         if not self._administrative_case_info:
#             self._load_case_info('administrative')
#         self._case_info_collection = [self._civil_case_info, self._criminal_case_info, self._administrative_case_info]

#         statistics = {}
#         # print(self._case_info_collection)
#         pie_data = self._cal_pie_number()
#         statistics['pie_case_number'] = pie_data[0]
#         statistics['pie_people_number'] = pie_data[1]

#         statistics['case_cause_distribution'] = self._cal_case_cause_distribution()

#         region_distribution = self._cal_case_region_number()
#         statistics['case_region_number'] = region_distribution[0]
#         statistics['map_data'] = region_distribution[1]

#         statistics['case_date_number'] = self._cal_case_date_number()
#         print(statistics)
#         return statistics


#     @connect_mongo('MS_data')
#     def _load_case_info(self, category):

#         case_info = {}
#         if 0 == self.categories[category]:
#             case_info['case_number'] = CivilCaseDoc.objects.count()
#             case_info['people_number'] = 2 * case_info['case_number']
#             case_info['map_data'] = temp_civil_case_region_distribution
#             case_info['case_region_number'] = flatten_dict_tuple_to_transformed_array(case_info['map_data'])
#             case_info['case_date_number'] = temp_civil_case_annual_number
#             self._civil_case_info = case_info
#         elif 1 == self.categories[category]:
#             case_info['case_number'] = CriminalCaseDoc.objects.count()
#             case_info['people_number'] = 2 * case_info['case_number']
#             case_info['map_data'] = temp_criminal_case_region_distribution
#             case_info['case_region_number'] = flatten_dict_tuple_to_transformed_array(case_info['map_data'])
#             case_info['case_date_number'] = temp_criminal_case_annual_number
#             self._criminal_case_info = case_info
#         elif 2 == self.categories[category]:
#             case_info['case_number'] = AdministrativeCaseDoc.objects.count()
#             case_info['people_number'] = 2 * case_info['case_number']
#             case_info['map_data'] = temp_administrative_case_region_distribution
#             case_info['case_region_number'] = flatten_dict_tuple_to_transformed_array(case_info['map_data'])
#             case_info['case_date_number'] = temp_administrative_case_annual_number
#             self._administrative_case_info = case_info
#         else:
#             pass  
#     def _load_case_cause(self):
#        return [
#             temp_civil_case_cause, 
#             temp_criminal_case_cause,
#             temp_administrative_case_cause    
#         ]
#     """
#     TODO 区域名称顺序、数量匹配
#     """  
#     def _cal_case_date_number(self):
#         date_number = []
#         date_number.append(self._civil_case_info['case_date_number'][0])
#         line_data = []
#         for i, info in enumerate(self._case_info_collection):
#             line_data.append(info['case_date_number'][1])
#         date_number.append(line_data)
#         return date_number
