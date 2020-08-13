#coding:utf-8
import os
import xlrd
import numpy as np
import copy
import json
import re
from fuzzywuzzy import process

def json_data_w(data, file_name):
    try:
        with open(file_name, 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as error:
        print(error)


def json_data_r(file_name):
    try:
        with open(file_name, 'r',encoding='utf-8') as f:
            #encoding='utf-8'
            data = json.load(f)
    except:
        with open(file_name, 'r', encoding='gbk') as f:
            data = json.load(f)
    return data

def check_date(data):
    date_dict = {}
    for i in data:
        date = ''
        if ('年' and '月' and '日') in i['date']:
            date = i['date']
            date = re.split('年|月|日', date)[:2]
            date = ".".join(date)
            # print(date)
        try:
            date_dict[date] = date_dict.setdefault(date, 0) + 1
        except:
            pass
    return sorted(date_dict.items())


#展示2018年数据
#刑事案件罪名数据分析
#'drive危险驾驶罪''drug走私、贩卖、运输、制造毒品罪''fraud诈骗罪''larceny盗窃罪''taccident交通肇事罪'
path = 'taccident'
name = '交通肇事罪'
data = json_data_r('./data/criminal_case_'+path+'_chartinfo_1.json')
print(data[0].keys())

def pie_line_data_extract(data, key_name):
    data_return = {}
    date_key = ['2018年1月', '2018年2月', '2018年3月', '2018年4月', '2018年5月', '2018年6月', '2018年7月', '2018年8月', '2018年9月',
                '2018年10月', '2018年11月', '2018年12月']
    judge = []
    #
    for j in date_key:

        judge_dict = {
            'date':j,
        }
        for i in data:
            cache = i[key_name]
            if j in i['date'] and cache != '':

                # print(i['judge_process'])
                judge_dict[cache] = judge_dict.setdefault(cache, 0) + 1
        judge.append(judge_dict)

    pie_data = []
    line_data = []

    for i in judge:
        key_list = list(i.keys())
        for j in key_list:
            # print(j)
            for k in range(12):
                judge[k][j] = judge[k].setdefault(j, 0)


    for j in judge[0].keys():
        line_data_meta = {
            'name':j,
            'data':[],
        }
        for i in judge:
            line_data_meta['data'].append(i[j])
        line_data.append(line_data_meta)
    for i in line_data[1:]:
        pie_data_meta = {}
        pie_data_meta['name'] = i['name']
        pie_data_meta['y'] = sum(i['data'])
        pie_data.append(pie_data_meta)
    data_return['pie_data'] = pie_data
    data_return['line_data'] = line_data
    return data_return

#地区案件数据提取
region_data = pie_line_data_extract(data, 'region')
#法院层级数据提取
base_court = np.zeros((1, 12))[0]
middle_court = np.zeros((1, 12))[0]
advanced_court = np.zeros((1, 12))[0]
# print(region_data)
for i in region_data['line_data'][1:]:
    if '中级' not in i['name'] and '高级' not in i['name']:
        base_court = base_court + np.array(i['data'])
    elif '中级' in i['name']:
        middle_court = middle_court + np.array(i['data'])
    else:
        advanced_court = advanced_court + np.array(i['data'])

# print(base_court)
class_pie_data = [{'name':'基层法院', 'y':sum(base_court)}, {'name':'中级法院', 'y':sum(middle_court)},{'name':'高级法院', 'y':sum(advanced_court)}]
class_line_data = [{'name': 'date', 'data': ['2018年1月', '2018年2月', '2018年3月', '2018年4月', '2018年5月', '2018年6月', '2018年7月', '2018年8月', '2018年9月', '2018年10月', '2018年11月', '2018年12月']},
                   {'name':'基层法院', 'data':list(base_court)},{'name':'中级法院', 'data':list(middle_court)},{'name':'高级法院', 'data':list(advanced_court)}]
class_data = {
    'pie_data':class_pie_data,
    'line_data':class_line_data
}
#性别数据提取
gender_data = pie_line_data_extract(data, 'gender')
#一审二审审理流程数据提取
process_data = pie_line_data_extract(data, 'judge_process')
process_list = []
for i in process_data['line_data']:
    process_list.append(i['name'])
if '再审' not in process_list:
    process_data['line_data'].append({'name':'再审','data':[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]})
    process_data['pie_data'].append({'name':'再审','y':0})
if '终审' not in process_list:
    process_data['line_data'].append({'name': '终审', 'data': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]})
    process_data['pie_data'].append({'name': '终审', 'y': 0})
# print(process_data)
#学历数据提取
education_data = pie_line_data_extract(data, 'education')
#年龄数据提取
age_data_dis = pie_line_data_extract(data, 'age')
#民族数据提取
nation_data = pie_line_data_extract(data, 'nation')
#收结案数据提取
# print(class_data)
sja_data = np.zeros((1,12))[0]
for i in class_data['line_data'][1:]:
    sja_data = sja_data + np.array(i['data'])
sja_data = list(sja_data)
#地图数据提取
map_data = []
for i in region_data['line_data'][1:]:
    map_data_meta = {}
    map_data_meta['name'] = i['name']
    map_data_meta['value'] = sum(i['data'])
    map_data.append(map_data_meta)

def season_data(data):
    season_data = {}
    for i in data['line_data'][1:]:
        season_data[i['name']] = []
        for j in range(4):
            # print(i['data'][j*3:j*3+3])
            season_data[i['name']].append(sum(i['data'][j*3:j*3+3]))
    return season_data
#审理流程季度数据处理
process_season_data = season_data(process_data)
#法院层级季度数据处理
class_season_data = season_data(class_data)
#收结案季度数据提取
sja_season_data = []

for j in range(4):
    # print(i['data'][j*3:j*3+3])
    sja_season_data.append(sum(sja_data[j*3:j*3+3]))
# print(sja_season_data)
#地区季度数据提取，第一个柱状图数据
region_season_data_1 = season_data(region_data)
region_name = list(region_season_data_1.keys())
region_season_data_2 = []
for i in range(4):
    region_season_data_2_meta = []
    for j in region_season_data_1.keys():
        region_season_data_2_meta.append(region_season_data_1[j][i])

    region_season_data_2.append(region_season_data_2_meta)
region_seanson_data = {
    'name':region_name,
    'season_data':region_season_data_2
}
#年龄数据区间处理
age_data_pro = age_data_dis
age_line_data_meta = {}
age_list = {
    '20岁以下':np.zeros((1,12))[0],
    '20岁~30岁':np.zeros((1,12))[0],
    '30岁~40岁':np.zeros((1,12))[0],
    '40岁~50岁':np.zeros((1,12))[0],
    '50岁以上':np.zeros((1,12))[0],
}
for i in age_data_pro['line_data'][1:]:
    if i['name'] <= 20:
        age_list['20岁以下'] = age_list['20岁以下'] + i['data']
    elif 20 < i['name'] <= 30:
        age_list['20岁~30岁'] = age_list['20岁~30岁'] + i['data']
    elif 30 < i['name'] <= 40:
        age_list['30岁~40岁'] = age_list['30岁~40岁'] + i['data']
    elif 40 < i['name'] <= 50:
        age_list['40岁~50岁'] = age_list['40岁~50岁'] + i['data']
    else:
        age_list['50岁以上'] = age_list['50岁以上'] + i['data']


age_pie_data = []
age_line_data = [age_data_pro['line_data'][0]]
for i in age_list.keys():
    age_pie_data_meta = {}
    age_line_data_meta = {}
    age_pie_data_meta['name'] = i
    age_pie_data_meta['y'] = sum(age_list[i])
    age_line_data_meta['name'] = i
    age_line_data_meta['data'] = list(age_list[i])
    age_pie_data.append(age_pie_data_meta)
    age_line_data.append(age_line_data_meta)

age_data = {
    'pie_data':age_pie_data,
    'line_data':age_line_data,
}
#整体数据汇总
data_dict = {
    'name':name,
    'map_data':map_data,
    'sja_data':sja_data,
    'class_data':class_data,
    'process_data':process_data,
    'region_season_data':region_seanson_data,
    'process_season_data':process_season_data,
    'class_season_data':class_season_data,
    'sja_season_data':sja_season_data,
    'education':education_data,
    'gender_data':gender_data,
    'age_data':age_data,
    'nation_data':nation_data
}
#数据存储
# print(data_dict)
json_data_w(data_dict, './data/criminal_case_'+path+'_chartinfo.json')
print(data_dict['process_season_data'])


