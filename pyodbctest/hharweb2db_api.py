import pyodbc
import datetime


HHARWEB2 = (r'DRIVER={SQL Server};'
            r'SERVER=HHARWEB2\SQLEXPRESS;'
            r'DATABASE=PositiveCensusReport;'
            r'Trusted_Connection=yes;'    )

HHSWLSQLDEV01 = (r'DRIVER={SQL Server};'
                r'SERVER=HHSWLSQLDEV01;'
                r'DATABASE=FredTesting;'
                r'Trusted_Connection=yes;'    )

conn_str = HHSWLSQLDEV01

Inbed = ''
REASON= ''
COMMENTS = ''


def reformat(row, rptdate):
    (Unit, Room, Bed, MRN, PatientID, lastname, firstname
     , AdmitDate, CensusStatus, SweepTime, Obsolete, Gender, LevelOfCare) = row
    newroom = Room + '/' + Bed
    if MRN:
        name = '{} {}'.format(lastname, firstname)
    else:
        MRN = PatientID = name = CensusStatus = LevelOfCare = Gender = ''
        AdmitDate = None #pyodbc converts to NULL during insert
    cleanup = (Unit, newroom, MRN, name, CensusStatus, LevelOfCare
               , Gender, AdmitDate, rptdate, Inbed, REASON, COMMENTS)
    return cleanup

def insert_bed_occupancy( data, rptdate, now):
    data = [reformat(d, rptdate) for d in data[1:]] #drop header row
    for d in data: print('insert', d)
    Connection = pyodbc.connect(conn_str)
    Cursor = Connection.cursor()
    test = Cursor.execute('SELECT 333')  #test connection
    Cursor.execute('SET NOCOUNT ON')
    Connection.commit()
    sql = '''INSERT INTO dbo.PositiveCensusReport 
              (Unit, Room, ResidentNumber, ResidentName, Status, LevelOfCare, Gender
              , OrigAdmitDate, RepDate, Inbed, Reason, Comments)
              VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
    Cursor.executemany(sql, data)
    Connection.commit()
    Cursor.close()
    Connection.close()

        
def unittest():
    Connection = pyodbc.connect(conn_str)
    Cursor = Connection.cursor()
    test = Cursor.execute('SELECT 333')
    results = Cursor.fetchone()
    print ('unittest connection', results)
    Cursor.execute('SELECT TOP 10 * FROM [dbo].[PositiveCensusReport]')
    results = Cursor.fetchall()
    for r in results: print ('unittest', r)

if __name__ == '__main__':
    unittest()
    #DB = HHDB()
    #DB.mark_all_obsolete()
    print ('done')
