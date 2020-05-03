#coding: utf-8
"""CourtDataVisualization overview module data loader

在此文件中定义模块中加载数据处理结果的方法。
在视图页面需要的数据通过调用本文件中的函数获取，

定义类时需要注意访问控制，同时为保证每一个函数的易读性，每个函数长度不超过30行。
"""
from .utils import *
from .constants import * 


class ResultLoader(object):

    def __init__(self):
        pass

    def load_case_basic_result(self, category):
        return json_data_r(DATA_PATH + FILENAME_LIST[CATEGORIES[category]] + JSON_TYPE_SUFFIX)

    def load_case_cause_result(self, category):
        return json_data_r(DATA_PATH + FILENAME_LIST[CATEGORIES[category]] +
            CASE_CAUSE_FILENAME_SUFFIX + JSON_TYPE_SUFFIX)

    def load_case_evaluation_title(self, category):
        return json_data_r(DATA_PATH + FILENAME_LIST[CATEGORIES[category]] +
            '_title' + JSON_TYPE_SUFFIX)