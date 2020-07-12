'''
Created on Nov 14, 2019

@author: fsells
'''
from docs.base import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'sql_server.pyodbc',
        'NAME': 'HHBedCheck',
        'HOST': r'.\SQLEXPRESS',
       # 'PORT':'1433',
        'USER': 'django',
        'PASSWORD': 'django',
        'OPTIONS': {
                 'driver': 'SQL Server Native Client 10.0',                
                 }
        },  
    }