'''
Created on June 30 2021

This is a Django command that stores the total census by shift and unit

@author: fsells
'''
import datetime, sys
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from webapp import sql_api

SELECT = '''
--DECLARE  @testdate SMALLDATETIME = '2021-7-1 22:00:00';  --NOT in Python

WITH cteOccupants (CurrentUnit, AdmitDate, AdmitUnit, PatientID, InfoDate, InfoUnit)
AS (
SELECT 
	 CASE WHEN info.UnitName IS NULL THEN admit.UnitName ELSE info.UnitName END [CurrentUnit]
	--,count(*) [total]
	,admit.DateTime [AdmitDateTime]
	, admit.UnitName [AdmitUnitName]
	--, admit.CensusType [AdmitCensusType]
	, admit.PatientID [ID]
	,info.DateTime [InfoDateTime]
	, info.UnitName [InfoUnitName]
	--, info.CensusType [InfoCensusType]
FROM (
	SELECT * FROM(
		SELECT unit.UnitName, c.*,  ROW_NUMBER()
		OVER (Partition BY PatientID ORDER BY DateTime DESC) row
		FROM 	[CensusApps].[mydata].[PatientCensus] c
		LEFT JOIN mydata.FacilityUnitRoomBed AS unit on unit.BedID = c.BedID
		--WHERE DateTime <= @testdate AND c.CensusType IN (1,3,4,5,6)
		WHERE DateTime <= '%(testdate)s'  AND c.CensusType IN (1,3,4,5,6) --for python call
		) AS ax
	WHERE ax.CensusType IN (1,5,6) AND row=1
	) AS admit
LEFT JOIN( SELECT * 
		FROM (
			SELECT unit.UnitName, c.*,  ROW_NUMBER()
			OVER (Partition BY PatientID ORDER BY DateTime DESC) row
			FROM 	[CensusApps].[mydata].[PatientCensus] AS c
			LEFT JOIN mydata.FacilityUnitRoomBed AS unit on unit.BedID = c.BedID
			--WHERE DateTime <=  @testdate AND CensusType =2
			WHERE DateTime <=  '%(testdate)s' AND CensusType =2 --python call format
			) AS ix 
		WHERE ix.CensusType=2 AND ix.row=1 
		)AS info ON info.PatientID = admit.PatientID AND info.DateTime>Admit.DateTime
) 
SELECT CurrentUnit, count(*) [total] 
FROM cteOccupants
group by CurrentUnit

/*
UNION ALL  -- -----used to append a total -----not part of production run 
SELECT 'SUM' Name, COUNT(1)
FROM cteOccupants
*/
'''


SHIFTS = [   (6,'Day'), (14,'Eve'),  (22,'Night') ]
ONEDAY = datetime.timedelta(days=1)  
ONEHOUR = datetime.timedelta(hours=1)

def get_shift(runhour):
    for (hour, name) in SHIFTS:
        if abs(float(runhour)-float(hour)) < 2.0: return name
    return 'TEST'
                
class Command(BaseCommand):
    help = 'copies data from nightly bed check into d:/temp/sagely.csv and emails it to Sagely DL'

    def add_arguments(self, parser):
        parser.add_argument('--start', action= 'store', help = 'first day of sweep mm/dd/yyyy, for testing',
                            type=lambda s: datetime.datetime.strptime(s, '%m/%d/%Y'),
                            default = datetime.date.today())

    def add_arguments(self, parser):          
        parser.add_argument('--start', action= 'store', help = 'start date mm/dd/yyyy',type=lambda s: datetime.datetime.strptime(s, '%m/%d/%Y'), default=None)
        parser.add_argument('--stop', action= 'store', help = 'last day', type=lambda s: datetime.datetime.strptime(s, '%m/%d/%Y'))
        parser.add_argument('--debug', action= 'store_true', help = 'true to ', default=False)
                        

    def get_one_shift(self, querytime):
        sql = SELECT % dict(testdate=querytime)
        totals = self.DBAPI.query(sql, show_names=False)
        return dict(totals)
        
    def save_totals(self, adate, shift, locations, totals):
        values = [(adate, location, shift, totals.get(location, 0)) for location in locations]
        sql = '''INSERT INTO dbo.UnitTotalsByShift ( [Census_Date], [Location], [Shift], [Patient_Count]) VALUES (%s, %s, %s, %s) '''
        if self.DEBUG:
            print('debug date={},  shift={}'.format(adate,shift))
            for (unit, total) in totals.items(): print('    ', unit,total)
        else:
            pass
            self.DBAPI.executemany(sql, values)

    def update_everything(self, startdate, stopdate):
        while startdate <= stopdate:
            for (hour, shiftname) in SHIFTS:
                querytime = startdate.replace(hour=hour)
                totals = self.get_one_shift( querytime)
                self.save_totals(querytime, shiftname, self.Locations,  totals)
            startdate = startdate + ONEDAY

    def update_current_snapshot(self):
        querytime = datetime.datetime.now()
        shiftname = get_shift(querytime.hour)
        totals = self.get_one_shift( querytime)
        self.save_totals(querytime, shiftname, self.Locations,  dict(totals))
        
    def handle(self, *args, **options):
        self.DBAPI =  sql_api.DatabaseQueryManager(DEBUG=False)
        print(options)
        start = options.get('start', None)
        stop  = options.get('stop', None)
        self.DEBUG = options.get('debug')   
        self.Locations = [x[0] for x in self.DBAPI.query('SELECT Description FROM mydata.PatientGroup',  show_names=False)]
        self.Locations.sort()
        
        if start:
            print('everything', start, stop)
            self.update_everything(start, stop)  
        else:
            print(start, stop, 'oneshot')
            self.update_current_snapshot()
        print('done')
       
