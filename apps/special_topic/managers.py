#coding: utf-8
"""CourtDataVisualization special topic module data manager

在此文件中定义模块中数据的处理业务逻辑，是整个模块的功能核心所在。
在视图页面需要的数据通过调用本文件中的函数获取，
同时本文件负责从模型（models）中利用drivers获取原始数据。

可以直接定义数据处理函数，再遇到复杂逻辑时建议定义Manager类统筹管理。
定义类时需要注意访问控制，同时为保证每一个函数的易读性，每个函数长度不超过30行。

离婚纠纷类中离婚原因与判决结果两项中各项数据总和同应有总数据量不符；

修改核心思路：
1.将数据处理部分按照是否有读取数据库操作（预处理可以包括少量后续流程）分为预处理与处理；
2.将两个阶段处理的数据结果存储到json文件，view调用loader直接读取json数据；
3.每个预处理与处理部分按照网页布局与数据流程分为数据特征、当事人特征和专题特征；
4.减少代码冗余，增加复用，将刑事民事行政案件分三类建立manager，统一处理各自分类下的案件；
5.除以上，具体每个数据处理函数的逻辑几乎没有改动，仅做了一些语法上的精简，语义上的明确。

ps 为了便于调试 对查询数据库条数作了限制 更改请搜索“limit”
"""
import re, os

from core.drivers import connect_mongo
from .models import *
from .temp_data import *
from .utils import *
from .constants import *

TOPIC_TYPE_NUM = 0

class CivilDataProcessManager():
    """将原本整个数据处理分析流程分为两个部分；
    涉及到读取数据库的以及相关联的部分视作预处理，处理结果用json文件保存；
    剩余部分处理将预处理的结果统计打包成为展示的结构视作处理，结果同样用json文件保存；
    最终访问请求由loader处理，直接读取处理结果json文件。
    """

    def __init__(self):
        pass

    @connect_mongo(CIVIL_DATABASE_LIST[TOPIC_TYPE_NUM])
    def preprocess(self):

        for key, value in CIVIL_TOPIC_DICT.items():

            TOPIC_TYPE_NUM = value
            raw_region_info = self._preprocess_case_party_features_with_region_info()

            self._preprocess_case_quantity_features(raw_region_info)

            self._preprocess_case_typical_features()

        pass


    def run(self):
        for key, value in CIVIL_TOPIC_DICT.items():

            TOPIC_TYPE_NUM = value
            self._compose_case_party_data()

            self._compose_case_quantity_data()

            self._compose_case_typical_data()
        pass


    
    def _preprocess_case_quantity_features(self, raw_region_info):
        total_case_number = 85696
        # total_case_number = CIVIL_MODEL_LIST[type_number].objects.count()
        region_distribution = self._translate_court_name_2_region(raw_region_info)

        date_distribution = self._calculate_case_date_number()
        quantity_features = {
            'case_number': total_case_number,
            'case_region_number': region_distribution,
            'case_date_number': date_distribution,
        }
        json_data_w(quantity_features, os.path.join(PREPROCESS_DATA_PATH, CIVIL_TOPIC_DIRNAME[TOPIC_TYPE_NUM]) + os.sep + FILENAME_LIST[0])
        pass

    def _preprocess_case_party_features_with_region_info(self):
        raw_region_info, *raw_age_info, plaintiff_gender, defendant_gender = self._organize_raw_age_and_region_info()

        age_distribution = list(map(self._calculate_age_distribution, raw_age_info))

        # todo: 补充获取教育水平数据的逻辑 
        education_distribution = temp_divorce_dispute_party_education
        # todo: 补充获取工作行业数据的逻辑
        job_distribution = temp_divorce_dispute_party_vocation

        party_features = {
            'party_number': plaintiff_gender['男'] + plaintiff_gender['女'] + defendant_gender['男'] + defendant_gender['女'],
            'plaintiff_age': age_distribution[0], #'原告年龄分布'
            'plaintiff_male_age': age_distribution[2], #'原告男性年龄分布'
            'plaintiff_female_age': age_distribution[3], #'原告女性年龄分布'
            'defendant_age': age_distribution[1], #'被告年龄分布'
            'defendant_male_age': age_distribution[4], #'被告男性年龄分布'
            'defendant_female_age': age_distribution[5], #'被告女性年龄分布'
            'plaintiff_gender': plaintiff_gender, #原告性别分布
            'defendant_gender': defendant_gender, #被告性别分布
            'education': education_distribution,
            'job': job_distribution
        }
        json_data_w(party_features, os.path.join(PREPROCESS_DATA_PATH, CIVIL_TOPIC_DIRNAME[TOPIC_TYPE_NUM]) + os.sep + FILENAME_LIST[1])
        return raw_region_info

    def _preprocess_case_typical_features(self):

        if TOPIC_TYPE_NUM == 0:
            json_data_w({
                'marriage_duration': self._calculate_marriage_duration_dict(),
                'divorce_reason': self._calculate_divorce_reason_dict(),
                'judgement_result': self._calculate_judgement_result_dict()
                }, os.path.join(PREPROCESS_DATA_PATH, CIVIL_TOPIC_DIRNAME[TOPIC_TYPE_NUM]) + os.sep + FILENAME_LIST[2])
        pass

    def _compose_case_quantity_data(self):
        preprocessed = json_data_r(os.path.join(PREPROCESS_DATA_PATH, CIVIL_TOPIC_DIRNAME[TOPIC_TYPE_NUM]) + os.sep + FILENAME_LIST[0])
        map_data = self._compose_map_dict(preprocessed['case_region_number'])
        date_data = preprocessed['case_date_number']
        json_data_w({
            'case_number': preprocessed['case_number'],
            'case_map': map_data,
            'case_region_histogram': self._compose_region_histogram_data(map_data),
            'case_date_line': [list(date_data.keys()), list(date_data.values()), '离婚纠纷案件'],
        }, os.path.join(DATA_PATH, CIVIL_TOPIC_DIRNAME[TOPIC_TYPE_NUM]) + os.sep + FILENAME_LIST[0])
        pass

    def _compose_case_party_data(self):
        preprocessed = json_data_r(os.path.join(PREPROCESS_DATA_PATH, CIVIL_TOPIC_DIRNAME[TOPIC_TYPE_NUM]) + os.sep + FILENAME_LIST[1])
        
        age_pie_data = {
            'name': '当事人性别',
            'data':[{
                'name': '男性',
                'y': preprocessed['plaintiff_gender']['男'] + preprocessed['defendant_gender']['男']
            },{
                'name': '女性',
                'y': preprocessed['plaintiff_gender']['女'] + preprocessed['defendant_gender']['女']
            }]
        }
        json_data_w({
            'party_number': preprocessed['party_number'],
            'gender_pie': age_pie_data,
            'age_histogram': [
                list(preprocessed['plaintiff_age'].keys()),
                [x + list(preprocessed['defendant_age'].values())[index] for index, x in enumerate(list(preprocessed['plaintiff_age'].values()))]
            ],
            'education_pie': {
                'name': '当事人学历',
                'data': preprocessed['education']
            },
            'job_histogram': preprocessed['job'],
        }, os.path.join(DATA_PATH, CIVIL_TOPIC_DIRNAME[TOPIC_TYPE_NUM]) + os.sep + FILENAME_LIST[1])
        pass

    def _compose_case_typical_data(self):
        preprocessed = json_data_r(os.path.join(PREPROCESS_DATA_PATH, CIVIL_TOPIC_DIRNAME[TOPIC_TYPE_NUM]) + os.sep + FILENAME_LIST[2])
        if TOPIC_TYPE_NUM == 0:
            json_data_w({
                'duration_line': [
                    [x[0] for x in preprocessed['marriage_duration']],
                    [x[1] for x in preprocessed['marriage_duration']],
                    '离婚纠纷案件'
                ],
                'reason_pie': {
                    'name': '离婚原因',
                    'data': [dict(name=x, y=preprocessed['divorce_reason'][x]) for x in list(preprocessed['divorce_reason'])]
                },
                'result_pie': {
                    'name': '判决结果',
                    'data': [dict(name=x, y=preprocessed['judgement_result'][x]) for x in list(preprocessed['judgement_result'])]
                }}, os.path.join(DATA_PATH, CIVIL_TOPIC_DIRNAME[TOPIC_TYPE_NUM]) + os.sep + FILENAME_LIST[2])
        pass

    def _calculate_case_date_number(self):
        case_date_number = {
            '2018': 0,
            '2017': 0,
            '2016': 0
        }
        for i in CIVIL_MODEL_LIST[TOPIC_TYPE_NUM].objects[1:20]:# limit
            for j in i.尾部信息.split('、'):
                if ('年' in j) and ('月' in j) and ('日' in j) and ('二' in j):
                    if ('二○一八' in j) or ('二〇一八' in j):
                        case_date_number['2018'] += 1
                    elif ('二○一七' in j) or ('二〇一七' in j):
                        case_date_number['2017'] += 1
                    elif ('二○一六' in j) or ('二〇一六' in j):
                        case_date_number['2016'] += 1
                    break
        return case_date_number


    def _organize_raw_age_and_region_info(self):
        court = {}
        plaintiff_age_dict = {}
        defendant_age_dict = {}
        plaintiff_male_age_dict = {}
        defendant_male_age_dict = {}
        plaintiff_female_age_dict = {}
        defendant_female_age_dict = {}
        plaintiff_gender = {
            '男': 0,
            '女': 0
        }
        defendant_gender = {
            '男': 0,
            '女': 0
        }
        for i in CIVIL_MODEL_LIST[TOPIC_TYPE_NUM].objects[1:20]:# limit
            # 从头部信息中获取法院与地区信息
            if i.头部信息:
                for j in i.头部信息.split('、'):
                    if '法院' in j and len(j)<25 and 'X' not in j and 'x' not in j:
                        # print(i.头部信息).split('、')
                        a = j.replace('重庆市','').replace('×','').replace('-','').replace('\t','').replace('\\', '').replace('\xa0', '')
                        court[a] = court[a] + 1 if a in court.keys() else 1
                        break
            party_info = i.当事人信息.split('、')
            plaintiff = ''
            defendant = ''
            # print(party_info)
            if party_info:
                for j in party_info:
                    if any([(x in j) for x in PLAINTIFF_ALIAS_LIST]) and (not plaintiff) and (len(j) > 15):
                        plaintiff = j
                    elif any([(x in j) for x in DEFENDANT_ALIAS_LIST]) and (not defendant) and (len(j) > 15):
                        defendant = j
                # 若两条信息都有 先统计分性别的四种
                if plaintiff and defendant:
                    if '男' in plaintiff:
                        plaintiff_gender['男'] = plaintiff_gender['男'] + 1
                        m = re.split('[,，]', plaintiff)
                        # print(m)
                        for k in m:
                            if '年' in k and '月' in k:
                                plaintiff_male_birth = re.findall(r'(\d{4})年', k)
                                if plaintiff_male_birth:
                                    plaintiff_male_age = CURRENT_YEAR - int(plaintiff_male_birth[0])
                                if str(plaintiff_male_age) in plaintiff_male_age_dict:
                                    plaintiff_male_age_dict[str(plaintiff_male_age)] = plaintiff_male_age_dict[str(plaintiff_male_age)] + 1
                                elif (str(plaintiff_male_age) not in plaintiff_male_age_dict) and (plaintiff_male_age < 120) and (
                                        plaintiff_male_age > 10):
                                    plaintiff_male_age_dict[str(plaintiff_male_age)] = 1
                                break
                    elif '女' in plaintiff:
                        plaintiff_gender['女'] = plaintiff_gender['女'] + 1
                        m = re.split('[,，]', plaintiff)
                        for k in m:
                            if '年' in k and '月' in k:
                                plaintiff_female_birth = re.findall(r'(\d{4})年', k)
                                if plaintiff_female_birth:
                                    plaintiff_female_age = CURRENT_YEAR - int(plaintiff_female_birth[0])
                                if (str(plaintiff_female_age) in plaintiff_female_age_dict):
                                    plaintiff_female_age_dict[str(plaintiff_female_age)] = plaintiff_female_age_dict[str(plaintiff_female_age)] + 1
                                elif (str(plaintiff_female_age) not in plaintiff_female_age_dict) and (
                                        plaintiff_female_age < 120) and (plaintiff_female_age > 10):
                                    plaintiff_female_age_dict[str(plaintiff_female_age)] = 1
                                break
                    if '男' in defendant:
                        defendant_gender['男'] = defendant_gender['男'] + 1
                        m = re.split('[,，]', defendant)
                        for k in m:
                            if '年' in k and '月' in k:
                                defendant_male_birth = re.findall(r'(\d{4})年', k)
                                if defendant_male_birth:
                                    defendant_male_age = CURRENT_YEAR - int(defendant_male_birth[0])
                                if (str(defendant_male_age) in defendant_male_age_dict):
                                    defendant_male_age_dict[str(defendant_male_age)] = defendant_male_age_dict[str(defendant_male_age)] + 1
                                elif (str(defendant_male_age) not in defendant_male_age_dict) and (defendant_male_age < 120) and (
                                        defendant_male_age > 10):
                                    defendant_male_age_dict[str(defendant_male_age)] = 1
                                break
                    elif '女' in defendant:
                        defendant_gender['女'] = defendant_gender['女'] + 1
                        m = re.split('[,，]', defendant)
                        for k in m:
                            if '年' in k and '月' in k:
                                defendant_female_birth = re.findall(r'(\d{4})年', k)
                                if defendant_female_birth:
                                    defendant_female_age = CURRENT_YEAR - int(defendant_female_birth[0])
                                if (str(defendant_female_age) in defendant_female_age_dict):
                                    defendant_female_age_dict[str(defendant_female_age)] = defendant_female_age_dict[str(defendant_female_age)] + 1
                                elif (str(defendant_female_age) not in defendant_female_age_dict) and (
                                        defendant_female_age < 120) and (defendant_female_age > 10):
                                    defendant_female_age_dict[str(defendant_female_age)] = 1
            # 再统计不分性别的两种
            if plaintiff and defendant:
                m = re.split('[,，]', plaintiff)
                n = re.split('[,，]', defendant)
                for k in m:
                    if '年' in k and '月' in k:
                        plaintiff_birth = re.findall(r'(\d{4})年', k)
                        if plaintiff_birth:
                            plaintiff_age = CURRENT_YEAR - int(plaintiff_birth[0])
                        if (str(plaintiff_age) in plaintiff_age_dict):
                            plaintiff_age_dict[str(plaintiff_age)] = plaintiff_age_dict[str(plaintiff_age)] + 1
                        elif (str(plaintiff_age) not in plaintiff_age_dict) and (plaintiff_age < 120) and (plaintiff_age > 10):
                            plaintiff_age_dict[str(plaintiff_age)] = 1
                        break
                for k in n:
                    if '年' in k and '月' in k:
                        defendant_birth = re.findall(r'(\d{4})年', k)
                        if defendant_birth:
                            defendant_age = CURRENT_YEAR - int(defendant_birth[0])
                        if (str(defendant_age) in defendant_age_dict):
                            defendant_age_dict[str(defendant_age)] = defendant_age_dict[str(defendant_age)] + 1
                        elif (str(defendant_age) not in defendant_age_dict) and (defendant_age < 120) and (defendant_age > 10):
                            defendant_age_dict[str(defendant_age)] = 1
                        break
        return [court, plaintiff_age_dict, defendant_age_dict, plaintiff_male_age_dict, plaintiff_female_age_dict, defendant_male_age_dict, defendant_female_age_dict, plaintiff_gender, defendant_gender]


    def _calculate_age_distribution(self, age_dict):
        DICTAGE = {
            '20岁以下': 0,
            '20~30岁': 0,
            '31~40岁': 0,
            '41~50岁': 0,
            '51~60岁': 0,
            '61~70岁': 0,
            '70岁以上': 0,
        }
        for j,k in age_dict.items():
            if int(j)<20:
                DICTAGE['20岁以下'] = DICTAGE['20岁以下']+k
            elif int(j)>=20 and int(j)<=30:
                DICTAGE['20~30岁'] = DICTAGE['20~30岁'] +k
            elif int(j)>30 and int(j)<=40:
                DICTAGE['31~40岁'] = DICTAGE['31~40岁'] + k
            elif int(j)>40 and int(j)<=50:
                DICTAGE['41~50岁'] = DICTAGE['41~50岁'] + k
            elif int(j)>50 and int(j)<=60:
                DICTAGE['51~60岁'] = DICTAGE['51~60岁'] + k
            elif int(j)>60 and int(j)<=70:
                DICTAGE['61~70岁'] = DICTAGE['61~70岁'] + k
            elif int(j) > 70:
                DICTAGE['70岁以上'] = DICTAGE['70岁以上'] + k
        return DICTAGE


    def _translate_court_name_2_region(self, court_dict):
        # court_list = [('江津区人民法院', 4357), ('万州区人民法院', 4349), ('合川区人民法院', 3247), ('云阳县人民法院', 3210), ('綦江区人民法院', 3103), ('开州区人民法院', 3012), ('渝北区人民法院', 2925), ('沙坪坝区人民法院', 2716), ('巴南区人民法院', 2679), ('涪陵区人民法院', 2639), ('九龙坡区人民法院', 2580), ('彭水苗族土家族自治县人民法院', 2551), ('奉节县人民法院', 2507), ('永川区人民法院', 2454), ('大足区人民法院', 2223), ('北碚区人民法院', 2139), ('荣昌区人民法院', 2066), ('垫江县人民法院', 2063), ('巫山县人民法院', 1994), ('丰都县人民法院', 1981), ('铜梁区人民法院', 1868), ('梁平区人民法院', 1839), ('潼南区人民法院', 1803), ('南川区人民法院', 1748), ('长寿区人民法院', 1669), ('忠县人民法院', 1606), ('璧山区人民法院', 1590), ('南岸区人民法院', 1560), ('石柱土家族自治县人民法院', 1387), ('江北区人民法院', 1381), ('巫溪县人民法院', 1326), ('黔江区人民法院', 1246), ('渝中区人民法院', 1096), ('梁平县人民法院', 1014), ('酉阳土家族苗族自治县人民法院', 952), ('城口县人民法院', 943), ('秀山土家族苗族自治县人民法院', 941), ('大渡口区人民法院', 892), ('开县人民法院', 741), ('武隆区人民法院', 682), ('第一中级人民法院', 606), ('第五中级人民法院', 561), ('江津市人民法院', 555), ('武隆县人民法院', 460), ('第二中级人民法院', 342), ('荣昌县人民法院', 265), ('合川市人民法院', 231), ('第三中级人民法院', 177), ('人民法院', 169), ('璧山县人民法院', 161), ('第四中级人民法院', 113), ('高级人民法院', 97)]
        court_list = list(court_dict.items())
        region_dict = {}
        for court in court_list:
            m = court[0].replace('区','').replace('人民法院', '').replace('自治县', '').replace('市', '').replace('苗族', '').replace('土家族', '')
            if m == '第一中级':
                m = '渝北区'
            elif m == '第二中级':
                m = '万州区'
            elif m == '第三中级':
                m = '涪陵区'
            elif m == '第四中级':
                m = '黔江区'
            elif m == '第五中级':
                m = '渝中'
            elif m == '高级':
                m = '渝北区'
            for j in region_dict.keys():
                if m[:2] in j:
                    region_dict[j] = region_dict[j]+court[1]
                    m = ''
                    break
            if m:
                region_dict[m] = court[1]
        return region_dict


    def _compose_map_dict(self, region_info):
        map_dict = []
        # court = MsLhjfData().get_court_info()
        for i, j in region_info.items():
            node = {}
            if i != '酉阳' and i != '秀山' and '县' not in i and '区' not in i and len(i)<5:
                node['name'] = i+'区'
            else:
                node['name'] = i
            node['value'] = j
            # print(node)
            map_dict.append(node)
        return map_dict

    def _compose_region_histogram_data(self, map_data):
        region_case_pre_number = sorted(map_data, key=lambda y: y['value'], reverse=True)[:6]
        return [[x['name'] for x in region_case_pre_number], [x['value'] for x in region_case_pre_number]]
# **************************************************TOPIC ANALYSIS************************************************

    def _calculate_marriage_duration_dict(self):
        marriage_duration={}
        for i in CIVIL_MODEL_LIST[TOPIC_TYPE_NUM].objects()[1:20]:# limit
            a=i.庭审过程
            b=a.split('、')
            for j in b:
                if '结婚' in j and '年' in j:
                    c=re.split('，|。',j)
                    for k in c:
                        if '结婚' in k and '年' in k:
                            marriage_date = re.findall(r'(\d{4})年', k)
                            if marriage_date:
                                marriage_time = 2019 - int(marriage_date[0])
                                if str(marriage_time) in marriage_duration:
                                    marriage_duration[str(marriage_time)] = marriage_duration[str(marriage_time)]+1
                                elif str(marriage_time) not in marriage_duration:
                                    marriage_duration[str(marriage_time)] = 1
                        break
        marriage_duration=sorted(marriage_duration.items(), key=lambda e: int(e[0]), reverse=False)
        return(marriage_duration)

    #离婚原因
    def _calculate_divorce_reason_dict(self):
        divorce_reason={
                    '感情不和': 0,
                    '破裂': 0,
                    '家庭暴力': 0,
                    '家暴': 0,
                    '离家': 0,
                    '不归': 0,
                    '不良': 0,
                    '恶习': 0,
                    '重婚': 0,
                    '婚外情':0,
                    '生理缺陷': 0,
                    '缺陷': 0,
        }
        a=['感情不和','破裂','家庭暴力','家暴','离家','不归','不良','恶习','重婚','婚外情','生理缺陷','缺陷']
        for i in CIVIL_MODEL_LIST[TOPIC_TYPE_NUM].objects()[1:20]:# limit
            b = i.庭审过程
            for j in a:
                if j in b:
                    divorce_reason[j]=divorce_reason[j]+1
        return(divorce_reason)

    #判决结果
    def _calculate_judgement_result_dict(self):
        divorce_result = {'解除婚姻关系': 0, '维持婚姻关系': 0}
        for i in CIVIL_MODEL_LIST[TOPIC_TYPE_NUM].objects()[1:20]:# limit
            a = i.庭审过程
            b = a.split('、')
            for j in b:
                if j.endswith('判决如下：'):
                    c = b.index(j)
                    k1 = b[c + 1]
                    k2 = b[c + 2]
                    k3 = b[c + 3]
                    if '离婚' in k1 or '离婚' in k2 or '离婚' in k3:
                        divorce_result['解除婚姻关系'] = divorce_result['解除婚姻关系'] + 1
                    elif '撤诉' in k1 or '驳回' in k1 or '撤诉' in k2 or '驳回' in k2:
                        divorce_result['维持婚姻关系'] = divorce_result['维持婚姻关系'] + 1
        return divorce_result


class CriminalDataProcessManager():
    """将原本整个数据处理分析流程分为两个部分；
    涉及到读取数据库的以及相关联的部分视作预处理，处理结果用json文件保存；
    剩余部分处理将预处理的结果统计打包成为展示的结构视作处理，结果同样用json文件保存；
    最终访问请求由loader处理，直接读取处理结果json文件。
    """

    def __init__(self):
        pass

    @connect_mongo(CRIMINAL_DATABASE_LIST[TOPIC_TYPE_NUM])
    def preprocess(self):

        for key, value in CRIMINAL_TOPIC_DICT.items():

            TOPIC_TYPE_NUM = value

            self._preprocess_quantity_features()
            
            self._preprocess_accused_features()

            self._preprocess_typical_features()

        return self


    def run(self):
        for key, value in CRIMINAL_TOPIC_DICT.items():

            TOPIC_TYPE_NUM = value
            self._compose_case_accused_data()

            self._compose_case_quantity_data()

            self._compose_case_typical_data()
        
        return self


    def _preprocess_quantity_features(self):

        # case_number = CRIMINAL_MODEL_LIST[TOPIC_TYPE_NUM].objects(Q(案由=CRIMINAL_CASE_CAUSE_LIST[TOPIC_TYPE_NUM])).count()
        case_number = 20
        map_data = self._translate_court_2_region_name(self._fetch_court_info())
        # his_row_data = XsWxjsData().get_his_row_data(map_data)
        date_distribution = self._calculate_case_date_number()
        json_data_w({
            'case_number': case_number,
            'case_map': map_data,
            'case_date_data': date_distribution,
        }, os.path.join(PREPROCESS_DATA_PATH, CRIMINAL_TOPIC_DIRNAME[TOPIC_TYPE_NUM]) + os.sep + FILENAME_LIST[0])
        pass

    def _preprocess_accused_features(self):

        accused_info = self._organize_accused_info()
        accused_gender = self._extract_accused_gender_info(accused_info)
        accused_age = self._extract_accused_age_info(accused_info)
        accused_education = self._extract_accused_education_info(accused_info)
        accused_job = self._fetch_accused_job()
        # accused_job = [['无业游民', '工人', '自营业主', '教师', '医生', '农民'], [773, 64, 89, 6, 7, 426]]
        json_data_w({
            'number': len(accused_info),  # 当事人性别信息
            'gender': accused_gender,# 职业分布
            'age': accused_age,  # 教育程度
            'education': accused_education,  # 年龄信息
            'job': accused_job,  # 年龄信息
        }, os.path.join(PREPROCESS_DATA_PATH, CRIMINAL_TOPIC_DIRNAME[TOPIC_TYPE_NUM]) + os.sep + FILENAME_LIST[1])
        pass

    def _preprocess_typical_features(self):

        json_data_w({
            'fine_number': self._fetch_fine_number(),
            'imprisonment_term': self._fetch_imprisonment_term(),
            'alcohol_amount': self._fetch_tested_alcohol_amount(),
        }, os.path.join(PREPROCESS_DATA_PATH, CRIMINAL_TOPIC_DIRNAME[TOPIC_TYPE_NUM]) + os.sep + FILENAME_LIST[2])
        pass

    def _compose_case_quantity_data(self):
        
        preprocessed = json_data_r(os.path.join(PREPROCESS_DATA_PATH, CRIMINAL_TOPIC_DIRNAME[TOPIC_TYPE_NUM]) + os.sep + FILENAME_LIST[0])

        json_data_w({
            'case_number': preprocessed['case_number'],
            'case_map': preprocessed['case_map'],
            'case_region_histogram': [
                [x['name'] for x in preprocessed['case_map']][:5],
                [x['value'] for x in preprocessed['case_map']][:5]
            ],
            'case_date_line': preprocessed['case_date_data'],
        }, os.path.join(DATA_PATH, CRIMINAL_TOPIC_DIRNAME[TOPIC_TYPE_NUM]) + os.sep + FILENAME_LIST[0])
        pass

    def _compose_case_accused_data(self):
        
        preprocessed = json_data_r(os.path.join(PREPROCESS_DATA_PATH, CRIMINAL_TOPIC_DIRNAME[TOPIC_TYPE_NUM]) + os.sep + FILENAME_LIST[1])

        json_data_w({
            'accused_number': preprocessed['number'],  # 当事人性别信息
            'accused_gender_pie': preprocessed['gender'],# 职业分布
            'accused_age_histogram': preprocessed['age'],  # 教育程度
            'accused_education_pie': preprocessed['education'],  # 年龄信息
            'accused_job_histogram': [
                [x[0] for x in list(preprocessed['job'].items())],
                [x[1] for x in list(preprocessed['job'].items())]
            ],  # 年龄信息
        }, os.path.join(DATA_PATH, CRIMINAL_TOPIC_DIRNAME[TOPIC_TYPE_NUM]) + os.sep + FILENAME_LIST[1])
        pass

    def _compose_case_typical_data(self):
        
        preprocessed = json_data_r(os.path.join(PREPROCESS_DATA_PATH, CRIMINAL_TOPIC_DIRNAME[TOPIC_TYPE_NUM]) + os.sep + FILENAME_LIST[2])

        json_data_w({
            'imprisonment_term_pie': self._compose_case_imprisonment_term(preprocessed['imprisonment_term']),
            'fine_number_pie': self._compose_case_fine(preprocessed['fine_number']),
            'alcohol_amount_pie': preprocessed['alcohol_amount'],
        }, os.path.join(DATA_PATH, CRIMINAL_TOPIC_DIRNAME[TOPIC_TYPE_NUM]) + os.sep + FILENAME_LIST[2])
        pass

    def _fetch_court_info(self):
        court = {}
        for i in CRIMINAL_MODEL_LIST[TOPIC_TYPE_NUM].objects(Q(案由=CRIMINAL_CASE_CAUSE_LIST[TOPIC_TYPE_NUM]))[:20]:# limit
            court[i.法院名称] = court[i.法院名称] + 1 if i.法院名称 in list(court.keys()) else 1
        return sorted(court.items(), key=lambda k: k[1], reverse=True)


    def _translate_court_2_region_name(self, court_data):
        region = {}
        for court in court_data:
            m = court[0].replace('区', '').replace('重庆市', '').replace('人民法院', '').replace('自治县', '').replace('市', '').replace('苗族', '').replace('土家族', '').replace('中华人民共和国', '')
            if m == '第一中级':
                m = '渝北'
            elif m == '第二中级':
                m = '万州'
            elif m == '第三中级':
                m = '涪陵'
            elif m == '第四中级':
                m = '黔江'
            elif m == '第五中级':
                m = '渝中'
            elif m == '高级':
                m = '渝北'
            for j in region.keys():
                if m[:2] in j:
                    region[j] = region[j] + court[1]
                    m = ''
                    break
            if m:
                region[m] = court[1]
        map_dict = []
        for key, value in region.items():
            map_dict.append({
                'name': (key + '区') if (key != '酉阳' and key != '秀山' and '县' not in key and '区' not in key and len(key)<5) else key,
                'value': value
            })
        return map_dict



    def _calculate_case_date_number(self):
        date_dict, date = {}, ''
        for i in CRIMINAL_MODEL_LIST[TOPIC_TYPE_NUM].objects(Q(案由=CRIMINAL_CASE_CAUSE_LIST[TOPIC_TYPE_NUM]))[:20]:# limit
            headers = i.头部信息.split('、')
            for j in headers:
                if '（20' in j:
                    date = str(j.split('）')[0].replace('（', '')) + '年'
            if (date not in date_dict.keys()) and (len(date) < 7):
                date_dict[date] = 1
            elif date in date_dict.keys():
                date_dict[date] += 1
        date_tuple = sorted(date_dict.items(), key=lambda k: k[0])
        return [[x[0] for x in date_tuple], [x[1] for x in date_tuple]]


    def _organize_accused_info(self):
        info = []
        for i in CRIMINAL_MODEL_LIST[TOPIC_TYPE_NUM].objects(Q(案由=CRIMINAL_CASE_CAUSE_LIST[TOPIC_TYPE_NUM]))[:20]:# limit
            accused = i.当事人信息.split('、')
            for j in accused:
                if any([(x in j) for x in ACCUSED_ALIAS_LIST]) and ('男，' in j or '女，' in j):
                    c = {'name': '未知', 'gender': '未知', 'birthdate': '未知', 'address': '未知', 'age': '未知', 'nation': '未知', 'education': '未知'}
                    if ',' in j or '，' in j :
                        e = re.split('，| ，|。', j)
                        b = []
                        for i in e:
                            for w in i.split(','):
                                b.append(w)
                        c['name'] = b[0].replace('被告人','').replace('罪犯', '').replace('上诉人（原审）', '').replace('上诉人(原审)', '').replace('被告:', '').replace('被告', '')
                        for k in b:
                            if '男'in k or '女' in k:
                                c['gender'] = k
                                # break
                            elif '出生' in k:
                                k1 = k.split('出生')
                                c['birthdate'] = k1[0]
                                if k1[1]:
                                    c['address'] = re.sub('于','',k1[1])
                                if c['birthdate'][:4].isdigit() :
                                    c['age'] = str(CURRENT_YEAR - int(c['birthdate'][:4]))
                            elif '族' in k and len(k)<6:
                                c['nation'] = k
                            elif '文化' in k and len(k)<6:
                                c['education'] = k
                            elif '文盲' in k and len(k)<6:
                                c['education'] = k
                        info.append(c)
                        break
        return info

    def _fetch_accused_job(self):
        jobs = {'无业游民': 0, '工人': 0, '自营业主': 0, '教师': 0, '医生': 0, '农民': 0}
        for case in CRIMINAL_MODEL_LIST[TOPIC_TYPE_NUM].objects(Q(案由=CRIMINAL_CASE_CAUSE_LIST[TOPIC_TYPE_NUM]))[:20]:# limit
            infos = case.当事人信息.split('、')
            # print(a)
            for segment in infos:
                if ('被告人' in segment or '被告' in segment) and ('男，' in segment or '女，' in segment):
                    c = {'edu': '未知'}
                    if ',' in segment or '，' in segment:
                        subsegs = segment.split('，')
                        b = []
                        for seg in subsegs:
                            for w in seg.split(','):
                                b.append(w)
                        for k in b:
                            if '无业' in k and len(k) < 6:
                                jobs['无业游民'] += 1
                            elif '工人' in k and len(k) < 6:
                                jobs['工人'] += 1
                            elif '公司' in k and len(k) < 6:
                                jobs['自营业主'] += 1
                            elif '教师' in k and len(k) < 6:
                                jobs['教师'] += 1
                            elif '医生' in k and len(k) < 6:
                                jobs['医生'] += 1
                            elif '农民' in k and len(k) < 6:
                                jobs['农民'] += 1
        return jobs

    def _extract_accused_gender_info(self, accused_info):
        result = {
            '男': 0,
            '女': 0,
            '未知': 0,
        }
        for info in accused_info:
            if info['gender'] == '男':
                result['男'] = result['男'] + 1
            elif info['gender'] == '女':
                result['女'] = result['女'] + 1
            else:
                result['未知'] = result['未知'] + 1
        return [dict(name=x[0], y=x[1]) for x in list(result.items())]


    def _extract_accused_age_info(self, accused_info):
        age = {
            '未知': 0,
            '20岁以下': 0,
            '21岁~30岁': 0,
            '31岁~40岁': 0,
            '41岁~50岁': 0,
            '51岁~60岁': 0,
            '60岁以上': 0,
        }
        for info in accused_info:
            if info['age'] == '未知':
                age['未知'] = age['未知'] + 1
            elif info['age'] <= '20':
                age['20岁以下'] = age['20岁以下'] + 1
            elif info['age'] <= '30':
                age['21岁~30岁'] = age['21岁~30岁'] + 1
            elif info['age'] <= '40':
                age['31岁~40岁'] = age['31岁~40岁'] + 1
            elif info['age'] <= '50':
                age['41岁~50岁'] = age['41岁~50岁'] + 1
            elif info['age'] <= '60':
                age['51岁~60岁'] = age['51岁~60岁'] + 1
            else:
                age['60岁以上'] = age['60岁以上'] + 1
        return [list(age.keys()), list(age.values())]

    def _extract_accused_education_info(self, accused_info):
        level = {
            '未知': 0,
            '文盲': 0,
            '小学文化': 0,
            '中学文化': 0,
            '高中文化': 0,
            '大专文化': 0,
            '本科文化': 0,
            '研究生文化': 0,
        }
        for info in accused_info:
            if info['education'] == '未知':
                level['未知'] = level['未知'] + 1
            elif info['education'] == '文盲':
                level['文盲'] = level['文盲'] + 1
            elif info['education'] in ['小学文化。', '小学文化']:
                level['小学文化'] = level['小学文化'] + 1
            elif info['education'] in ['初中文化。', '初中文化', '中学文化', '中技文化']:
                level['中学文化'] = level['中学文化'] + 1
            elif info['education'] in ['高中文化', '中专文化', '中专文化。', '高中文化。', '职高文化']:
                level['高中文化'] = level['高中文化'] + 1
            elif info['education'] in ['大专文化', '专科文化', '大专文化。']:
                level['大专文化'] = level['大专文化'] + 1
            elif info['education'] in ['大学文化', '本科文化', '本科文化。', '大学文化。', '大学本科文化']:
                level['本科文化'] = level['本科文化'] + 1
            elif info['education'] in ['研究生文化']:
                level['研究生文化'] = level['研究生文化'] + 1
        return [dict(name=x[0], y=x[1]) for x in list(level.items())]



######################################TOPIC FEATURES###############################################
    def _fetch_imprisonment_term(self):
        prison = []
        for case in CRIMINAL_MODEL_LIST[TOPIC_TYPE_NUM].objects(Q(案由=CRIMINAL_CASE_CAUSE_LIST[TOPIC_TYPE_NUM]))[:20]:# limit
            for description in case.庭审过程.split('、'):
                if '被告人' in description:
                    for segments in re.split('[,，；]', description):
                        if '判处' in segments:
                            date = ''
                            if re.findall(r'判处(.*?)月',segments):
                                date = re.findall(r'判处(.*?)月',segments)[0]
                                date = date+'月'
                            elif re.findall(r'判处(.*?)年',segments):
                                date = re.findall(r'判处(.*?)年', segments)[0]
                                date = date + '年'
                            elif re.findall(r'判处(.*?)刑', segments):
                                sentence = re.findall(r'判处(.*?)刑', segments)[0]
                                if '死' in sentence:
                                    date = '死刑'
                                elif '无期徒' in sentence:
                                    date = '无期徒刑'
                            if len(date)<=10 and date and ('�' not in date) and ('的' not in date) and ('被告人' not in date):
                                if date.startswith('拘') or date.startswith('有'):
                                    prison.append(date)
        return prison

    def _fetch_fine_number(self):
        fine = []
        for case in CRIMINAL_MODEL_LIST[TOPIC_TYPE_NUM].objects(Q(案由=CRIMINAL_CASE_CAUSE_LIST[TOPIC_TYPE_NUM]))[:20]:# limit
            for procedures in case.庭审过程.split('、'):
                if '被告人' in procedures:
                    for segments in re.split('[,，；]',procedures):
                        # print(k)
                        if '罚金' in segments and '�' not in segments:
                            # print(k)
                            if re.findall(r'罚金(.*?)元', segments):
                                # print(str(re.findall(r'罚金(.*?)元',k)[0]).replace('人民币',''))
                                num = str(re.findall(r'罚金(.*?)元', segments)[0]).replace('人民币', '').replace('人币', '').replace('人民', '')
                                if 0 < len(num) <= 6:
                                    fine.append(num)
                            elif bool(re.findall(r'处罚金(.*?)。', segments)):
                                # print(str(re.findall(r'处罚金(.*?)。', k)[0]))
                                num = str(re.findall(r'处罚金(.*?)。', segments)[0]).replace('人民币', '')
                                if 0 < len(num) <= 6:
                                    fine.append(num)
        fine_re = []
        for l in fine:
            if l.isdigit():
                fine_re.append(int(l))
            elif not re.compile(u'[^\u4e00-\u9fa5]').search(l):
                if '在' not in l and '各' not in l and '限' not in l and '的' not in l and '至' not in l and '已' not in l:
                    p = chinese_to_arabic(l)
                    fine_re.append(p)
        return fine_re


    def _fetch_tested_alcohol_amount(self):
        alcohol = []
        count = 0
        for case in CRIMINAL_MODEL_LIST[TOPIC_TYPE_NUM].objects(Q(案由=CRIMINAL_CASE_CAUSE_LIST[TOPIC_TYPE_NUM]))[:20]:# limit
            procedures = case.庭审过程
            segments = procedures.split('，')
            for line in segments:
                if '乙醇' in line:
                    digit = re.findall('(\d+)', line)
                    if digit:
                        alcohol.append(float(digit[0]))
                    else:
                        count += 1
        alcohol.sort()
        alcohol_amount = {
            '80mg~100mg': 0,
            '101mg~150mg': 0,
            '151mg~200mg': 0,
            '201mg~250mg': 0,
            '251mg~300mg': 0,
            '301mg及以上': 0,
        }
        for num in alcohol:
            if num <= 100:
                alcohol_amount['80mg~100mg'] = alcohol_amount['80mg~100mg'] + 1
            elif num <= 150:
                alcohol_amount['101mg~150mg'] = alcohol_amount['101mg~150mg'] + 1
            elif num <= 200:
                alcohol_amount['151mg~200mg'] = alcohol_amount['151mg~200mg'] + 1
            elif num <= 250:
                alcohol_amount['201mg~250mg'] = alcohol_amount['201mg~250mg'] + 1
            elif num <= 300:
                alcohol_amount['251mg~300mg'] = alcohol_amount['251mg~300mg'] + 1
            else:
                alcohol_amount['301mg及以上'] = alcohol_amount['301mg及以上'] + 1
        return [dict(name=x[0], y=x[1]) for x in list(alcohol_amount.items())]

    def _compose_case_imprisonment_term(self, term_length):
        d = {}
        for i in term_length:
            d[i] = d[i] + 1 if i in list(d.keys()) else 1
        # d= sorted(d.items(),key=lambda x:x[1],reverse=True)
        return [dict(name=x[0], y=x[1]) for x in list(d.items())]


    def _compose_case_fine(self, fine_number):
        d = {
            '少于1000元': 0,
            '1001元~5000元': 0,
            '5001元~10000元': 0,
            '10001元~20000元': 0,
            '20001元~30000元': 0,
            '30000元以上': 0,
        }
        for i in fine_number:
            if i <= 1000:
                d['少于1000元'] = d['少于1000元'] + 1
            elif i <= 5000:
                d['1001元~5000元'] = d['1001元~5000元'] + 1
            elif i <= 10000:
                d['5001元~10000元'] = d['5001元~10000元'] + 1
            elif i <= 20000:
                d['10001元~20000元'] = d['10001元~20000元'] + 1
            elif i <= 30000:
                d['20001元~30000元'] = d['20001元~30000元'] + 1
            elif i > 30000:
                d['30000元以上'] = d['30000元以上'] + 1
        return [dict(name=x[0], y=x[1]) for x in list(d.items())]
       