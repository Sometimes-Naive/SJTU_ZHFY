#coding: utf-8
"""CourtDataVisualization core command for data process scheduling

这个命令调用全部模块的数据处理，在系统中辅以crontab命令定时执行。
"""




from django.core.management.base import BaseCommand, CommandError
from apps.special_topic.managers import CivilDataProcessManager as CivilManager, CriminalDataProcessManager as CriminalManager

class Command(BaseCommand):
    help = 'Update the data for overview module'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):

        civil_manager = CivilManager()
        criminal_manager = CriminalManager()
        criminal_manager.preprocess().run()
        # manager.preprocess()
        # manager.run()

        self.stdout.write(self.style.SUCCESS('Successfully updated data'))
