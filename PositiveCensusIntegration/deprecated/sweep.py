'''
Created on Jul 10, 2019

THIS MODULE IS OBSOLETE; IT WAS DESIGNED TO RUN WITHIN THE DJANGO ENVIRONMENT
WHICH IS NOT USED FOR THIS TASK

@author: fsells
'''
import datetime
import random
from django.core.management.base import BaseCommand, CommandError



from . import mydata_api 
from . import hharweb2db_api

class Command(BaseCommand):
    help = 'copies data from MatrixCare to local DB'

    def add_arguments(self, parser):
        parser.add_argument('--start', action= 'store', help = 'first day of sweep mm/dd/yyyy, for testing',
                            type=lambda s: datetime.datetime.strptime(s, '%m/%d/%Y'),
                            default = datetime.date.today())
        parser.add_argument('--days', action= 'store', help = 'number of days for sweep, for testing', default=1, type=int)
        parser.add_argument('--fakeinput', action= 'store_true', help = 'create fake user entry for testing', default=False)
        
    def handle(self, *args, **options):
        mydata = mydata_api.MyDataQueryManager()
        firstday =  options['start'] 
        ndays = options['days']
        almost_midnight = ' 11:45:00 PM'
        for n in range(ndays):
            sweeptime = firstday + datetime.timedelta(days=n)
            tomorrow = sweeptime + datetime.timedelta(days=1)
            rptdate = tomorrow.strftime('%Y-%m-%d')
            texttime = sweeptime.strftime('%m/%d/%Y') + almost_midnight
            beds = mydata.get_beds_x_patients( texttime)
            #for b in beds: print (b)
            hharweb2db_api.insert_bed_occupancy(beds, rptdate)
            ################if fake_input:                self.fake_user_input(hhdb, nos=3, blanks=2)
            print ('sweeptime={} nrecords={}'.format( texttime, len(beds)))

        print('sweep done')

            
            
            
        