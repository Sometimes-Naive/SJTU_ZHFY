import xlrd
import difflib


fpath_score = "./data/score_40.xls"
fpath_rank = "./data/rank_40.xls"


heatmap_court_names = {'万州区': 40, '丰都县': 40, '九龙坡区': 40, '云阳县': 40, '北碚区': 39, '南岸区': 40, '南川区': 40,
          '合川区': 40, '垫江县': 40, '城口县': 40, '大渡口区': 40, '大足区': 40, '奉节县': 40, '巫山县': 40,
          '巫溪县': 40, '巴南区': 40, '开州区': 39, '彭水苗族土家族': 40, '忠县': 40, '梁平区': 40, '武隆区': 40,
          '永川区': 40, '江北区': 40,  '江津区': 40, '沙坪坝区': 40, '涪陵区': 40, '渝中区': 40, '渝北区': 40,
          '潼南区': 40, '璧山区': 40, '石柱土家族': 40, '秀山': 40, '綦江区': 40, '荣昌区': 40, '酉阳': 40,
          '铜梁区': 40, '长寿区': 40, '黔江区': 40}


# s = '渝北'
# query_str = '渝中区'
# print(difflib.SequenceMatcher(None, query_str, s).quick_ratio())


def court_name_translator(name):
    if name != '铁路' and name != '彭水':
        for key in heatmap_court_names:
            if difflib.SequenceMatcher(None, key, name).quick_ratio() > 0.5:
                return key
    elif name == '彭水':
        return '彭水苗族土家族'
    else:
        return '铁路'


def read_in(fpath1, fpath2):
    workbook_score = xlrd.open_workbook(fpath_score)
    sheet_score = workbook_score.sheet_by_name(workbook_score.sheet_names()[0])
    sheet_score_rownum = sheet_score.nrows
    sheet_score_colnum = sheet_score.ncols
    print(sheet_score_rownum)
    print(sheet_score_colnum)

    workbook_rank = xlrd.open_workbook(fpath_rank)
    sheet_rank = workbook_rank.sheet_by_name(workbook_rank.sheet_names()[0])
    sheet_rank_rownum = sheet_rank.nrows
    sheet_rank_colnum = sheet_rank.ncols
    print(sheet_rank_rownum)
    print(sheet_rank_colnum)

    dict_score = {}
    for row in range(1, sheet_score_rownum):
        tmp = court_name_translator(sheet_score.row_values(row)[0])
        dict_score[tmp] = []
        for j in range(1, sheet_score_colnum):
            dict_score[tmp].append(round(sheet_score.row_values(row)[j], 3))
    print("dict_score: ", dict_score)

    dict_rank = {}
    col = 0
    i = 0
    while col < sheet_rank_colnum:
        dict_rank[str(i)] = []
        tmp = sheet_rank.col_values(col)[1:8:1]
        dict_rank[str(i)] = tmp
        col += 2
        i += 1
    print("dict_rank: ", dict_rank)

    return dict_score, dict_rank


score_data, rank_data = read_in(fpath_score, fpath_rank)


def data_generator(score_data, rank_data):
    heatmap_data = []
    for i in range(0, 40):
        heatmap_data.append([])
        j = 0
        for key in score_data.keys():
            # print(court_name_translator(key))
            heatmap_data[i].append({})
            heatmap_data[i][j]['name'] = key
            heatmap_data[i][j]['value'] = score_data[key][i]
            j += 1
    print("heatmap_data: ", heatmap_data)

    barmap_data = []
    for i in range(0, 40):
        barmap_data.append({})
        barmap_data[i]['name'] = '总质效排名'
        barmap_data[i]['region'] = rank_data[str(i)]
        barmap_data[i]['score'] = {}
        barmap_data[i]['score']['data'] = []
        for name in rank_data[str(i)]:
            if name != '铁路' and name != '彭水':
                for key in score_data:
                    if difflib.SequenceMatcher(None, key, name).quick_ratio() > 0.5:
                        barmap_data[i]['score']['data'].append(score_data[key][i])
            elif name == '彭水':
                barmap_data[i]['score']['data'].append(score_data['彭水苗族土家族'][i])
            else:
                barmap_data[i]['score']['data'].append(score_data['铁路'][i])
    print("barmap_data: ", barmap_data)

    time_data = []
    for i in range(0, 40):
        if i < 12:
            time_data.append(str(2016) + '年' + str(i+1) + '月')
        else:
            time_data.append(str(2016+int(i/12)) + '年' + str(i%12+1) + '月')
    print(time_data)
    return heatmap_data, barmap_data, time_data

heatmap_data, barmap_data, time_data = data_generator(score_data, rank_data)
