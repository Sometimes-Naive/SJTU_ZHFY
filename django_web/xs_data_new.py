#coding:utf-8
#此脚本后续采用定时处理，每隔一定时间进行数据更新，存入json文件

from django_web.models import AllData
import re
from django_web.case_info_process import *
data_path = '/Users/wsk/SJTU_ZHFY/data/case_info/'


def xsay_key_extract(file_name, out_file_name):
    ay_key = []
    with open(data_path + file_name, 'r') as f:
        a = f.readlines()
        # print(a)
        for i in a:
            crime_list = re.split('\n|\t', i)
            if len(crime_list[1]) > 0:
                ay_key.append(crime_list[1])
    json_data_w(ay_key, data_path + out_file_name)
    return ay_key

def xscase_info_data_process(case):
    map = {}
    date_case_number = {}
    File_name = 'xspre_data'
    for i in case:
        try:
            region = re.findall(r'重庆(.*?)法院', i.法院名称)[0].replace('人民','').replace('市', '')
            date = i.年份 + i.日期
            # temp_data = i.头部信息[0]

            map[region] = map.setdefault(region, 0) + 1
            date_case_number[date] = date_case_number.setdefault(date, 0) + 1
        except:
            print(i.法院名称)

    data = {
        'map':map,
        'date_case_number':date_case_number
    }
    json_data_w(data, data_path + File_name)
    #读取File_name文件的数据，输出为mscase_info_data文件，包含数量信息数据
    info = case_info(File_name,'xscase_info_data','刑事案件')
    return info


def xsay_info_data_process(case):
    #读取网上搜索的相关分类案由信息，存储名为msay_key_2019.txt，输出为msay_key文件
    ay_key = xsay_key_extract('xsay_key_2019.txt', 'xsay_key')
    ay_key = json_data_r(data_path + 'xsay_key')

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

    json_data_w(ay_info, data_path + 'xsay_data_pre')
    json_data_w(error_case, data_path + 'xserror_data')
    info = ay_info_process(10, 'xsay_data_pre', 'xsay_info_data','刑事案由')

    return info, error_case


if __name__ == '__main__':

    # case = AllData.objects(省份='重庆', 案件类别='刑事案件')
    # # 输出直接可用json数据文件为mscase_info_data
    # number_info = xscase_info_data_process(case)
    # #输出json文件为msay_info_data
    # ay_info, error = xsay_info_data_process(case)
    # print(number_info)
    # print(ay_info)
    # print(error,len(error))
    File_name = 'xspre_data'
    a = case_info(File_name, 'xscase_info_data', '刑事案件')