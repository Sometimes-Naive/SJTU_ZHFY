#coding:utf-8
from mongoengine import *
# from .utils import json_data_w
import re
import json
from fuzzywuzzy import process

connect('court', host='202.121.180.66', port=7101)

class AllData(DynamicDocument):
    年份 = StringField()
    日期 = StringField()
    省份 = StringField()
    法院名称 = StringField()
    案件类别 = StringField()
    案件数据 = ListField()
    头部信息 = ListField()
    人员信息 = ListField()
    案件过程 = ListField()
    判决信息 = ListField()
    meta = {
        # 'db_alias': 'all_data_db',
        'collection': 'WSK',#database
    }


def json_data_w(data, file_name):
    try:
        with open(file_name, 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as error:
        print(error)


def json_data_r(file_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except:
        with open(file_name, 'r', encoding='gbk') as f:
            data = json.load(f)
    return data

index = 0
error_id = []
data = AllData.objects(案件类别='刑事案件')

# print(data.count())
judge_dict = {}
count = 0
steal_info_list = []
#('妨害公务罪', 229), ('抢劫罪', 230), ('寻衅滋事罪', 322), ('开设赌场罪', 335), ('非法捕捞水产品罪', 371), ('非法持有毒品罪', 376), ('故意伤害罪', 835), ('容留他人吸毒罪', 958), ('诈骗罪', 993),
# ('交通肇事罪', 1009), ('危险驾驶罪', 3273), ('走私、贩卖、运输、制造毒品罪', 3326), ('盗窃罪', 7576)]
def cause_info_pro(data,cause_name):
    count = 0
    for i in data:
        # print(i.头部信息)
        if '刑事判决书' in i.头部信息 and cause_name in i.头部信息[0]:
            count += 1
            # print(count)
            if count % 1000 == 0:
                print(count)
            date = []
            for j in i.判决信息:
                if '年' in j and '月' in j and '日' in j:
                    date = j
            judge_process = i.头部信息[0]
            court_name = i.法院名称
            if '.3.19998文书内容.5118405.405.4.5.51.0' in i.案件数据:
                i.案件数据.remove('.3.19998文书内容.5118405.405.4.5.51.0')
            if '.5118405.405.4.5.51.0' in i.案件数据:
                i.案件数据.remove('.5118405.405.4.5.51.0')
            if '1' in i.案件数据:
                i.案件数据.remove('1')
            people_info = i.案件数据[5]
            judge_dict = {
                'date':date,
                'judge_process':judge_process,
                'court_name':court_name,
                'people_info':people_info,
            }
            steal_info_list.append(judge_dict)
            # print(steal_info_list)
            # break
    print(count)
    return steal_info_list
#
# cause_info = cause_info_pro(data, '危险驾驶罪')
# # print(cause_info)
# # print(count)
# json_data_w(cause_info, './data/criminal_case_drive_info.json')
# cause_info = cause_info_pro(data, '诈骗罪')
# # print(cause_info)
# # print(count)
# json_data_w(cause_info, './data/criminal_case_fraud_info.json')
cause_info = cause_info_pro(data, '交通肇事罪')
# print(cause_info)
# print(count)
json_data_w(cause_info, './data/criminal_case_taccident_info.json')
# data = AllData.objects(案件类别='民事案件')
# count = 0


def ms_judge_info(data):
    count = 0
    info_data_1 = []
    for i in data:

        if '民事判决书' in i.头部信息:
            count += 1
            if count % 1000 == 0:
                print(count)
            people_info = i.人员信息
            # for j in i.案件数据:
            #     if '原告' in j or '上诉人' in j or '申请人' in j:
            #         count += 1
            #         people_info = j
            #         if count % 1000 == 0:
            #             print(count)
            #         break
            date = []
            for j in i.判决信息:
                if '年' in j and '月' in j and '日' in j:
                    date = j
            judge_process = i.头部信息[0]
            court_name = i.法院名称
            cause_name = i.头部信息[0].split('-')[1]
            judge_dict = {
                'cause_name':cause_name,
                'date': date,
                'judge_process': judge_process,
                'court_name': court_name,
                'people_info': people_info,
            }
            info_data_1.append(judge_dict)

            # print(judge_dict)
            # break
    # print(info_data_1)
    return info_data_1
def str2num(year, month, day):
    if len(day) >= 3:
        day = day[0] + day[2]
    chinese_english = dict(零=0, 一=1, 二=2, 三=3, 四=4, 五=5, 六=6, 七=7, 八=8, 九=9, 十=10)
    year = "".join(str(chinese_english[i]) for i in year)
    month = "".join(str(chinese_english[i]) for i in month)
    day = "".join(str(chinese_english[i]) for i in day)
    if len(month) == 3:
        month = month[0] + month[2]
    if len(day) == 3:
        day = day[0] + day[2]
    final_date = year + '年' + month + '月' + day + '日'
    return final_date


def ms_cause(name, path):
    # data = ms_judge_info(data)
    # json_data_w(data, './data/civil_case_all_cause_info.json')

    case_data = json_data_r('./data/criminal_case_'+path+'_info.json')
    map_key = json_data_r('./data/map_key')
    # print(map_key)
    count = 0
    cause_info_list = []
    dict_2 = {}
    for i in case_data:
        # print(i)
        # break
        if i:
            #['cause_name'] == name
            count += 1
            if count % 1000 == 0:
                print(count)
            cause_info_list_dict = {}
            people_class = ''
            age = ''
            gender = ''
            nation = ''
            date = ''
            region = ''
            judge_process = ''

            try:

                date = re.split('年|月|日', i['date'])

                year = list(date[0])

                year.insert(1,'零')
                year = "".join(year)
                if '0' in year:
                    year = year.replace('0','')
                    # print(year)
                date = str2num(year,date[1],date[2])

                i['date'] = date
                region = i['court_name']
                region = re.findall(r'重庆市(.*?)人民法院', region)[0]

                if '中级' not in region and '高级' not in region:
                    region = process.extractOne(region, map_key)[0]
                # if '中级' in region:
                #     print(region)
                judge_process = ''
                if '一审' in i['judge_process']:
                    judge_process = '一审'
                elif '二审' in i['judge_process']:
                    judge_process = '二审'
                elif '再审' in i['judge_process']:
                    judge_process = '再审'
                elif '终审' in i['judge_process']:
                    judge_process = '终审'

                # if '公司' in i['people_info'][0] or '医院' in i['people_info'][0]:
                #     pass
                # else:
                #     print(i['people_info'][0])
                #民事数据改i['people_info']为i['people_info'][0]
                people_info = []
                if '年' in i['people_info'] and '月' in i['people_info'] and '日' in i['people_info']:
                    info = i['people_info']
                    people_class = 'person'
                    birth = re.findall(r'([0-9]{4})年(.*?)月(.*?)日', info)
                    age = 2020 - int(birth[0][0])
                    if '男' in info:
                        gender = '男'
                    elif '女' in info:
                        gender = '女'
                    else:
                        gender = '未知'


                    if '文盲' in info:
                        education = '文盲'
                        # work = re.findall(r'文盲(.{2}?)', info)[0]
                        # print(work)
                        # print(info)
                    else:
                        education = re.findall(r'(.{2}?)文化', info)[0]
                        # work = re.findall(r'文化(.{2}?)', info)[0]
                    if education == '究生':
                        education = '研究生'
                    elif education == '大学':
                        education = '本科'

                    # if '销售' in info:
                    #     print(info)
                    # print(education)
                    # # print(age)
                    # print(work)
                    # dict_2[work] = dict_2.setdefault(work, 0) + 1




                    nation = re.findall(r'(.?)族',info)[0]
                    if nation == '家':
                        nation = '土家'
                # else:
                #     # print(i['people_info'][0])
                #     people_class = 'organization'
                #     print(i)

            except:

                pass

            cause_info_list_dict = {
                'date': date,
                'region': region,
                'judge_process': judge_process,
                'people_class':people_class,
                'age':age,
                'gender':gender,
                'nation':nation,
                'education':education,

            }
            # print(cause_info_list_dict)
            # break
            # print(cause_info_list_dict)
            cause_info_list.append(cause_info_list_dict)
            # print(cause_info_list)
            # break
    # print(sorted(dict_2.items(), key=lambda key:(key[1], key[0])))
    # work_list = ['无业', '农民', '务工', '务农', '工人', '厨师', '教师', '销售', '保安', '退休', '无业', '无业', '无业', '无业', ]
    # print(count)
    # print(cause_info_list)
    json_data_w(cause_info_list, './data/criminal_case_'+path+'_chartinfo_1.json')
# dict_2 = {}
cause_mapping = {
    '服务合同纠纷':'civil_case_ServiceContractDispute_info.json',

    '合同纠纷': 'civil_case_ContractDispute_info.json',

    '信用卡纠纷': 'civil_case_CreditCardDispute_info.json',

    '劳动争议': 'civil_case_LaborDispute_info.json',

    '民间借贷纠纷': 'civil_case_PrivateLendingDispute_info.json',

    '机动车交通事故责任纠纷': 'civil_case_TrafficAccidentDispute_info.json',

    '借款合同纠纷': 'civil_case_LoanContractDispute_info.json',

    '买卖合同纠纷': 'civil_case_TradeContractDispute_info.json',


}

# for i in cause_mapping.keys():
#     ms_cause(i, cause_mapping[i])
# criminal_cause_info = json_data_r('./data/criminal_case_larceny_info.json')
# print(criminal_cause_info)
# xs_key = ['drive', 'drug', 'fraud', 'larceny', 'taccident']
# for i in xs_key:
#     ms_cause('11', i)