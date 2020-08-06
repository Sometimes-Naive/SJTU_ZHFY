#coding: utf-8
"""CourtDataVisualization overview module Utils

在此文件中定义一些可复用的对数据结构等的通用处理
还可以包含一些本模块中特有的数据处理逻辑中的原子环节
"""
import json
import sys, os, zipfile

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
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            # encoding='utf-8'
            data = json.load(f)
    except:
        with open(file_name, 'r', encoding='gbk') as f:
            data = json.load(f)
    return data


def dict_sorted(dict, label, reverse):
    #label 0表示按kay排序，1表示按values排序
    #reverse True为降序，False为升序
    sorted_tuple_data = sorted(dict.items(), key=lambda dict: dict[label], reverse=reverse)
    data = {}
    for i in sorted_tuple_data:
        data[i[0]] = i[1]
    return data, sorted_tuple_data

def list2dict(data):
        dict = {}
        for i in data:
            dict[i['name']] = i['value']
        return dict


def dict2list(data):
    region_key = list(data.keys())
    number = list(data.values())
    region_list = []
    for i in range(len(region_key)):
        # print(region_key[i])
        data_meta = {}
        data_meta['name'] = region_key[i]
        data_meta['value'] = number[i]
        # print(data)
        region_list.append(data_meta)
    return region_list

def info2str(info):
    str1 = ''
    for j in info:
        if str1 == '':
            str1 = j
        else:
            str1 = str1 + '\n' + j
    return str1

def unzip_single(src_file, dest_dir, password):
    ''' 解压单个文件到目标文件夹。
    '''
    if password:
        password = password.encode()
    zf = zipfile.ZipFile(src_file)
    try:
        zf.extractall(path=dest_dir, pwd=password)
    except RuntimeError as e:
        print(e)
    zf.close()

def unzip_all(source_dir, dest_dir, password):
    if not os.path.isdir(source_dir):    # 如果是单一文件
        unzip_single(source_dir, dest_dir, password)
    else:
        it = os.scandir(source_dir)
        dest_unzip_dir = ''
        for entry in it:
            print(entry.path)
            tail = entry.path.split('/')[-1].strip('.zip')
            dest_unzip_dir = dest_dir + '/' + tail
            print(dest_unzip_dir)
            if entry.is_file() and os.path.splitext(entry.name)[1]=='.zip' :
                unzip_single(entry.path, dest_unzip_dir, password)

def data_unzip():
    # 获取源路径和目标路径
    source_dir = "D:/工作/法院项目相关/数据相关/数据汇总0524/201801月收结存/"
    dest_dir = "D:/工作/法院项目相关/数据相关/数据汇总0524/收结存/2018/1月"
    password = None
    print(source_dir)
    print("源目录:", source_dir)
    print("解压到:", dest_dir)
    print("解压密码:", password)

    # 判断源路径是否合法
    if not os.path.exists(source_dir):
        print("压缩文件或压缩文件所在路径不存在！")
        exit()
    if not os.path.isdir(source_dir) and not zipfile.is_zipfile(source_dir):
        print("指定的源文件不是一个合法的.zip文件！")
        exit()

    # 如果解压到的路径不存在，则创建
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)

    unzip_all(source_dir, dest_dir, password)