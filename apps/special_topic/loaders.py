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

    def load_quantity_result(self, subject, category):
        if subject == 'civil':
            return json_data_r(os.path.join(DATA_PATH, CIVIL_TOPIC_DIRNAME[CIVIL_TOPIC_DICT[category]]) + os.sep + FILENAME_LIST[0])
        elif subject == 'criminal':
            return json_data_r(os.path.join(DATA_PATH, CRIMINAL_TOPIC_DIRNAME[CRIMINAL_TOPIC_DICT[category]]) + os.sep + FILENAME_LIST[0])
        elif subject == 'administrative':
            pass

    def load_party_result(self, subject, category):
        if subject == 'civil':
            return json_data_r(os.path.join(DATA_PATH, CIVIL_TOPIC_DIRNAME[CIVIL_TOPIC_DICT[category]]) + os.sep + FILENAME_LIST[1])
        elif subject == 'criminal':
            return json_data_r(os.path.join(DATA_PATH, CRIMINAL_TOPIC_DIRNAME[CRIMINAL_TOPIC_DICT[category]]) + os.sep + FILENAME_LIST[1])
        elif subject == 'administrative':
            pass

    def load_topic_result(self, subject, category):
        if subject == 'civil':
            return json_data_r(os.path.join(DATA_PATH, CIVIL_TOPIC_DIRNAME[CIVIL_TOPIC_DICT[category]]) + os.sep + FILENAME_LIST[2])
        elif subject == 'criminal':
            return json_data_r(os.path.join(DATA_PATH, CRIMINAL_TOPIC_DIRNAME[CRIMINAL_TOPIC_DICT[category]]) + os.sep + FILENAME_LIST[2])
        elif subject == 'administrative':
            pass