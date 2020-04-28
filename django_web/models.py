#coding: utf-8

from django.db import models
from mongoengine import *

disconnect()
connect('MS_data', host='202.121.180.66', port=7101, alias='default')
connect('TOPIC_data', host='202.121.180.66', port=7101, alias='topic_db')
connect('court', host='202.121.180.66', port=7101, alias='all_data_db')

class LHJF(Document):
    头部信息 = StringField()
    当事人信息 = StringField()
    庭审过程 = StringField()
    尾部信息 = StringField()
    meta = {
        'db_alias':'topic_db',
        'collection': 'LHJF_data'
    }

class AllData(Document):
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
        'db_alias': 'all_data_db',
        'collection': 'database'
    }

class XSAJ(Document):
    标题 = StringField()
    案号 = StringField()
    案件类型 = StringField()
    庭审程序 = StringField()
    案由 = StringField()
    文书类型 = StringField()
    法院 = StringField()
    判决日期 = StringField()
    原告 = StringField()
    被告 = StringField()
    第三人 = StringField()
    法官 = StringField()
    审判长 = StringField()
    审判员 = StringField()
    书记员 = StringField()
    头部 = StringField()
    头部2 = StringField()
    当事人 = StringField()
    当事人2 = StringField()
    庭审程序说明 = StringField()
    庭审程序说明2 = StringField()
    庭审过程 = StringField()
    庭审过程2 = StringField()
    庭审过程3 = StringField()
    庭审过程4 = StringField()
    庭审过程5 = StringField()
    庭审过程6 = StringField()
    法院意见 = StringField()
    法院意见2 = StringField()
    判决结果 = StringField()
    判决结果2 = StringField()
    庭后告知 = StringField()
    庭后告知2 = StringField()
    结尾 = StringField()
    结尾2 = StringField()
    附录 = StringField()
    附录2 = StringField()
    meta = {
        'collection':'XS_law_data'
    }

class XZAJ(Document):
    标题 = StringField()
    案号 = StringField()
    案件类型 = StringField()
    庭审程序 = StringField()
    案由 = StringField()
    文书类型 = StringField()
    法院 = StringField()
    判决日期 = StringField()
    原告 = StringField()
    被告 = StringField()
    第三人 = StringField()
    法官 = StringField()
    审判长 = StringField()
    审判员 = StringField()
    书记员 = StringField()
    头部 = StringField()
    头部2 = StringField()
    当事人 = StringField()
    当事人2 = StringField()
    庭审程序说明 = StringField()
    庭审程序说明2 = StringField()
    庭审过程 = StringField()
    庭审过程2 = StringField()
    庭审过程3 = StringField()
    庭审过程4 = StringField()
    庭审过程5 = StringField()
    庭审过程6 = StringField()
    法院意见 = StringField()
    法院意见2 = StringField()
    判决结果 = StringField()
    判决结果2 = StringField()
    庭后告知 = StringField()
    庭后告知2 = StringField()
    结尾 = StringField()
    结尾2 = StringField()
    附录 = StringField()
    附录2 = StringField()
    meta = {
        'collection':'XZ_law_data'
    }

class MSAJ(Document):
    标题 = StringField()
    案号 = StringField()
    案件类型 = StringField()
    庭审程序 = StringField()
    案由 = StringField()
    文书类型 = StringField()
    法院 = StringField()
    判决日期 = StringField()
    原告 = StringField()
    被告 = StringField()
    第三人 = StringField()
    法官 = StringField()
    审判长 = StringField()
    审判员 = StringField()
    书记员 = StringField()
    头部 = StringField()
    头部2 = StringField()
    当事人 = StringField()
    当事人2 = StringField()
    庭审程序说明 = StringField()
    庭审程序说明2 = StringField()
    庭审过程 = StringField()
    庭审过程2 = StringField()
    庭审过程3 = StringField()
    庭审过程4 = StringField()
    庭审过程5 = StringField()
    庭审过程6 = StringField()
    法院意见 = StringField()
    法院意见2 = StringField()
    判决结果 = StringField()
    判决结果2 = StringField()
    庭后告知 = StringField()
    庭后告知2 = StringField()
    结尾 = StringField()
    结尾2 = StringField()
    附录 = StringField()
    附录2 = StringField()
    meta = {
        'collection':'MS_law_data'
    }


if __name__ == "__main__":
    docs = AllData.objects(省份='重庆').count()
    print(docs)