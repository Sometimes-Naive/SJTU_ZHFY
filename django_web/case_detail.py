#coding:utf-8
from django_web.models import AllData


def info2str(info):
    str1 = ''
    for j in info:
        if str1 == '':
            str1 = j
        else:
            str1 = str1 + '\n' + j
    return str1

def get_case_title(case_cate = ''):
    #输入为案件类别信息，案件难度筛选（之后加）
    if case_cate == '':
        case_info = AllData.objects(省份='重庆').limit(10)
    else:
        case_info = AllData.objects(省份='重庆', 案件类别=case_cate).limit(10)

    CASE = {
        'case_id': [],
        'case_title': [],
    }
    for i in case_info:
        CASE['case_id'].append(str(i.id))
        CASE['case_title'].append(i.头部信息[0].split('-')[0])
    return CASE

def detail_get(id):
    case_info = AllData.objects(id=id)

    CASE = {
        'case_id':[],
        'case_title':[],
        'case_person':[],
        'case_head':[],
        'case_trial':[],
        'case_judge':[],

    }
    for i in case_info:
        CASE['case_id'] = (str(i.id))
        CASE['case_title'] = (i.头部信息[0].split('-')[0])
        # print(i.头部信息[0])
        CASE['case_head'] = info2str(i.头部信息[1:])
        CASE['case_person'] = info2str(i.人员信息)
        CASE['case_trial'] = info2str(i.案件过程)
        CASE['case_judge'] = info2str(i.判决信息)
    return CASE


if __name__ == '__main__':
    a = get_case_title('刑事案件')
    print(a)




