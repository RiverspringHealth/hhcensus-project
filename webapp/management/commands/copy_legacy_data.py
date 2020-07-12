'''
Created on Jul 10, 2019

This is a Django command that copies data from HHARWEB2 to the local database
it is used to load historical data from the legacy system to the new system 
to support both testing and historical analysis.  It should only be run once, manually,
when going to production, live.

@author: fsells
'''
import pyodbc
import datetime

from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from django.conf import settings

ONE_HOUR = datetime.timedelta(hours=1)

def get_old_data(Connection, start, end):
    Cursor = Connection.cursor()
    sql = '''
             SELECT pcr.Unit, Room, ResidentNumber, ResidentName, Status, LevelOfCare,Gender
                      ,OrigAdmitDate,  YesNo, Reason, RepDate, Comments
                      , pcr.update_by, update_dt, pcr.create_dt, users.UserName
                FROM [dbo].[PositiveCensusReport] AS pcr
                LEFT JOIN [dbo].[PositiveCensusReportLogins] AS logins 
                    ON pcr.update_by=logins.PositiveCensusReportLoginID
                LEFT JOIN [dbo].[PositiveCensusReportUsers] AS users 
                    ON logins.PositiveCensusReportUserID=users.PositiveCensusReportUserID
                WHERE pcr.RepDate BETWEEN '{}' AND '{}'
                AND pcr.Unit NOT IN ('M1', 'M2', 'MM')
                ORDER BY pcr.RepDate, Unit, Room;
        '''
    sql = sql.format(start, end)
    Cursor.execute(sql)
    rows = Cursor.fetchall()
    Cursor.close()
    Connection.close()
    return rows

def insert_data(Connection, start, end,  data):
    Cursor = Connection.cursor()
    Cursor.execute('SET NOCOUNT ON')
    Connection.commit()
    delete_redundant = '''DELETE dbo.NightlyBedCheck WHERE RepDate BETWEEN  '{}' AND '{}' '''
    sql = delete_redundant.format(start, end)
    Cursor.execute(sql)
    Connection.commit()
    sql = '''INSERT  dbo.NightlyBedCheck
                  (Unit ,Room  ,ResidentNumber ,ResidentName
                  ,Status  ,LevelOfCare  ,Gender  ,CurrentAdmitDate
                  ,Inbed  ,Reason ,RepDate   ,Comments
                  ,UpdateByID  ,UpdateDatetime  ,CreateDatetime  ,UpdateByName
                    ,Obsolete)   
                 VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 1)
                 '''
    Cursor.executemany(sql, data)
    Connection.commit()
    Cursor.close()    

def execute(source, destination, startdate, enddate, save):
    data = get_old_data(source, startdate, enddate)
    print(len(data[0]), data[0])
    if save:
        insert_data(destination, startdate, enddate, data)
        print ('%s records inserted  into target database' % (len(data),))
    else:
        for x in data[:9]: print('census:', x)
        print('DEBUG=True, no data written to DB')



class Command(BaseCommand):
    help = 'USEAGE: python copy_legacy_data start=4/7/2020 --end=4/9/2020 [--save]'
              
    def add_arguments(self, parser):
        parser.add_argument('--start', action= 'store', help = 'first day of copy mm/dd/yyyy',
                            type=lambda s: datetime.datetime.strptime(s, '%m/%d/%Y'),
                            default = datetime.date.today())
        parser.add_argument('--end', action= 'store', help = 'last day of copy mm/dd/yyyy',
                            type=lambda s: datetime.datetime.strptime(s, '%m/%d/%Y'),
                            default = datetime.date.today())

        parser.add_argument('--target', action='store', help='dev (default) for dev server, prod for production server'  ,
                            default = 'dev')
        parser.add_argument('--save', action= 'store_true', help = 'required to write data to target', default=False)
        

    def handle(self, *args, **options):
        startdate = options['start']
        enddate = options['end']
        save = options['save']
        source = pyodbc.connect(settings.HHARWEB2_CONNECTION_STRING)
        target = connection # from settings DATABASES
        execute(source, target, startdate, enddate, save)
        print('copy done')

    

        
            
            
            
        