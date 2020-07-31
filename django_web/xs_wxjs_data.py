#coding: utf-8
from django_web.models import XSAJ
import re
from mongoengine import *

class XsWxjsData:
    def __init__(self):
        CN_NUM = {
            '〇': 0, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '零': 0,
            '壹': 1, '贰': 2, '叁': 3, '肆': 4, '伍': 5, '陆': 6, '柒': 7, '捌': 8, '玖': 9, '貮': 2, '两': 2,
        }
        CN_UNIT = {
            '十': 10,
            '拾': 10,
            '百': 100,
            '佰': 100,
            '千': 1000,
            '仟': 1000,
            '万': 10000,
            '萬': 10000,
            '亿': 100000000,
            '億': 100000000,
            '兆': 1000000000000,
        }
        self.CN_NUM = CN_NUM
        self.CN_UNIT = CN_UNIT

    def get_defendant_info(self, AY_str):
        d = []
        # print(str)
        for i in XSAJ.objects(Q(案由=AY_str,文书类型='判决书')):
            a = i.当事人.split('、')
            # print(a)
            for j in a:
                if ('被告人' in j or '罪犯' in j or '被告' in j)and('男，' in j or '女，' in j):
                    c = {
                        'name':'未知','sex':'未知','birthdate':'未知','addr':'未知','age':'未知','nation':'未知','edu':'未知'
                    }
                    # print(j)
                    if ',' in j or '，' in j :
                        e = j.split('，')
                        b = []
                        for i in e:
                            for w in i.split(','):
                                b.append(w)
                        b[0] = b[0].replace('被告人','')
                        b[0] = b[0].replace('罪犯', '')
                        b[0] = b[0].replace('上诉人（原审）', '')
                        b[0] = b[0].replace('上诉人(原审)', '')
                        b[0] = b[0].replace('被告:', '')
                        b[0] = b[0].replace('被告', '')
                        c['name'] = b[0]
                        # print(b)
                        for k in b:
                            if '男'in k or '女' in k:
                                c['sex'] = k
                                # break
                            elif '出生' in k:
                                k1 = k.split('出生')
                                c['birthdate'] = k1[0]
                                if k1[1]:
                                    c['addr'] = re.sub('于','',k1[1])
                                if (c['birthdate'][:4].isdigit()) :
                                    c['age'] = str(2019 - int(c['birthdate'][:4]))
                                # break
                            elif '族' in k and len(k)<6:
                                c['nation'] = k
                                # break
                            elif '文化' in k and len(k)<6:
                                c['edu'] = k
                            elif '文盲' in k and len(k)<6:
                                c['edu'] = k
                                # break

                        d.append(c)
                        break
        return d

    def chinese_to_arabic(self, cn: str) -> int:
        unit = 0  # current
        ldig = []  # digest
        for cndig in reversed(cn):
            if cndig in self.CN_UNIT:
                unit = self.CN_UNIT.get(cndig)
                if unit == 10000 or unit == 100000000:
                    ldig.append(unit)
                    unit = 1
            else:
                dig = self.CN_NUM.get(cndig)
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

    def prison_date(self, AY_str):
        prison = []
        for i in XSAJ.objects(Q(案由=AY_str)):
            for j in i.判决结果.split('、'):
                if '被告人' in j:
                    for k in re.split('[,，；]', j):
                        if '判处' in k:
                            # print(k)
                            date = ''
                            if re.findall(r'判处(.*?)月',k):
                                date = re.findall(r'判处(.*?)月',k)[0]
                                date = date+'月'
                            elif re.findall(r'判处(.*?)年',k):
                                date = re.findall(r'判处(.*?)年', k)[0]
                                date = date + '年'
                            elif re.findall(r'判处(.*?)刑', k):
                                date1 = re.findall(r'判处(.*?)刑', k)[0]
                                if '死' in date1:
                                    date = '死刑'
                                elif '无期徒' in date1:
                                    date = '无期徒刑'
                            if len(date)<=10 and date and ('�' not in date) and ('的' not in date) and ('被告人' not in date):
                                # print(date)
                                prison.append(date)
        return prison

    def money_AJ(self, AY_str):
        money = []
        for i in XSAJ.objects(Q(案由=AY_str)):
            for j in i.判决结果.split('、'):
                if '被告人' in j:
                    for k in re.split('[,，；]',j):
                        # print(k)
                        if '罚金' in k and '�' not in k:
                            # print(k)
                            if re.findall(r'罚金(.*?)元',k):
                                # print(str(re.findall(r'罚金(.*?)元',k)[0]).replace('人民币',''))
                                str1 = str(re.findall(r'罚金(.*?)元', k)[0]).replace('人民币', '')
                                str1 = str1.replace('人币', '')
                                money.append(str1.replace('人民', ''))
                            elif bool(re.findall(r'处罚金(.*?)。',k)):
                                # print(str(re.findall(r'处罚金(.*?)。', k)[0]))
                                money.append(str(re.findall(r'处罚金(.*?)。', k)[0]).replace('人民币', ''))
        # print(money)
        money_re = []
        for l in money:
            # print(l)
            if l.isdigit():
                # print()
                money_re.append(int(l))
            elif not re.compile(u'[^\u4e00-\u9fa5]').search(l):
                # print(l)
                p = XsWxjsData().chinese_to_arabic(l)
                # print(p)
                money_re.append(p)
        return money_re

    def get_case_sex_number(self, WXJSdefendant_info):
        count = 0
        b = {
            '男': 0,
            '女': 0,
            '未知': 0,
        }
        WXJSSEX = []

        for sex in WXJSdefendant_info:
            # print(sex['sex'])
            if sex['sex'] == '男':
                b['男'] = b['男'] + 1
            elif sex['sex'] == '女':
                b['女'] = b['女'] + 1
            else:
                b['未知'] = b['未知'] + 1
        # print(b)
        for bl in b:
            # print(bl)
            c = {}
            c['name'] = bl
            c['y'] = b[bl]
            WXJSSEX.append(c)
        return WXJSSEX

    def get_case_age_number(self, WXJSdefendant_info):
        WXJSAGE = []
        c = {
            '未知': 0,
            '20岁以下': 0,
            '21岁~30岁': 0,
            '31岁~40岁': 0,
            '41岁~50岁': 0,
            '51岁~60岁': 0,
            '60岁以上': 0,
        }
        for i in WXJSdefendant_info:
            if i['age'] == '未知':
                c['未知'] = c['未知'] + 1
            elif i['age'] <= '20':
                c['20岁以下'] = c['20岁以下'] + 1
            elif i['age'] <= '30':
                c['21岁~30岁'] = c['21岁~30岁'] + 1
            elif i['age'] <= '40':
                c['31岁~40岁'] = c['31岁~40岁'] + 1
            elif i['age'] <= '50':
                c['41岁~50岁'] = c['41岁~50岁'] + 1
            elif i['age'] <= '60':
                c['51岁~60岁'] = c['51岁~60岁'] + 1
            else:
                c['60岁以上'] = c['60岁以上'] + 1
        # print(c)
        WXJSAGE = []
        WXJSAGE.append(list(c.keys()))
        WXJSAGE.append(list(c.values()))
        return WXJSAGE

    def get_case_edu_number(self, WXJSdefendant_info):
        WXJSEDU = []
        c = {
            '未知': 0,
            '文盲': 0,
            '小学文化': 0,
            '中学文化': 0,
            '高中文化': 0,
            '大专文化': 0,
            '本科文化': 0,
            '研究生文化': 0,
        }

        for i in WXJSdefendant_info:
            if i['edu'] == '未知':
                c['未知'] = c['未知'] + 1
            elif i['edu'] == '文盲':
                c['文盲'] = c['文盲'] + 1
            elif i['edu'] in ['小学文化。', '小学文化']:
                c['小学文化'] = c['小学文化'] + 1
            elif i['edu'] in ['初中文化。', '初中文化', '中学文化', '中技文化']:
                c['中学文化'] = c['中学文化'] + 1
            elif i['edu'] in ['高中文化', '中专文化', '中专文化。', '高中文化。', '职高文化']:
                c['高中文化'] = c['高中文化'] + 1
            elif i['edu'] in ['大专文化', '专科文化', '大专文化。']:
                c['大专文化'] = c['大专文化'] + 1
            elif i['edu'] in ['大学文化', '本科文化', '本科文化。', '大学文化。', '大学本科文化']:
                c['本科文化'] = c['本科文化'] + 1
            elif i['edu'] in ['研究生文化']:
                c['研究生文化'] = c['研究生文化'] + 1
        for cl in c:
            # print(bl)
            d = {}
            d['name'] = cl
            d['y'] = c[cl]
            WXJSEDU.append(d)
        return WXJSEDU

    def get_case_sentence_date_number(self, WXJSprison_date_info):
        WXJSPDATE = []
        d = {}
        for i in WXJSprison_date_info:
            if i not in WXJSPDATE:
                WXJSPDATE.append(i)
                d[i] = 1
            else:
                d[i] = d[i] + 1
        # d= sorted(d.items(),key=lambda x:x[1],reverse=True)

        WXJSPDATE = []
        for cl in d:
            # print(bl)
            c = {}
            c['name'] = cl
            c['y'] = d[cl]
            WXJSPDATE.append(c)
        return WXJSPDATE

    def get_case_alcohol_amount(self):
        alcohol = []
        count = 0
        for i in XSAJ.objects(Q(案由='危险驾驶罪')):
            k = re.findall(r'(\d{1,4}|[1-9]\d*\.\d*|0\.\d*[1-9]\d*)mg', i.庭审过程, flags=0)
            # k1 = re.findall(r'(\d{1,4}|[1-9]\d*\.\d*|0\.\d*[1-9]\d*)mg/(\d{3})ml', i.庭审过程, flags=0)
            if k:
                # print(k)
                alcohol.append(float(k[-1]))
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
        for a in alcohol:
            if a <= 100:
                alcohol_amount['80mg~100mg'] = alcohol_amount['80mg~100mg'] + 1
            elif a <= 150:
                alcohol_amount['101mg~150mg'] = alcohol_amount['101mg~150mg'] + 1
            elif a <= 200:
                alcohol_amount['151mg~200mg'] = alcohol_amount['151mg~200mg'] + 1
            elif a <= 250:
                alcohol_amount['201mg~250mg'] = alcohol_amount['201mg~250mg'] + 1
            elif a <= 300:
                alcohol_amount['251mg~300mg'] = alcohol_amount['251mg~300mg'] + 1
            else:
                alcohol_amount['301mg及以上'] = alcohol_amount['301mg及以上'] + 1
        # print(alcohol_amount)
        ALA = []
        for al in alcohol_amount:
            b = {}
            b['name'] = al
            b['y'] = alcohol_amount[al]
            ALA.append(b)
        return ALA

    def get_case_money(self, WXJSajmoney):
        WXJSAJMON = []
        d = {
            '少于1000元': 0,
            '1001元~5000元': 0,
            '5001元~10000元': 0,
            '10001元~20000元': 0,
            '20001元~30000元': 0,
            '30000元以上': 0,
        }
        for i in WXJSajmoney:
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

        for cl in d:
            # print(bl)
            c = {}
            c['name'] = cl
            c['y'] = d[cl]
            WXJSAJMON.append(c)
        return WXJSAJMON

    def get_court_pre_info(self):
        court = {}
        for i in XSAJ.objects(Q(案由='危险驾驶罪', 文书类型='判决书')):
            if i.法院 in list(court.keys()):
                court[i.法院] += 1
            else:
                court[i.法院] = 1
        court_pre = sorted(court.items(), key=lambda k: k[1], reverse=True)
        return court_pre

    def get_court_info(self):
        # court = get_age_info()[0]
        court_pre = XsWxjsData().get_court_pre_info()
        # [('重庆市北碚区人民法院', 707), ('重庆市万州区人民法院', 664), ('重庆市渝中区人民法院', 646), ('重庆市涪陵区人民法院', 444), ('重庆市高级人民法院', 6)]
        court = {}
        for i in court_pre:
            m = i[0].replace('人民法院', '')
            m = m.replace('重庆市', '')
            # print(court)
            if m == '第一中级':
                m = '渝北区'
            elif m == '第二中级':
                m = '万州区'
            elif m == '第三中级':
                m = '涪陵区'
            elif m == '第四中级':
                m = '黔江区'
            elif m == '第五中级':
                pass
            elif m == '高级':
                m = '渝北区'
            for j in court.keys():
                if m[:2] in j:
                    court[j] = court[j] + i[1]
                    m = ''
                    break
            if m:
                court[m] = i[1]
        return court

    def get_map_data(self, court_l_data):
        map_data = []
        for i in court_l_data.keys():
            map_meta_data = {}
            map_meta_data['name'] = i
            map_meta_data['value'] = court_l_data[i]
            map_data.append(map_meta_data)
        return map_data

    def get_his_row_data(self, map_data):
        his_row_data = []
        his_region_data = []
        his_number_data = []
        for i in map_data:
            his_region_data.append(i['name'])
            his_number_data.append(i['value'])
        his_row_data = [his_region_data, his_number_data]
        return his_row_data

    def get_case_date_number(self):
        case_date_number = {
            '2018': 0,
            '2017': 0,
            '2016': 0
        }
        for i in XSAJ.objects(Q(案由='危险驾驶罪', 文书类型='判决书')):
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

    def get_line_data(self):
        line_data_dict = {}
        for i in XSAJ.objects(Q(案由='危险驾驶罪', 文书类型='判决书')):
            date = str(i.案号.split('）')[0].replace('（', '')) + '年'
            if (date not in line_data_dict.keys()) and (len(date) < 7):
                line_data_dict[date] = 1
            elif date in line_data_dict.keys():
                line_data_dict[date] += 1
        line_data_tuple = sorted(line_data_dict.items(), key=lambda k: k[0])
        line_data = [[], []]
        for i in line_data_tuple:
            line_data[0].append(i[0])
            line_data[1].append(i[1])
        return line_data

class ChartRegion:
    def __init__(self, defendant_info):
        self.defendant_info = defendant_info

    def get_Fchart_data(self):
        WXJSpnumber = len(self.defendant_info)
        WXJScasenum = XSAJ.objects(Q(案由='危险驾驶罪', 文书类型='判决书')).count()
        court_data = XsWxjsData().get_court_info()
        map_data = XsWxjsData().get_map_data(court_data)
        his_row_data = XsWxjsData().get_his_row_data(map_data)
        line_data = XsWxjsData().get_line_data()
        Fchart_data = {
            'WXJSpnumber': WXJSpnumber,
            'WXJScasenum': WXJScasenum,
            'map_data': map_data,
            'his_row_data': his_row_data,
            'line_data': line_data,
        }
        return Fchart_data

    def get_Schart_data(self):
        WXJSsex = XsWxjsData().get_case_sex_number(self.defendant_info)
        WXJSage = XsWxjsData().get_case_age_number(self.defendant_info)
        WXJSedu = XsWxjsData().get_case_edu_number(self.defendant_info)
        WXJSjob = [['无业游民', '工人', '自营业主', '教师', '医生', '农民'], [420, 330, 340, 390, 520, 750]]
        Schart_data = {
            'WXJSSEX': WXJSsex,  # 当事人性别信息
            'WXJSJOB': WXJSjob,# 职业分布
            'WXJSEDU': WXJSedu,  # 教育程度
            'WXJSAGE': WXJSage,  # 年龄信息
        }
        return Schart_data

    def get_Tchart_data(self):
        WXJSajmoney = XsWxjsData().money_AJ('危险驾驶罪')
        WXJSprison_date_info = XsWxjsData().prison_date('危险驾驶罪')
        WXJSsentence = XsWxjsData().get_case_sentence_date_number(WXJSprison_date_info)
        WXJScasemoney = XsWxjsData().get_case_money(WXJSajmoney)
        WXJSalcohol = XsWxjsData().get_case_alcohol_amount()
        Tchart_data = {
            'WXJSsentence': WXJSsentence,
            'WXJScasemoney': WXJScasemoney,
            'WXJSalcohol': WXJSalcohol,
        }
        return Tchart_data



WXJSdefendant_info = XsWxjsData().get_defendant_info('危险驾驶罪')

F_chart_wxjs_data = ChartRegion(WXJSdefendant_info).get_Fchart_data()

S_chart_wxjs_data = ChartRegion(WXJSdefendant_info).get_Schart_data()

T_chart_wxjs_data = ChartRegion(WXJSdefendant_info).get_Tchart_data()

print('F_chart_wxjs_data: ', F_chart_wxjs_data)
# print('*'*100)
# print(S_chart_wxjs_data)
# print('*'*100)
# print(T_chart_wxjs_data)

