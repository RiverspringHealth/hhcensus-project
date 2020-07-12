'''
Created on Sep 17, 2019

@author: fsells
'''
import sys, datetime, os, time
import pyodbc

def record_elapsed_time(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        print ('%r executed in  %2.2f sec' % (method.__name__,  te-ts) )
        return result
    return timed

LOCAL_LINK_VIEWS = (r'DRIVER={SQL Server};'
                r'SERVER=.;'
                r'DATABASE=FredTesting;'
                r'Trusted_Connection=yes;'    )


SQL = '''
SET NOCOUNT ON
  
DECLARE @SweepDate DATETIME = ? --'2019-10-28 23:45:00'
--SELECT @SweepDate
 --SELECT --pse.PatientID, pse.StartDate, pse.CensusType , count(*)
 --bed.UnitName, bed.RoomAndBed, pat.LastName, pat.FirstName, loc.LocID, loc.Description [LoCDescription], pse.*
 
 DECLARE @ResidentsTbl TABLE (
	[BedID] INT NULL,
	[ResidentNumber] [nvarchar](50) NULL,
	[ResidentName] [nvarchar](50) NULL,
	[Status] [nvarchar](50) NULL,
	[LevelOfCare] [nvarchar](50) NULL,
	[Gender] [nvarchar](50) NULL,
	[OrigAdmitDate] [datetime] NULL
) 

 INSERT INTO @ResidentsTbl
 SELECT UnitName, CONCAT(bed.RoomName, '/', bed.BedName) AS Room,
 pat.MedicalRecordNumber,  pat.LastName+' '+ pat.FirstName [Name], pse.LastStatus, loc.Description [LevelOfCare], pat.sex , pse.AdmitDate
 FROM mydata.FacilityUnitRoomBed AS bed
 LEFT JOIN mydata.PatientStayElementLatest AS pse
 LEFT JOIN mydata.Patient AS pat ON pat.PatientID=pse.PatientID
LEFT JOIN mydata.Census_LevelOfCare AS loc on loc.LOCID = pse.LOCID and pse.FacilityID=loc.FacilityID 
WHERE pse.CensusType IN (1,2,5,6)
AND  @SweepDate BETWEEN StartDate AND EndDate
AND pat.CensusStatus = 'In House'  -- ignore discharged
Order By  UnitName, Room

SELECT UnitName, CONCAT(bed.RoomName, '/', bed.BedName) AS RoomAndBed, ResidentNumber, ResidentName, Status, LevelOfCare, Gender, OrigAdmitDate
From mydata.FacilityUnitRoomBed AS bed
LEFT JOIN @ResidentsTbl AS res on res.BedID=bed.BedID
Order By  UnitName, RoomName, BedName
'''

def find_more_than_one_person_in_a_bed(records):
    duplicates = []
    grouper = dict()
    for r in records:
        key = '%s-%s' % (r[0],r[1])
        grouper.setdefault(key, []).append(r)
    for key, value in grouper.items():
        print (key, value)
#         if len(value)>1:
#             for v in value:
#                 print ('duplicate', v)

class MyDataQueryManager(object):
    '''
    This class gets all beds in the facility and their occupant if any.
    It returns column names in the first row in case subsequent code
    needs that information.
    '''


    def __init__(self, conn_str = LOCAL_LINK_VIEWS, DEBUG=False):
        self.DEBUG = DEBUG
        self.Connection = pyodbc.connect(conn_str)
        cursor = self.Connection.cursor()
        cursor.execute("SELECT 1")  #will raise exception if connection fails

    def get_something(self, sql, *args):
        cursor = self.Connection.cursor()
        cursor.execute(sql, *args)
        names = [column[0] for column in cursor.description]
        records = cursor.fetchall()  
        return [names] + records
         
    def get_beds_x_patients(self, sweeptime):
        sql = SQL
        records = self.get_something(sql, sweeptime)
        return records

@record_elapsed_time        
def unittest():
    mydata = MyDataQueryManager()
    sweeptime = datetime.datetime.now()
    records = mydata.get_beds_x_patients(sweeptime)
    return records

        
if __name__ == '__main__':
    records = unittest()
    for p in records: print('bed_patient', p)
    print ('mydata_api unittest done', len(records)-1)  #deduct for header row dummy
    if len(records)>756: find_more_than_one_person_in_a_bed(records)    