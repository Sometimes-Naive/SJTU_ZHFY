#coding: utf-8
"""CourtDataVisualization overview module Model Definition

在此文件中定义模块中用到数据库、文件等数据来源所对应的数据格式。
连接Mongo数据库时变量名需要和数据库中对应表（table）中的Json键名一致。
连接Mongo数据库时，API使用可参考： http://docs.mongoengine.org/index.html

"""
# from core.models import *
from djongo import models

class CivilCaseDoc(models.Model):
    标题 = models.TextField()
    案号 = models.TextField()
    案件类型 = models.TextField()
    庭审程序 = models.TextField()
    案由 = models.TextField()
    文书类型 = models.TextField()
    法院 = models.TextField()
    判决日期 = models.TextField()
    原告 = models.TextField()
    被告 = models.TextField()
    第三人 = models.TextField()
    法官 = models.TextField()
    审判长 = models.TextField()
    审判员 = models.TextField()
    书记员 = models.TextField()
    头部 = models.TextField()
    头部2 = models.TextField()
    当事人 = models.TextField()
    当事人2 = models.TextField()
    庭审程序说明 = models.TextField()
    庭审程序说明2 = models.TextField()
    庭审过程 = models.TextField()
    庭审过程2 = models.TextField()
    庭审过程3 = models.TextField()
    庭审过程4 = models.TextField()
    庭审过程5 = models.TextField()
    庭审过程6 = models.TextField()
    法院意见 = models.TextField()
    法院意见2 = models.TextField()
    判决结果 = models.TextField()
    判决结果2 = models.TextField()
    庭后告知 = models.TextField()
    庭后告知2 = models.TextField()
    结尾 = models.TextField()
    结尾2 = models.TextField()
    附录 = models.TextField()
    附录2 = models.TextField()
    class Meta:
        # managed = False
        db_table = 'MS_law_data'


class CriminalCaseDoc(models.Model):
    标题 = models.TextField()
    案号 = models.TextField()
    案件类型 = models.TextField()
    庭审程序 = models.TextField()
    案由 = models.TextField()
    文书类型 = models.TextField()
    法院 = models.TextField()
    判决日期 = models.TextField()
    原告 = models.TextField()
    被告 = models.TextField()
    第三人 = models.TextField()
    法官 = models.TextField()
    审判长 = models.TextField()
    审判员 = models.TextField()
    书记员 = models.TextField()
    头部 = models.TextField()
    头部2 = models.TextField()
    当事人 = models.TextField()
    当事人2 = models.TextField()
    庭审程序说明 = models.TextField()
    庭审程序说明2 = models.TextField()
    庭审过程 = models.TextField()
    庭审过程2 = models.TextField()
    庭审过程3 = models.TextField()
    庭审过程4 = models.TextField()
    庭审过程5 = models.TextField()
    庭审过程6 = models.TextField()
    法院意见 = models.TextField()
    法院意见2 = models.TextField()
    判决结果 = models.TextField()
    判决结果2 = models.TextField()
    庭后告知 = models.TextField()
    庭后告知2 = models.TextField()
    结尾 = models.TextField()
    结尾2 = models.TextField()
    附录 = models.TextField()
    附录2 = models.TextField()
    class Meta:
        # managed = False
        db_table = 'XS_law_data'


class AdministrativeCaseDoc(models.Model):
    标题 = models.TextField()
    案号 = models.TextField()
    案件类型 = models.TextField()
    庭审程序 = models.TextField()
    案由 = models.TextField()
    文书类型 = models.TextField()
    法院 = models.TextField()
    判决日期 = models.TextField()
    原告 = models.TextField()
    被告 = models.TextField()
    第三人 = models.TextField()
    法官 = models.TextField()
    审判长 = models.TextField()
    审判员 = models.TextField()
    书记员 = models.TextField()
    头部 = models.TextField()
    头部2 = models.TextField()
    当事人 = models.TextField()
    当事人2 = models.TextField()
    庭审程序说明 = models.TextField()
    庭审程序说明2 = models.TextField()
    庭审过程 = models.TextField()
    庭审过程2 = models.TextField()
    庭审过程3 = models.TextField()
    庭审过程4 = models.TextField()
    庭审过程5 = models.TextField()
    庭审过程6 = models.TextField()
    法院意见 = models.TextField()
    法院意见2 = models.TextField()
    判决结果 = models.TextField()
    判决结果2 = models.TextField()
    庭后告知 = models.TextField()
    庭后告知2 = models.TextField()
    结尾 = models.TextField()
    结尾2 = models.TextField()
    附录 = models.TextField()
    附录2 = models.TextField()
    class Meta:
        # managed = False
        db_table = 'XZ_law_data'



