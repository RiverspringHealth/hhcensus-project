import pyodbc
import datetime


Inbed = ''
REASON= ''
COMMENTS = ''


def reformat(row, rptdate):
    (Unit, Room, ResidentNumber, ResidentName, Status, LevelOfCare, Gender, AdmitDate) = row
    cleanup = (Unit, Room, ResidentNumber, ResidentName, Status, LevelOfCare, Gender, AdmitDate, Inbed, REASON,  rptdate, COMMENTS)
    return cleanup

def insert_bed_occupancy(conn_str,  beds, rptdate):
    beds = [reformat(bed, rptdate) for bed in beds[1:]] #drop header row
    ##################################for d in data: print('insert', d)
    Connection = pyodbc.connect(conn_str)
    Cursor = Connection.cursor()
    test = Cursor.execute('SELECT 333')  #test connection
    Cursor.execute('SET NOCOUNT ON')
    Connection.commit()
    sql = '''INSERT INTO dbo.PositiveCensusReport 
              (Unit, Room, ResidentNumber, ResidentName, Status, LevelOfCare, Gender
              , OrigAdmitDate, Inbed, Reason, RepDate, Comments)
              VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
    Cursor.executemany(sql, beds)
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
    print ('done')
