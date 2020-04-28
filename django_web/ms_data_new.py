#coding:utf-8
#此脚本后续采用定时处理，每隔一定时间进行数据更新，存入json文件

from django_web.models import AllData
import re
from django_web.case_info_process import *
data_path = '/Users/wsk/SJTU_ZHFY/data/case_info/'


def mscase_info_data_process(case):
    map = {}
    date_case_number = {}
    count = 0
    File_name = 'mspre_data'
    for i in case:
        count += 1
        if count % 1000 == 0:
            print(count)

        try:
            region = re.findall(r'重庆(.*?)法院', i.法院名称)[0].replace('人民','').replace('市', '')
            date = i.年份 + i.日期
            # temp_data = i.头部信息[0]

            map[region] = map.setdefault(region, 0) + 1
            date_case_number[date] = date_case_number.setdefault(date, 0) + 1
        except:
            print(i.法院名称)

    data = {
        'map': map,
        'date_case_number': date_case_number
    }
    json_data_w(data, data_path + File_name)
    #读取File_name文件的数据，输出为mscase_info_data文件，包含数量信息数据
    info = case_info(File_name,'mscase_info_data','民事案件')
    return info


def msay_info_data_process(case):
    #读取网上搜索的相关分类案由信息，存储名为msay_key_2019.txt，输出为msay_key文件
    ay_key = ay_key_extract('msay_key_2019.txt', 'msay_key')
    ay_key = json_data_r(data_path + 'msay_key')

    ay_info = {}
    error_case = []
    count = 0
    for i in case:
        count += 1
        try:
            temp_data = i.头部信息[0]
            temp_data = re.split('一审|二审|再审', temp_data)[0]
            # temp_data = re.split('与', temp_data)[-1]
            # print(temp_data)
            pre_ay = process.extractOne(temp_data, ay_key)[0]
            ay_info[pre_ay] = ay_info.setdefault(pre_ay, 0) + 1
            if '-' not in i.头部信息[0]:
                i.头部信息[0] = i.头部信息[0] + '-' + pre_ay
                i.save()
            # print(i.头部信息[0])
            if count % 1000 == 0:
                print(count)
        except:
            error_case.append(str(i.id))
            print(i.头部信息, i.id)

    json_data_w(ay_info, data_path + 'msay_data_pre')
    info = ay_info_process(10, 'msay_data_pre', 'msay_info_data','民事案由')
    return info


if __name__ == '__main__':

    # case = AllData.objects(省份='重庆', 案件类别='民事案件')
    # #输出直接可用json数据文件为mscase_info_data
    # number_info = mscase_info_data_process(case)
    # #输出json文件为msay_info_data
    # ay_info = msay_info_data_process(case)
    # print(number_info)

    File_name = 'mspre_data'
    a = case_info(File_name, 'mscase_info_data', '民事案件')