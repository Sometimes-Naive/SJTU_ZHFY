#coding:utf-8

from django_web.models import AllData
import re
import json
from fuzzywuzzy import process
import copy
import pandas as pd
data_path = '/Users/wsk/SJTU_ZHFY/data/case_info/'


def json_data_w(data, file_name):
    with open(file_name, 'w') as f:
        json.dump(data, f)


def json_data_r(file_name):
    with open(file_name, 'r') as f:
        data = json.load(f)
    return data


def dict_sorted(dict, label, reverse):
    #label 0表示按kay排序，1表示按values排序
    #reverse True为降序，False为升序
    sorted_tuple_data = sorted(dict.items(), key=lambda dict: dict[label], reverse=reverse)
    data = {}
    for i in sorted_tuple_data:
        data[i[0]] = i[1]
    return data, sorted_tuple_data


def ay_key_extract(file_name, out_file_name):
    ay_key = []
    with open(data_path + file_name, 'r') as f:
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
    json_data_w(ay_key, data_path + out_file_name)
    return ay_key

def map_data_repalce(file_name):
    #file_name为存储predata的名字，输出存储为原文件名加'_map'，输出为修正地区名之后的地图数据和地区案件数据
    map_key = json_data_r(data_path + 'map_key')
    map = json_data_r(data_path + file_name)['map']
    map_bak = {}
    for i in map.keys():
        map_re = process.extractBests(i, map_key, score_cutoff=60)
        if map_re:
            map_bak[map_re[0][0]] = map[i]
    # print(map_bak)
    map_data = []
    for i, j in map_bak.items():
        map_data_meta = {}
        map_data_meta['name'] = i
        map_data_meta['value'] = j
        map_data.append(map_data_meta)
    map, _ = dict_sorted(map, 1, True)
    region_case_number = [list(map.keys()), list(map.values())]
    case_map_info = {
        'map': map_data,
        'region_case_number': region_case_number
    }
    json_data_w(case_map_info, data_path + file_name + '_map')

    return case_map_info


def date_case_data(file_name,case_cate):
    date_pre_data = json_data_r(data_path + file_name)['date_case_number']
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
    date_case_number = [list(date_data.keys()), [{
        'name': case_cate,
        'data': list(date_data.values())
    }]]
    case_date_info = {
        'date_case_number':date_case_number
    }
    json_data_w(case_date_info, data_path + file_name + '_date')
    return case_date_info


def case_info(file_name, out_file_name, case_cate):
    number = AllData.objects(省份='重庆', 案件类别=case_cate).count()
    map = map_data_repalce(file_name)
    date_case_number = date_case_data(file_name, case_cate)
    case_info = {
        'case_number': number,
        'people_number': 2 * number,
        'map': map['map'],
        'region_case_number': map['region_case_number'],
        'date_case_number': date_case_number['date_case_number']
    }
    json_data_w(case_info, data_path + out_file_name)
    return case_info


def ay_info_process(count_restrict, file_name, out_file_name, case_cate):
    # 处理main函数中案由部分处理结果，输出为限定数目下的案由信息
    # count_restrict限制展示的案由数量
    a = json_data_r(data_path + file_name)
    b, _ = dict_sorted(a, 1, True)
    ay_info = {
        'name': case_cate,
        'data': []
    }
    count = 0

    for key, value in b.items():
        if count != count_restrict:
            ay_meta = {}
            ay_meta['name'] = key
            ay_meta['value'] = value
            ay_info['data'].append(ay_meta)
            count += 1
        else:
            break
    json_data_w([ay_info], data_path + out_file_name)
    return ay_info