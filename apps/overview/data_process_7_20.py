#coding:utf-8
from mongoengine import *
# from .utils import json_data_w
import re
import json

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
    with open(file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

dict = {}
index = 0
error_id = []
data = AllData.objects(案件类别='刑事案件')
# for i in data:
#     try:
#         index += 1
#         if index % 1000 == 0:
#             print(index)
#         head = i.头部信息
#         re_context = re.split('-',head[0])
#         # print(re_context[0][-7:])
#         class_name = re_context[0][-7:]
#         dict[class_name] = dict.setdefault(class_name, 0) + 1
#
#     except:
#         error_id.append(str(i.id))
#     # break
#23079
print(data.count())
judge_dict = {}
count = 0
for i in data:
    if '刑事判决书' in i.头部信息:
        judge = i.头部信息[0].split('-')[0][-7:]
        judge_dict[judge] = judge_dict.setdefault(judge, 0) + 1
        # print(judge_dict)
print(judge_dict)