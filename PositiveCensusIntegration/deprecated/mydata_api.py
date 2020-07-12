'''
Created on Sep 17, 2019

@author: fsells
'''
import sys, datetime, os
import pyodbc

RiverSpringProduction = ( #this works w/o opening any VPN, etc.
    r'Driver={SQL Server};'
    r'Server=mydatahost5.matrixcarecloud.com,41434\CUSPVIMANDBS05;'
    r'Database=BIDW_50582_HebrewHome;'
    r'Trusted_Connection=yes;'
    
    )
SQL = '''
SET NOCOUNT ON
  
DECLARE @SWEEPDATETIME DATETIME = GETDATE()
 --SELECT  @SWEEPDATETIME
 
--set @SWEEPDATETIME = CONVERT(DATETIME, '{}', 101)

DECLARE @BedsTbl TABLE (
      BedId INTEGER
    , RoomId Integer
    , PatientGroupId INTEGER
    , BuildingId INTEGER
    , FacilityId INTEGER
    , BedName VARCHAR(5)  -- from FacilityBed
    , RoomName VARCHAR(6) -- from FacilityRoom
    , UnitName VARCHAR(10) --Abbreviation from PatientGroup
    , FacilityName VARCHAR(50)
)

INSERT INTO @BedsTbl
SELECT 
      facbed.BedID
    , facbed.RoomID
    , facroom.PatientGroupID
    , patgrp.BuildingID
    , patgrp.FacilityID
    , facbed.BedName
    , facroom.RoomName
    , patgrp.Abbreviation
    , fac.Name
FROM STVSNF.FacilityBed AS facbed
JOIN STVSNF.FacilityRoom AS facroom ON facroom.RoomID=facbed.RoomID
JOIN STVSNF.PatientGroup AS patgrp ON patgrp.PatientGroupID=facroom.PatientGroupID
Join STVSNF.Facility AS fac ON fac.FacilityID=patgrp.FacilityID
WHERE facbed.DeletedFlag=0
AND facroom.DeletedFlag=0
AND patgrp.DeletedFlag=0
AND fac.IsActive =1
ORDER BY patgrp.Abbreviation, facroom.RoomName, facbed.BedName


DECLARE @LastPatientEventTbl TABLE(
      PatientID INTEGER
    , lastname VARCHAR(50)
    , firstname VARCHAR(50)
    , gender CHAR(1)
    , RoomNumber VARCHAR(151)
    , MRN VARCHAR(9)
    , CurrentAdmitDt DATETIME
    , CurrentReturnDt DATETIME
    , CensusStatus VARCHAR(30)
    , LastCensusType INTEGER
    , LastCensusDateTime DATETIME
    , LastCensusBedID INTEGER
    , FacilityID INTEGER
    , BuildingID INTEGER
    , LOC INTEGER --fk to STVSNF.Census_LevelOfCare AS loctype on pc.LOC = loctype.LOCID
    , LOCDescription VARCHAR(50)
    )
    
INSERT INTO @LastPatientEventTbl 
SELECT p.PatientID, p.LastName, p.FirstName, p.sex, p.RoomNumber, p.MedicalRecordNumber
     , p.CurrentAdmtDt, p.CurrentReturnDt, p.CensusStatus
      , c.CensusType,  last.LastDateTime, c.BedID, c.FacilityID, c.BuildingID
      , NULL, NULL
FROM STVSNF.Patient p
LEFT JOIN (
      SELECT PatientID, MAX(DateTime) [LastDateTime]
      FROM STVSNF.PatientCensus
      WHERE  CensusType NOT IN (8,9) 
      AND Deleted=0
      GROUP BY PatientID
    ) AS last ON p.PatientID=last.PatientID
JOIN STVSNF.PatientCensus AS c ON (last.PatientID=c.PatientID AND last.LastDateTime = c.DateTime AND c.Deleted=0)
WHERE p.IsActive = 1


UPDATE pc
    SET pc.LOC = x.LOC, pc.LOCDescription = loctype.Description
FROM @LastPatientEventTbl AS pc
JOIN (
    Select FacilityID, PatientID, MAX(DateTime) [DateTime]
    FROM STVSNF.PatientCensus
    WHERE LOC IS NOT NULL AND LOC <> 0
    AND DeletedFlag=0
    GROUP BY FacilityID, PatientID
    ) AS lastloc ON lastloc.PatientID=pc.PatientID and lastloc.DateTime >= pc.CurrentAdmitDt
JOIN STVSNF.PatientCensus AS x ON x.PatientID=lastloc.PatientID AND x.DateTime=lastloc.DateTime AND x.DeletedFlag=0    
LEFT JOIN STVSNF.Census_LevelOfCare AS loctype on x.LOC = loctype.LOCID and pc.FacilityID=lastloc.FacilityID AND loctype.DeletedFlag=0


SELECT UnitName, beds.RoomName, beds.BedName, MRN, PatientID,  lastname, firstname
    , CurrentAdmitDt, CensusStatus, @SWEEPDATETIME, 0, gender, LOCDescription
FROM @BedsTbl AS beds
LEFT JOIN @LastPatientEventTbl AS pat ON beds.BedId=pat.LastCensusBedID
ORDER BY UnitName, RoomName, BedName
'''


class MyDataQueryManager(object):
    '''
    classdocs
    '''


    def __init__(self, conn_str = RiverSpringProduction, DEBUG=False):
        self.DEBUG = DEBUG
        self.Connection = pyodbc.connect(conn_str)
        cursor = self.Connection.cursor()
        cursor.execute("SELECT 1")  #will raise exception if connection fails

    def get_something(self, sql):
        cursor = self.Connection.cursor()
        cursor.execute(sql)
        names = [column[0] for column in cursor.description]
        records = cursor.fetchall()  
        return [names] + records
         
    def get_beds_x_patients(self):
        sql = SQL
        records = self.get_something(sql)
        return records
    
#     def get_patients(self):
#         patients = self.get_something(SQL.get_patients)
#         return patients
        
def unittest():
    mydata = MyDataQueryManager()
    sweeptime = datetime.datetime.now()
    records = mydata.get_beds_x_patients()
    for p in records: print('bex_patient', p) 
    print ('mydata_api unittest done')
        
if __name__ == '__main__':
    unittest()