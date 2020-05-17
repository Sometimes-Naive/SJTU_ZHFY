#coding: utf-8
"""CourtDataVisualization special topic module Configuration

在此文件中定义模块基本配置，在配置好name项后需要
到configs/settings.py中的 INSTALLED_APPS 添加相应模块。
"""

from django.apps import AppConfig


class SpecialTopicConfig(AppConfig):
    name = 'special_topic'