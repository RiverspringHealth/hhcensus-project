'''
Created on Nov 27, 2019

@author: fsells
'''
import pyodbc

'''
The following connection string works for SQL Server 2012 installed on fred's laptop
'''


local_database = (r'DRIVER={SQL Server};'
#works                r'SERVER=PS-6KR5WF2;'
                r'SERVER=.;'  #Also works and is not dependent on computer name for a local server version.
                r'DATABASE=HHdev;'
                r'Trusted_Connection=yes;'    )

HHARWEB2 = (r'DRIVER={SQL Server};'
            r'SERVER=HHARWEB2\SQLEXPRESS;'
            r'DATABASE=PositiveCensusReport;'
            r'Trusted_Connection=yes;'    )




def unittest_hharweb2_database(conn_str):
    Connection = pyodbc.connect(conn_str)
    Cursor = Connection.cursor()
    test = Cursor.execute('SELECT 333')
    results = Cursor.fetchone()
    print ('unittest connection', results)
    
    
def unittest_local_database(conn_str):
    Connection = pyodbc.connect(conn_str)
    Cursor = Connection.cursor()
    test = Cursor.execute('SELECT 333')
    results = Cursor.fetchone()
    print ('unittest connection', results)
    Cursor.execute('SELECT TOP 10 * FROM [dbo].[bedcheck]')
    results = Cursor.fetchall()
    print('results=', results)
    for r in results: print ('unittest', r)

if __name__ == '__main__':
    #unittest_local_database(local_database)
    #unittest_hharweb2_database(HHARWEB2)
    print ('done')
