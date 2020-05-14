import pandas as pd
import numpy as np
import xlrd
import statsmodels.api as sm


class ChartData:
    
    sa_number = []
    ja_number = []
    region = []
    judge_number = []
    feature = []


    #处理表格文件数据得到收结案和地区信息，收结案可以看做矩阵
    def __init__(self): 
        
        for i in range(1, 10):
            url = '/Users/Tracy/SJTU_ZHFY/data/sjayc/df0' + str(i) + '.xlsx'
            excel = xlrd.open_workbook(url)
            sheet = excel.sheet_by_name('Sheet1')
            sa_data = sheet.col_values(3, 1)
            ja_data = sheet.col_values(2, 1)
            self.sa_number.append(sa_data)
            self.ja_number.append(ja_data) 
            
        for i in range(10, 41):
            url = '/Users/Tracy/SJTU_ZHFY/data/sjayc/df' + str(i) + '.xlsx'
            excel = xlrd.open_workbook(url)
            sheet = excel.sheet_by_name('Sheet1')
            sa_data = sheet.col_values(3, 1)
            ja_data = sheet.col_values(2, 1)
            self.sa_number.append(sa_data)
            self.ja_number.append(ja_data)
        self.region = sheet.col_values(1, 1)
        self.region = [x + '区' for x in self.region]
        self.judge_number = sheet.col_values(4, 1)
        for i in range(6, 9):
            f_data = sheet.col_values(i, 1)
            self.feature.append(f_data)

    
    #得到地图数据,show sa_number and ja_number of every region at last month
    def get_map_data(self):
        
        map_data = []
        for i in range(len(self.region)):
            map_meta_data = {}
            map_meta_data['name'] = self.region[i]
            map_meta_data['value'] = []
            map_meta_data['value'].append(self.sa_number[39][i])
            map_meta_data['value'].append(self.ja_number[39][i])
            map_data.append(map_meta_data)

        return map_data
 
    
    #get sa_number and ja_number of every region at last month
    def get_his_case_data(self):       

        his_data = []
        for i in range(len(self.region)):
            his_meta_data = {}
            his_meta_data['name'] = self.region[i]
            his_meta_data['value'] = []
            his_meta_data['value'].append(self.sa_number[39][i])
            his_meta_data['value'].append(self.ja_number[39][i])
            his_data.append(his_meta_data)

        return his_data


    #get three judicial features of every region at last month
    def get_his_feature_data(self):
        
        feature_name = ['撤诉结案数', '调节结案数', '法定期限内结案数']
        his_data = []
        for i in range(len(self.region)):
            his_meta_data = {}
            his_meta_data['name'] = self.region[i]
            his_meta_data['value'] = []
            for j in range(3):
                his_meta_data['value'].append(self.feature[j][i])
            his_data.append(his_meta_data)
        
        return his_data 

    
    #40 months sa_number and ja_number grouped by 28 regions, draw the line chart 
    def get_line_data(self):
                
        chart_date = [
            '2016-01', '2016-02', '2016-03', '2016-04',
            '2016-05', '2016-06', '2016-07', '2016-08',
            '2016-09', '2016-10', '2016-11', '2016-12',
            '2017-01', '2017-02', '2017-03', '2017-04',
            '2017-05', '2017-06', '2017-07', '2017-08',
            '2017-09', '2017-10', '2017-11', '2017-12',
            '2018-01', '2018-02', '2018-03', '2018-04',
            '2018-05', '2018-06', '2018-07', '2018-08',
            '2018-09', '2018-10', '2018-11', '2018-12',
            '2019-01', '2019-02', '2019-03', '2019-04'
        ]
        line_data = []
        
        for i in range(len(self.region)):
            line_meta_data = {}
            line_sa_number = []
            line_ja_number = []
            for j in range(len(self.sa_number)):
                line_sa_number.append(self.sa_number[j][i])
                line_ja_number.append(self.ja_number[j][i])
            line_meta_data['region'] = self.region[i]
            line_meta_data['chart_date'] = chart_date
            line_meta_data['chart_sa_number'] = line_sa_number
            line_meta_data['chart_ja_number'] = line_ja_number
            line_data.append(line_meta_data)
            
        return line_data
    
    
    #judge_number and its percentage of every region at last month
    def get_pie_data(self):
        
        pie_data = []
        judge_sum = 0
        
        for i in range(28):
            judge_sum += self.judge_number[i]
            
        for i in range(len(self.region)):
            pie_meta_data = {}
            pie_meta_data['name'] = self.region[i]
            pie_meta_data['value'] = []
            pie_meta_data['value'].append(self.judge_number[i])
            pie_meta_data['value'].append(self.judge_number[i]/judge_sum)            
            pie_data.append(pie_meta_data)
        
        return pie_data
        

    #predict sa_number of next month and give corresponding advice
    def prediction(self):

        chart_date = [
            '2016-01', '2016-02', '2016-03', '2016-04',
            '2016-05', '2016-06', '2016-07', '2016-08',
            '2016-09', '2016-10', '2016-11', '2016-12',
            '2017-01', '2017-02', '2017-03', '2017-04',
            '2017-05', '2017-06', '2017-07', '2017-08',
            '2017-09', '2017-10', '2017-11', '2017-12',
            '2018-01', '2018-02', '2018-03', '2018-04',
            '2018-05', '2018-06', '2018-07', '2018-08',
            '2018-09', '2018-10', '2018-11', '2018-12',
            '2019-01', '2019-02', '2019-03', '2019-04', '2019-05'
        ]
        line_data = []
        #sa_predictions = []
        advice_set = ['预测未来收案数量较上个月会出现一个较大增幅，会出现法院在人力资源配置方面案件剧增与人员缓增的矛盾，需要对内部资源进行科学合理分配', 
                      '预测未来收案数量较上个月增幅较小，可视当地司法资源和公共管理水平进行灵活调整', 
                      '预测未来收案数量不会超过上个月的案件处理水平，司法资源配置充足']
        advice = []
        
        for i in range(len(self.region)):
            line_meta_data = {}
            line_sa_number = []
            for j in range(len(self.sa_number)):
                line_sa_number.append(self.sa_number[j][i])
            line_meta_data['region'] = self.region[i]
            line_meta_data['chart_date'] = chart_date
            line_meta_data['chart_sa_number'] = line_sa_number
            line_data.append(line_meta_data) 
        
        for i in range(len(self.region)):
            model = sm.tsa.AR(line_data[i]['chart_sa_number'])
            model_fit = model.fit()
            predictions = model_fit.predict(start=len(line_data[i]['chart_sa_number']), end=len(line_data[i]['chart_sa_number']), dynamic=False)
            #sa_predictions.append(predictions)
            line_data[i]['chart_sa_number'].append(predictions[0])
            if predictions[0] > (line_data[i]['chart_sa_number'][39] + 1000) :
                advice.append(advice_set[0])
            else:
                if predictions[0] > line_data[i]['chart_sa_number'][39] :
                    advice.append(advice_set[1])
                else:
                    advice.append(advice_set[2])
        
        return line_data, advice


#test all the modules
real_chart = ChartData()
map_data = real_chart.get_map_data()
line_data = real_chart.get_line_data()
his_data1 = real_chart.get_his_case_data()
his_data2 = real_chart.get_his_feature_data()
pie_data = real_chart.get_pie_data()
sa_predictions, advice = real_chart.prediction()

print(his_data1['value'])
