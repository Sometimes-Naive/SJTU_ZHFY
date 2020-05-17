#coding: utf-8
"""CourtDataVisualization special topic module Utils

在此文件中定义一些可复用的对数据结构等的通用处理
还可以包含一些本模块中特有的数据处理逻辑中的原子环节
"""
import json


def transform_name_value_dict_arr(arr):
    result = []
    for element in arr:
        result.append({
            'name': arr[0],
            'value': arr[1],
            })	
    return result

def flatten_dict_tuple_to_transformed_array(dict_tuple):
    val_1, val_2 = [], []
    for item in dict_tuple:
        val_1.append(item['name'])
        val_2.append(item['value'])
    return [val_1, val_2]

def construct_2d_array_to_dict_tuple(array):
    dict_tuple = []
    for i in range(len(array[0])):
        dict_tuple.append({
            'name': array[0][i],
            'value': array[1][i],
            })
    return dict_tuple

def json_data_w(data, file_name):
    try:
        with open(file_name, 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as error:
        print(error)


def json_data_r(file_name):
    with open(file_name, 'r') as f:
        data = json.load(f)
    return data

    
    
def chinese_to_arabic(cn: str) -> int:
    CN_NUM = {
        '〇': 0, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '零': 0,
        '壹': 1, '贰': 2, '叁': 3, '肆': 4, '伍': 5, '陆': 6, '柒': 7, '捌': 8, '玖': 9, '貮': 2, '两': 2,
    }
    CN_UNIT = {
        '十': 10,
        '拾': 10,
        '百': 100,
        '佰': 100,
        '仠': 1000,
        '千': 1000,
        '仟': 1000,
        '万': 10000,
        '萬': 10000,
        '亿': 100000000,
        '億': 100000000,
        '兆': 1000000000000,
    }
    unit = 0  # current
    ldig = []  # digest
    for cndig in reversed(cn):
        if cndig in CN_UNIT:
            unit = CN_UNIT.get(cndig)
            if unit == 10000 or unit == 100000000:
                ldig.append(unit)
                unit = 1
        else:
            dig = CN_NUM.get(cndig)
            if unit:
                dig *= unit
                unit = 0
            ldig.append(dig)
    if unit == 10:
        ldig.append(10)
    val, tmp = 0, 0
    for x in reversed(ldig):
        if x == 10000 or x == 100000000:
            val += tmp * x
            tmp = 0
        else:
            tmp += x
    val += tmp
    return val
