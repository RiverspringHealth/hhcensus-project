'''
Created on Jul 10, 2019

This is a Django command that copies data from MyData to the kronos table.

@author: fsells
'''

from django.core.management.base import BaseCommand, CommandError
from webapp import sql_api

def insert_data(Connection, start, end,  data):
    pass


class Command(BaseCommand):
    help = 'USEAGE: python manage.py kronos [--save]'
              
    def add_arguments(self, parser):
        parser.add_argument('--save', action= 'store_true', help = 'required to write data to target', default=False)
        

    def handle(self, *args, **options):
        save = options['save']
        DB = sql_api.DatabaseQueryManager()
        records = DB.get_unit_summary()
        if save:
            pass
        else:
            [print(x) for x in records]
        print('kronos done')

    

        
            
            
            
        