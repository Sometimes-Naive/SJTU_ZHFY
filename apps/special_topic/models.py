#coding: utf-8
"""CourtDataVisualization special topic module Model Definition

在此文件中定义模块中用到数据库、文件等数据来源所对应的数据格式。
连接Mongo数据库时变量名需要和数据库中对应表（table）中的Json键名一致。
连接Mongo数据库时，API使用可参考： http://docs.mongoengine.org/index.html

"""
# from core.models import *
from mongoengine import *

# TOPIC_data
class DivorceDisputeCaseDoc(Document):
    头部信息=StringField()
    当事人信息 = StringField()
    庭审过程 = StringField()
    尾部信息 = StringField()
    meta = {
        'collection': 'LHJF_data'
    }

# court
class CriminalCaseDoc(Document):
    年份 = StringField()
    日期 = StringField()
    省份 = StringField()
    法院名称 = StringField()
    案件类别 = StringField()
    案件数据 = StringField()
    头部信息 = StringField()
    当事人信息 = StringField()
    庭审过程 = StringField()
    尾部信息 = StringField()
    案由= StringField()

    meta = {
        'collection':'QY2',
        'strict': False
    }