import os
import xlrd
import numpy as np
import copy
import json
from fuzzywuzzy import process

def json_data_w(data, file_name):
    try:
        with open(file_name, 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as error:
        print(error)


def json_data_r(file_name):
    with open(file_name, 'r') as f:
        #encoding='utf-8'
        data = json.load(f)
    return data

def excel_data_test(path):
    #excel表格数据测试
    # path = 'D:/工作/法院项目相关/数据相关/数据汇总0524/收结存/2016/10月/石柱/1558611226259/000100_各类案件收结存情况统计表.xls'
    data = xlrd.open_workbook(path)
    sheet = data.sheet_by_index(0)
    date = ''.join([path.split('\\')[6] + '年', path.split('\\')[7]])
    region_name = sheet.row_values(2)[0].split('：')[1]
    dict = {

    }

    row_data = sheet.row_values(4)
    case_class_name = [i for i in row_data if i != '']
    # print(len(case_class_name))
    print(region_name)
    row_data = sheet.row_values(7)[6:]
    dict['index_name'] = case_class_name
    dict[region_name] = {
        date: row_data
    }

    # print(dict)
    return dict



def data_clean2dict():
    #解压完毕数据进行整理，输出字典数据
    dict = {}
    all_dict = {}
    path = 'D:\工作\法院项目相关\数据相关\数据汇总0524\收结存\\2018'
    dir = os.scandir(path)
    for entry in dir:
        sub_dir = os.scandir(entry.path)
        for entry_sub in sub_dir:#到地区级别目录
            # print(entry_sub.path)
            file_dir = os.scandir(entry_sub.path)
            for file_dir_excel in file_dir:
                final_dir = file_dir_excel.path + '\\000100_各类案件收结存情况统计表.xls'
                # print(''.join([final_dir.split('\\')[6]+'年',final_dir.split('\\')[7]]))
                test_dict = excel_data_test(final_dir)
                # dict['index_name'] = test_dict['index_name']
                dict[list(test_dict.keys())[1]] = test_dict[list(test_dict.keys())[1]]

        for i in list(dict.keys()):
            if i in list(all_dict.keys()):
                # print(all_dict[i])
                # print(dict[i])
                # print('*' * 100)
                all_dict[i].update(dict[i])
            else:
                all_dict[i] = copy.deepcopy(dict[i])
    return all_dict


def region_key_nor_2016(region_key, cache_data):
    #2016年数据地区名称统一化清洗
    # print(cache_data.keys())
    if cache_data['开县人民法院'] is not None:
        cache_data['开州区'] = cache_data.pop('开县人民法院')
    if cache_data['彭水县人民法院'] is not None:
        cache_data['彭水苗族土家族'] = cache_data.pop('彭水县人民法院')
    # print(cache_data.keys())
    for i in cache_data.keys():
        match = process.extractOne(i, region_key, score_cutoff=60)
        if match is not None:
            print(i,match)
            cache_data[match[0]] = cache_data.pop(i)
    return cache_data

def region_key_nor(region_key, cache_data):
    #其他年份数据地区名称清洗
    # print(cache_data.keys())
    # if cache_data['开县人民法院'] is not None:
    #     cache_data['开州区'] = cache_data.pop('开县人民法院')
    if cache_data['彭水县人民法院'] is not None:
        cache_data['彭水苗族土家族'] = cache_data.pop('彭水县人民法院')
    key_list = copy.deepcopy(list(cache_data.keys()))
    for i in key_list:
        match = process.extractOne(i, region_key, score_cutoff=60)
        if match is not None:
            print(i,match)
            cache_data[match[0]] = cache_data.pop(i)
    return cache_data

def data_json_write():
    cache_2016 = json_data_r('./cache_2016')
    cache_2017 = json_data_r('./cache_2017')
    cache_2018 = json_data_r('./cache_2018')
    cache_2019 = json_data_r('./cache_2019')

    region_key = json_data_r('./data/map_key')
    # print(cache_2018.keys())
    data = region_key_nor(region_key, cache_2017)
    print(data.keys())
    json_data_w(data, './cache_2017_nor.json')
    # print(region_key)


if __name__ == "__main__":
    np.set_printoptions(suppress=True, threshold=np.inf)
    '''"刑事案件收案",4
    "刑事案件旧存",5
    "刑事案件结案",6
    "刑事案件未结",7
    "民事案件收案",8
    "民事案件旧存",9
    "民事案件结案",10
    "民事案件未结",11
    "行政案件收案",12
    "行政案件旧存",13
    "行政案件结案",14
    "行政案件未结",15
    '''
    sta_dict = {}
    data = json_data_r('./cache_2017_nor.json')
    region_list = copy.deepcopy(list(data.keys()))
    #check it
    time_list = copy.deepcopy(list(data[region_list[0]].keys()))
    # print(time_list)
    for i in region_list:
        time_list_check = list(data[i].keys())
        for j in time_list:
            if j not in time_list_check:
                data[i][j] = np.zeros(1,40)
                print(data[i][j])


    # region_dim = len(list(data.keys()))
    # time_dim = len(list(data[region_list[0]].keys()))
    # cha_dim = 40
    # matrix = np.zeros((region_dim, time_dim, cha_dim), dtype=float)
    # # print(matrix)
    # for i in range(len(region_list)):
    #     print(len(list(data[region_list[i]].keys())))
    #     for j in range(len(list(data[region_list[i]].keys()))):
    #         index = list(data[region_list[i]].keys())[j]
    #
    #         # print(index)
    #         matrix[i][j] = data[region_list[i]][index]
    #     # break
    # # print(matrix)