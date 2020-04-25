#coding: utf-8
"""CourtDataVisualization overview module data manager

在此文件中定义模块中数据的处理业务逻辑，是整个模块的功能核心所在。
在视图页面需要的数据通过调用本文件中的函数获取，
同时本文件负责从模型（models）中利用drivers获取原始数据。

可以直接定义数据处理函数，再遇到复杂逻辑时建议定义Manager类统筹管理。
定义类时需要注意访问控制，同时为保证每一个函数的易读性，每个函数长度不超过30行。
"""

from .models import *
from .temp_data import *
from .utils import *


def compose_case_details():
    details = {
        'case_id': [],
        'case_title': [],
        'case_detail': [],
    }
    print(111111)
    for doc in CriminalCaseDoc.objects.all()[:10]:
        details['case_id'].append(str(doc.id))
        details['case_title'].append(doc.标题)
        details['case_detail'].append(doc.庭审过程)
    return details


class DataManager():

    categories = {'civil': 0, 'criminal':1, 'administrative':2}
    category_names = ['民事案件', '刑事案件', '行政案件']
    case_cause_names = ['民事案由', '刑事案由', '行政案由']

    def __init__(self):
        self._civil_case_info = {}
        self._criminal_case_info = {}
        self._administrative_case_info = {}
        self._case_info_collection = []
        pass


    def assemble_case_statistics(self):
        # 读取原始数据
        if not self._civil_case_info:
            self._load_case_info('civil')
        if not self._criminal_case_info:
            self._load_case_info('criminal')
        if not self._administrative_case_info:
            self._load_case_info('administrative')
        self._case_info_collection = [self._civil_case_info, self._criminal_case_info, self._administrative_case_info]

        statistics = {}
        # print(self._case_info_collection)
        pie_data = self._cal_pie_number()
        statistics['pie_case_number'] = pie_data[0]
        statistics['pie_people_number'] = pie_data[1]

        statistics['case_cause_distribution'] = self._cal_case_cause_distribution()

        region_distribution = self._cal_case_region_number()
        statistics['case_region_number'] = region_distribution[0]
        statistics['map_data'] = region_distribution[1]

        statistics['case_date_number'] = self._cal_case_date_number()
        print(statistics)
        return statistics


    def _load_case_info(self, category):

        case_info = {}
        if 0 == self.categories[category]:
            case_info['case_number'] = CivilCaseDoc.objects.count()
            case_info['people_number'] = 2 * case_info['case_number']
            case_info['map_data'] = temp_civil_case_region_distribution
            case_info['case_region_number'] = flatten_dict_tuple_to_transformed_array(case_info['map_data'])
            case_info['case_date_number'] = temp_civil_case_annual_number
            self._civil_case_info = case_info
        elif 1 == self.categories[category]:
            case_info['case_number'] = CriminalCaseDoc.objects.count()
            case_info['people_number'] = 2 * case_info['case_number']
            case_info['map_data'] = temp_criminal_case_region_distribution
            case_info['case_region_number'] = flatten_dict_tuple_to_transformed_array(case_info['map_data'])
            case_info['case_date_number'] = temp_criminal_case_annual_number
            self._criminal_case_info = case_info
        elif 2 == self.categories[category]:
            case_info['case_number'] = AdministrativeCaseDoc.objects.count()
            case_info['people_number'] = 2 * case_info['case_number']
            case_info['map_data'] = temp_administrative_case_region_distribution
            case_info['case_region_number'] = flatten_dict_tuple_to_transformed_array(case_info['map_data'])
            case_info['case_date_number'] = temp_administrative_case_annual_number
            self._administrative_case_info = case_info
        else:
            pass	


    def _load_case_cause(self):
       return [
            temp_civil_case_cause, 
            temp_criminal_case_cause,
            temp_administrative_case_cause    
        ]


    def _cal_pie_number(self):
        pie_data = [[], []]
        for i,info in enumerate(self._case_info_collection):
            print(info)
            pie_data[0].append({
                'name': self.category_names[i],
                'y': info['case_number']
                })
            pie_data[1].append({
                'name': self.category_names[i],
                'y': info['people_number']
                })
        return pie_data


    def _cal_case_cause_distribution(self):
        cause_data_collection = self._load_case_cause()
        case_cause = []
        for idx, causes in enumerate(cause_data_collection):
            case_cause.append({
                'name': self.case_cause_names[idx],

                'data': transform_name_value_dict_arr(sorted(causes.items(), key=lambda x: x[1], reverse=True)[:6])
                })
        return case_cause
    

    """
    TODO 区域名称顺序、数量匹配
    """  
    def _cal_case_region_number(self):
        region_arr, case_region_number = self._civil_case_info['case_region_number']

        for i in range(len(region_arr)):
            for j in range(len(self._criminal_case_info['case_region_number'][0])):
                if region_arr[i] == self._criminal_case_info['case_region_number'][0][j]:
                    case_region_number[i] = case_region_number[i] + self._criminal_case_info['case_region_number'][1][j] + \
                                      self._administrative_case_info['case_region_number'][1][j]
        return [[region_arr, case_region_number], construct_2d_array_to_dict_tuple([region_arr, case_region_number])]


    def _cal_case_date_number(self):
        date_number = []
        date_number.append(self._civil_case_info['case_date_number'][0])
        line_data = []
        for i, info in enumerate(self._case_info_collection):
            line_data.append(info['case_date_number'][1])
        date_number.append(line_data)
        return date_number




