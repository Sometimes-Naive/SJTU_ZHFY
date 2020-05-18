#coding: utf-8
"""CourtDataVisualization situation assessment module temporary data source

在此文件中定义一些经过一定处理的常量数据，以使由于特殊原因暂时不能实时获取处理的数据能够集中管理。
"""

## data for test

# 2019重庆地区营商司法环境得分-热力图数据
from unittest import *
courts = {'万州区': 40, '丰都县': 40, '九龙坡区': 40, '云阳县': 40, '北碚区': 39, '南岸区': 40, '南川区': 40,
          '合川区': 40, '垫江县': 40, '城口县': 40, '大渡口区': 40, '大足区': 40, '奉节县': 40, '巫山县': 40,
          '巫溪县': 40, '巴南区': 40, '开州区': 39, '彭水苗族土家族': 40, '忠县': 40, '梁平区': 40, '武隆区': 40,
          '永川区': 40, '江北区': 40,  '江津区': 40, '沙坪坝区': 40, '涪陵区': 40, '渝中区': 40, '渝北区': 40,
          '潼南区': 40, '璧山区': 40, '石柱土家族': 40, '秀山': 40, '綦江区': 40, '荣昌区': 40, '酉阳': 40,
          '铜梁区': 40, '长寿区': 40, '黔江区': 40}  # 注意区县名字

def heatmap(item, index):
    return {
        'name': list(item)[0],
        'value': 65 + 0.6 * index
    }
heatmap_data = [heatmap(x, list(courts.items()).index(x)) for x in list(courts.items())]
# print('heatmap_data:', heatmap_data)

# 营商环境司法建设总体态势-折线图数据
china = {
    'name': '中国 (北京+上海)',
    'data': [64.6, 65.2, 74.0, 77.9]
}
chongqing = {
    'name': '重庆',
    'data': [61.3, 63.4, 69.2, 73.7]
}
overall_trend = {
    'xCategory': ['2016', '2017', '2018', '2019'],
    'series': [china, chongqing],
    'legend': '重庆地区'
}
# print('overall_trend: ', overall_trend)

# 2019重庆营商环境司法建设-优秀区县-条状图数据
overall_rank = {}
overall_rank['x'] = ['万州区', '北碚区', '合川区', '巴南区', '武隆区', '涪陵区', '江津区']
overall_rank['data'] = [86.5, 82.2, 80.3, 77.9, 75.4, 72.5, 70.4]
overall_rank['title'] = '2019重庆营商环境司法建设-优秀区县'
# print('overall_rank: ', overall_rank)

# 重庆营商环境司法指标态势-柱状图数据
htzx = {}
pccl = {}
htzx['name'] = '合同执行'
htzx['data'] = [68.8, 69.7, 79.0, 80.9]
pccl['name'] = '破产处理'
pccl['data'] = [52.1, 54.6, 55.9, 62.1]

indicator_trend = {}
indicator_trend['xCategory'] = ['2016', '2017', '2018', '2019']
indicator_trend['series'] = [htzx, pccl]
# print('indicator_trend: ', indicator_trend)

# 破产处理指标得分情况-仪表图数据
pccl_score = {}
pccl_score['x'] = ['回收率', '破产框架指数']
pccl_score['data'] = [39.8, 84.4]
pccl_score['title'] = '指标映射得分情况'
# print('pccl_score: ', pccl_score)

# 合同执行指标得分情况-仪表图数据
htzx_score = {}
htzx_score['x'] = ['时间', '成本', '司法程序质量指数']
htzx_score['data'] = [70.1, 83.1, 91.7]
htzx_score['title'] = '指标映射得分情况'
# print('htzx_score: ', htzx_score)

# 营商指标年度分数对比-蜘蛛图数据
this_year = {}
last_year = {}

this_year['name'] = '2019'
this_year['data'] = [94.1, 62.1, 77.3, 95.4, 81.0, 80.9, 60.0, 72.0, 70.1, 86.5]
this_year['pointPlacement'] = 'on'

last_year['name'] = '2018'
last_year['data'] = [93.4, 55.9, 65.2, 92.0, 80.8, 79.0, 60.0, 62.0, 67.9, 83.4]
last_year['pointPlacement'] = 'on'

spidermap_data = {}
spidermap_data['x'] = ['企业创办', '破产处理', '施工许可', '电力许可', '财产登记', '合同执行', '信贷获取', '中小投资者保护', '税务缴纳', '跨境贸易']
spidermap_data['series'] = [last_year, this_year]
spidermap_data['title'] = '营商指标年度分数展示'
# print('spidermap_data: ', spidermap_data)

# 营商指标年度分数变化情况-条状图数据
diff_data = {}
diff_data['x'] = ['总体', '企业创办', '破产处理', '施工许可', '电力许可', '财产登记', '合同执行', '信贷获取', '中小投资者保护', '税务缴纳', '跨境贸易']
diff_data['data'] = [3.9, 0.7, 6.2, 12.1, 3.4, 0.2, 1.9, 0, 10.0, 2.2, 3.1]
diff_data['title'] = '营商指标年度分数变化情况'
# print('diff_data: ', diff_data)
