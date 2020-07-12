'''
Created on Nov 14, 2019

@author: fsells
'''
from docs.base import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'sql_server.pyodbc',
        'HOST': 'localhost', # 'HHARSWLSQLDEV01.HHARSWLSQLDEV01',
        'PORT': '', #'1433',
        'NAME': 'FredTesting',
        'Trusted_Connection': 'yes;',
#        'USER': 'project_user',
#        'PASSWORD': 'project_password',
        'OPTIONS': {
            'driver': 'ODBC Driver 11 for SQL Server',
            'unicode_results': True,
        },
    },
}