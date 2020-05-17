#coding:utf-8
from django_web.models import AllData
from django_web.xz_data import xzay_info
from django_web.case_detail import get_case_title
from django_web.case_info_process import *
import copy


data_path = '/Users/Tracy/SJTU_ZHFY/data/case_info/'


allcase_info = {
    '民事案件': json_data_r(data_path + 'mscase_info_data'),
    '刑事案件': json_data_r(data_path + 'xscase_info_data'),
    '行政案件': json_data_r(data_path + 'xzcase_info_data'),
}
cate = ['民事案件', '刑事案件', '行政案件']

class OverView:
    def __init__(self):
        pass

    def list2dict(self, data):
        dict = {}
        for i in data:
            dict[i['name']] = i['value']
        return dict


    def dict2list(self, data):
        region_key = list(data.keys())
        number = list(data.values())
        region_list = []
        for i in range(len(region_key)):
            # print(region_key[i])
            data_meta = {}
            data_meta['name'] = region_key[i]
            data_meta['value'] = number[i]
            # print(data)
            region_list.append(data_meta)
        return region_list

    def get_ay_info(self):
        ay_info = []
        ay_info.append(json_data_r(data_path + 'msay_info_data')[0])
        ay_info.append(json_data_r(data_path + 'xsay_info_data')[0])
        ay_info.append(xzay_info[0])
        return ay_info

    def get_pie_case_number(self, cate, allcase_info):
        pie_case_number = []
        for i in cate:
            pie_meta_case_number = {}
            pie_meta_case_number['name'] = i
            pie_meta_case_number['y'] = allcase_info[i]['case_number']
            pie_case_number.append(pie_meta_case_number)
        return pie_case_number

    def get_pie_people_number(self, cate, allcase_info):
        pie_people_number = []
        for i in cate:
            pie_meta_people_number = {}
            pie_meta_people_number['name'] = i
            pie_meta_people_number['y'] = allcase_info[i]['people_number']
            pie_people_number.append(pie_meta_people_number)
        return pie_people_number

    def get_region_case_number(self, data):
        case_info = copy.deepcopy(data['民事案件']['region_case_number'])
        # case_info[0][0] = 0
        # print(case_info)
        # print(data['民事案件']['region_case_number'])
        # print(case_info is data['民事案件']['region_case_number'])
        for i in range(len(case_info[0])):
            if case_info[0][i] in data['刑事案件']['region_case_number'][0]:
                index = data['刑事案件']['region_case_number'][0].index(case_info[0][i])
                case_info[1][i] = case_info[1][i] + data['刑事案件']['region_case_number'][1][index]
            if case_info[0][i] in data['行政案件']['region_case_number'][0]:
                index = data['行政案件']['region_case_number'][0].index(case_info[0][i])
                case_info[1][i] = case_info[1][i] + data['行政案件']['region_case_number'][1][index]
        # print(case_info)
        return case_info

    def get_map_data(self, data):
        map_data_dict = {}
        msmap = OverView().list2dict(data['民事案件']['map'])
        xsmap = OverView().list2dict(data['刑事案件']['map'])
        xzmap = OverView().list2dict(data['行政案件']['map'])
        for i in list(msmap.keys()):
            map_data_dict[i] = msmap[i] + xsmap[i] + xzmap[i]
            # map_data_dict['value'] = msmap[i] + xsmap[i] + xzmap[i]
        map_data = OverView().dict2list(map_data_dict)
       # print(map_data)
        return map_data

    def get_line_data(self):
        date_case_data = copy.deepcopy(allcase_info['民事案件']['date_case_number'])
        line_data = []
        for i in cate:
            line_data.append(allcase_info[i]['date_case_number'][1][0])
        date_case_data[1] = line_data
        return date_case_data



    def get_case_info(self):
        case_info = {}
        pie_case_number = OverView().get_pie_case_number(cate, allcase_info)
        pie_people_number = OverView().get_pie_people_number(cate, allcase_info)
        ay_info = OverView().get_ay_info()
        region_case_number = OverView().get_region_case_number(allcase_info)
        map_data = OverView().get_map_data(allcase_info)
        line_data = OverView().get_line_data()
        case_info['pie_case_number'] = pie_case_number
        case_info['pie_people_number'] = pie_people_number
        case_info['ay_info'] = ay_info
        case_info['region_case_number'] = region_case_number
        case_info['map_data'] = map_data
        case_info['line_data'] = line_data
        return case_info


case_info = OverView().get_case_info()
CASE = get_case_title()
# print(case_info)

