#coding: utf-8
from django.apps import AppConfig, apps
from django.conf import settings

class VisualizationConfig(AppConfig):

    name = 'core'

    def ready(self):

        print(111111111111111)

        # self.path =  settings.BASE_DIR
        print(self.path)

        pass