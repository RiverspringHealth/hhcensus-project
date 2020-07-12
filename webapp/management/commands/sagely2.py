'''
Created on Feb 27, 2020
The purpose of this module is to send emails to a specified distribution list
for all residents where the inbed status is blank or is no and the reason is blank.

@author: fsells
'''

import sys, os, datetime, csv, smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from django.conf import settings

from webapp.constants import *
from webapp import sql_api


class Command(BaseCommand):
    help = 'copies data from nightly bed check into d:/temp/sagely.csv and emails it to Sagely DL'

    def add_arguments(self, parser):
        parser.add_argument('--start', action= 'store', help = 'first day of sweep mm/dd/yyyy, for testing',
                            type=lambda s: datetime.datetime.strptime(s, '%m/%d/%Y'),
                            default = datetime.date.today())
        
    def get_data(self):
        db = sql_api.DatabaseQueryManager()
        records = db.get_sagely2()
        return records

    def write_file(self, records):
        path = os.path.abspath('D:/Temp/sagely.csv')
        with open(path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(records)
        return path

    def send_email(self, path):
        outer = MIMEMultipart()
        outer['Subject'] = '{} Sagely2n'.format(settings.EMAIL_SUBJECT_PREFIX)
        outer['From'] = 'no-reply@hebrewhome.org'
        outer['To'] = ', '.join(settings.SAGELY2_DISTRIBUTION_LIST)
        with open(path, 'rb') as fp:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(fp.read())
        part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(path))
        outer.attach(part)
        s = smtplib.SMTP(settings.EMAIL_HOST)
        s.send_message(outer)
        s.quit()


    def handle(self, *args, **options):
        # print('options', options)
        records = self.get_data() 
        path = self.write_file(records)
        self.send_email(path)
        
            
            
    
        