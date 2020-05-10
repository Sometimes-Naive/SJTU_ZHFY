#coding: utf-8
"""CourtDataVisualization Data Drivers 

在此文件中包含了全局项目中使用的数据输入处理接口。

"""
from django.conf import settings
import wrapt

# mongoengine 废弃不再使用
class connect_mongo(object):

    def __init__(self, database, **kwargs):
        self.database = database
        if 'keep_alive' in kwargs:
            self.keep_alive = kwargs['keep_alive']
        else:
            self.keep_alive = False

    @wrapt.decorator
    def __call__(self, wrapped, instance, args, kwargs):
        from mongoengine.connection import connect, disconnect
        if settings.MONGODB['mode'] == 'single':
            conn = connect(db = self.database, host = settings.MONGODB['host'], port = settings.MONGODB['port'])
            result = wrapped(*args, **kwargs)
            if not self.keep_alive:
                disconnect()
            return result

# class BaseMongoDBDriver():
# 	@staticmethod
# 	def connect(database):
# 		host = 'fetch_host_config'
# 		port = 'fetch_port_config'
# 		connect(database, host='127.0.0.1', port=27017)


class ExcelDataDriver():
	pass


class TxtDataDriver():
	# json & raw
	pass


