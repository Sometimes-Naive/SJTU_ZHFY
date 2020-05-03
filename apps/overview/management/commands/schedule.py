#coding: utf-8
from django.core.management.base import BaseCommand, CommandError
from apps.overview.managers import DataProcessManager as Manager

class Command(BaseCommand):
    help = 'Update the data for overview module'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):

        manager = Manager()

        manager.preprocess().run()
        # manager.run()

        self.stdout.write(self.style.SUCCESS('Successfully updated data'))