'''
Created on Dec 28, 2019

@author: fsells

This module bypasses Django ORM and uses pyodbc to increase speed where needed.
'''

import sys, datetime, os
import pyodbc
from webapp import utilities
from webapp import sql_queries_MatrixCare as SQL

BIDW_50582_HebrewHome = ( #this works w/o opening any VPN, etc.
    r'Driver={SQL Server};'
    r'Server=mydatahost5.matrixcarecloud.com,41434\CUSPVIMANDBS05;'
    r'Database=BIDW_50582_HebrewHome;'
    r'Trusted_Connection=yes;'
    
    )

LOCAL_LAPTOP = ( 
        r'DRIVER={SQL Server};'
        r'SERVER=.;'
        r'DATABASE=FredTesting;'
        r'Trusted_Connection=yes;'   )

HHSWLDEV02 = (  #this works, even though UID and PWD are defined in ODBC DSN 32 bit
    r'DSN=censusapps32;'
    r'UID=hhcensus;'
    r'PWD=Plan-Tree-Scale-Model-Seed-9;'
    )  

from django.db import connection

class DatabaseQueryManager(object):
    '''
    The methods are used to get applicable data from the local copy
    of the MatrixCare (MyData) DB.  Each method is self explanatory
    except "get_something" which is used byy all other methods to
    convert the list of data records to a list of Python dictionaries.
    '''


    def __init__(self, conn_str = HHSWLDEV02, DEBUG=False):
#        self.CONNECTION_STRING = conn_str
        self.DEBUG = DEBUG
        self._get_connection()
        
    def _get_connection(self):
#        self.Connection = pyodbc.connect(self.CONNECTION_STRING)
        self.Connection = connection
        cursor = self.Connection.cursor()
        cursor.execute("SELECT 1")  #will raise exception if connection fails
        cursor.close()


    def get_something(self, sql, *args, include_column_names=True):
        cursor = self.Connection.cursor()
        cursor.execute(sql, *args)
        records = cursor.fetchall() 
        names = tuple([column[0] for column in cursor.description] )
        #print(names)
        #print (records[0])
        records = [dict(zip(names, row )) for row in records] 
        #for r in records: print(r)
        cursor.close()
        return records
         
    def get_beds(self):
        records = self.get_something(SQL.ALL_BEDS)
        return records

    def get_patients(self):
        records = self.get_something(SQL.ALL_PATIENTS)
        return records

    def get_level_of_care_definitions(self):
        records = self.get_something(SQL.LEVEL_OF_CARE_DEFINITIONS)
        return records

    def get_leave_of_absence_definitions(self):
        records = self.get_something(SQL.CENSUS_LOA)
        return records
    
    
    def get_admit_discharge_locations(self):
        records = self.get_something(SQL.CENSUS_ADMIT_DISCHARGE_LOCATION)
        return records
    
    def get_all_beds_and_current_occupants(self):
        records = self.get_something(SQL.All_BEDS_AND_CURRENT_OCCUPANTS)
        return records

    def get_unit_summary(self):
        cursor = self.Connection.cursor()
        cursor.execute(SQL.UNIT_SUMMARY)
        records = cursor.fetchall() 
        names = tuple([column[0] for column in cursor.description] )
        results = [names] + records
        return results

    def get_sagely2(self):
        cursor = self.Connection.cursor()
        cursor.execute(SQL.SAGELY2)
        records = cursor.fetchall() 
        names = tuple([column[0] for column in cursor.description] )
        results = [names ] + records
        return results

def quickprint(title, records):
    for record in records: print(title, record)
    print()
    
@utilities.record_elapsed_time    
def unittest():
    mydata = DatabaseQueryManager()
    quickprint('level of care',  mydata.get_level_of_care_definitions() )
    quickprint('beds', mydata.get_beds() )
    quickprint('patients', mydata.get_patients() )
    quickprint('LoA',  mydata.get_leave_of_absence_definitions())
    quickprint('Admit-DC Locations', mydata.get_admit_discharge_locations())
    quickprint('Positive Census', mydata.get_all_beds_and_current_occupants())

if __name__ == '__main__':
    print ('starting sql api')
    unittest()
    print ('ending sql api')