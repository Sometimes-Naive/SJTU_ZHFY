#coding:utf-8
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
    try:
        with open(file_name, 'r',encoding='utf-8') as f:
            #encoding='utf-8'
            data = json.load(f)
    except:
        with open(file_name, 'r', encoding='gbk') as f:
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
    # cache_2016 = json_data_r('./data/cache_2016')
    cache_2017 = json_data_r('./data/cache_2017')
    # cache_2018 = json_data_r('./data/cache_2018')
    # cache_2019 = json_data_r('./data/cache_2019')

    region_key = json_data_r('./data/map_key')
    # print(cache_2018.keys())
    data = region_key_nor(region_key, cache_2017)
    print(data.keys())
    json_data_w(data, './data/cache_2017_nor.json')
    # print(region_key)


if __name__ == "__main__":
    # data_json_write()
    np.set_printoptions(suppress=True)
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
    data = json_data_r('./data/cache_2017_nor.json')
    region_list = copy.deepcopy(list(data.keys()))
    #check it
    time_list = copy.deepcopy(list(data[region_list[0]].keys()))
    # print(time_list)
    for i in time_list:
        sta_dict[i] = np.zeros((1,40))
    season_dict = {}
    season_dict['第一季度'] = time_list[3:6]
    season_dict['第二季度'] = time_list[6:9]
    season_dict['第三季度'] = time_list[9:]
    season_dict['第四季度'] = time_list[0:3]
    # print(season_dict)
    for i in time_list:
        for j in region_list:
            if i in list(data[j].keys()):
                sja_data = np.array(data[j][i][:])
                sta_dict[i] = sja_data + sta_dict[i]
    # print(sta_dict)



    case_region_dis = {}
    for i in region_list:
        count = 0
        for j in time_list:
            if j in list(data[i].keys()):
                # print(data[i][j][4],data[i][j][8],data[i][j][12])
                #总体案件
                # count = count + data[i][j][4] + data[i][j][8] + data[i][j][12]
                #民事案件
                # count = count + data[i][j][8]
                #刑事案件
                # count = count + data[i][j][4]
                #行政案件
                count = count + data[i][j][12]
        case_region_dis[i] = count
    # print(case_region_dis)

    case_region_season = {}
    for i in region_list:
        season_data = []
        for j in season_dict.keys():

            count = 0
            for k in season_dict[j]:
                if k in list(data[i].keys()):
                    #总体案件
                    # count = count + data[i][k][4] + data[i][k][8] + data[i][k][12]
                    #民事案件
                    # count = count + data[i][k][8]
                    # 刑事案件
                    # count = count + data[i][k][4]
                    # 行政案件
                    count = count + data[i][k][12]
            season_data.append(count)
        case_region_season[i] = season_data
    # print(case_region_season)


    season_sjc_data = []
    count_s = np.array([0,0,0,0])

    for l in range(4):
        count_s = np.array([0, 0, 0, 0])
        for i in region_list:
            season_data = []
            for j in season_dict.keys():

                count = 0
                for k in season_dict[j]:
                    if k in list(data[i].keys()):
                        #总体案件
                        # count = count + data[i][k][4+l] + data[i][k][8+l] + data[i][k][12+l]
                        #民事案件
                        # count = count + data[i][k][8 + l]
                        # 刑事案件
                        # count = count + data[i][k][4 + l]
                        # 行政案件
                        count = count + data[i][k][12 + l]
                season_data.append(count)
            count_s = count_s + np.array(season_data)
        season_sjc_data.append(list(count_s))
    # print(season_sjc_data)

    get_judge_his_data = {
        '总体案件':[],
        '民事案件':[],
        '刑事案件':[],
        '行政案件':[]
    }
    for i in sta_dict.keys():
        get_judge_his_data['民事案件'].append(sta_dict[i][0][8])
        get_judge_his_data['刑事案件'].append(sta_dict[i][0][4])
        get_judge_his_data['行政案件'].append(sta_dict[i][0][12])
        get_judge_his_data['总体案件'].append(sta_dict[i][0][8]+sta_dict[i][0][12]+sta_dict[i][0][4])
    # print(get_judge_his_data)

    map_data = []
    for i in case_region_dis.keys():
        map_data_meta = {

        }
        if '重庆' not in i:
            map_data_meta['name'] = i
            map_data_meta['value'] = case_region_dis[i]
            map_data.append(map_data_meta)
    # print(map_data)

    region_season_his_data = []
    region_his_list = list(case_region_season.keys())
    region_season_his_data.append(region_his_list)
    for i in range(4):
        region_season_his_data_meta = []
        for j in region_his_list:
            region_season_his_data_meta.append(case_region_season[j][i])
        region_season_his_data.append(region_season_his_data_meta)
    # print(region_season_his_data)

    court_season_his_data = {
        '基层法院':[0,0,0,0],
        '中级法院':[0,0,0,0],
        '高级法院':[0,0,0,0]
    }

    for i in case_region_season.keys():
        if '中级' in i:
            court_season_his_data['中级法院'] = list(np.array(court_season_his_data['中级法院']) + np.array(case_region_season[i]))
        elif '高级' in i:
            court_season_his_data['高级法院'] = list(np.array(court_season_his_data['高级法院']) + np.array(case_region_season[i]))
        else:
            court_season_his_data['基层法院'] = list(np.array(court_season_his_data['基层法院']) + np.array(case_region_season[i]))
    # print(court_season_his_data)

    overall_data = {
        'sjc_case_data':season_sjc_data,
        'judge_his_data':get_judge_his_data,
        'map_data':map_data,
        'region_season_his_data':region_season_his_data,
        'court_season_his_data':court_season_his_data,
    }
    print(overall_data)
    # json_data_w(overall_data, './data/adminstrative_case.json')
    # test = json_data_r('./data/overall_statistics.json')
    # print(test)