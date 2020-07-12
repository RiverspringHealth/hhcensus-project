'''
Created on Jul 10, 2019
This program copies beds and occupants from MyData into CensusApps NightlyBedCheck.
It is intended to be run from an external scheduler at 11:45 pm
In case of a malfunction, it can also be rerun during the day.

@author: fsells
'''
import datetime
from django.core.management.base import BaseCommand, CommandError

from webapp  import models
from webapp import sql_api 
from webapp.utilities import DataObject

ONE_HOUR = datetime.timedelta(hours=1)

class Command(BaseCommand):
    help = 'copies census data from local mydata tables  to local NightlyBedCheck in the same database'

    def add_arguments(self, parser):
        parser.add_argument('--start', action= 'store', help = 'first day of sweep mm/dd/yyyy, for testing',
                            type=lambda s: datetime.datetime.strptime(s, '%m/%d/%Y'),
                            default = datetime.date.today())
        parser.add_argument('--days', action= 'store', help = 'number of days for sweep, for testing', default=1, type=int)
                
    def reformat(self, row, reportdate):
        row.AdmitDate = row.AdmitDate.strftime('%m/%d/%Y %H%M %A')
        newrow = (row.UnitName, row.RoomAndBed, row.MedicalRecordNumber, row.Name, row.LastStatus, row.LevelOfCare, row.Sex, row.AdmitDate, reportdate)
        return newrow

    def get_scrubbed_beds_and_occupants(self, mydata,  querydate=None, reportdate=None):
        records = mydata.get_all_beds_and_current_occupants()
        return records

    def save_bedcheck_data(self, records, reportdate):
        records = [DataObject(r) for r in records]
        for r in records:
            bed = models.NightlyBedCheck()
            bed.Unit = r.UnitName
            bed.Room = r.RoomAndBed
            bed.ResidentNumber = r.MedicalRecordNumber
            bed.ResidentName =r.Name
            bed.Status = r.LastStatus
            bed.LevelOfCare = r.LevelOfCare
            bed.Gender = r.Sex
            bed.CurrentAdmitDate = r.AdmitDate
            bed.RepDate = reportdate.date()
            bed.save()
    

    def handle(self, *args, **options):
        firstday =  options['start'] 
        ndays = options['days']
        almost_midnight = ' 11:45:00 PM'
        NOW = datetime.datetime.now()
        REPORT_DATE = NOW + ONE_HOUR       
        NOW= NOW.date()
        print(REPORT_DATE)
        mydata = sql_api.DatabaseQueryManager()
        for n in range(ndays):
            records = self.get_scrubbed_beds_and_occupants(mydata, reportdate=REPORT_DATE.strftime('%m/%d/%Y'))
            self.save_bedcheck_data(records, REPORT_DATE)
        print('sweep done')
        
            
            
            
        