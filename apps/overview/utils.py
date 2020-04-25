#coding: utf-8
"""CourtDataVisualization overview module Utils

在此文件中定义一些可复用的对数据结构等的通用处理
还可以包含一些本模块中特有的数据处理逻辑中的原子环节
"""

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