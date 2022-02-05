'''
Created on Jan 30, 2021
The purpose of this module is to create several .csv files and send 
those files to a specified distribution list.  The files contain PHI.
    The format was specified by RXNT, however RSL is only using a small
    Amount of the possible fields, blank fields are designated by adjacent
    commas.
    1) Payers (All)
        a: PayerID (i.e. Primary Key)
        b: Paner Name
        c...u: blank
    2) Patients (only those who are "In House" when file is created)
        a: MRN
        b: blank
        c: First Name
        d: blank
        e: Last Name
        f: Gender
        g: DoB: mm/dd/yyyy
        h: 5901 Palisade Avenue
        i: unit-room-bed  i.e. G1-102-B
        j: 10471 i.e. zipcode of facility always
        k: blank
        l: Riverdale
        m: NY
        n: blank
        o: phone
        p...r: blank
    3) Case (correlates patient to first two payers)
        a: blank
        b: MRN
        c: blank
        d: blank
        e: blank
        f...M  Primary Insurance
            f: PayerID
            g: blank
            h: blank
            i: policy # if available
            j...k:blank
            l: start date
            m: end date
        N...U: Secondary Insurance same as Primary fields 
    @author: fsells
'''

import sys, os, datetime, csv, smtplib, os.path
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from django.conf import settings

from webapp.constants import *
from webapp import sql_api
from . import rxnt_sql


class Command(BaseCommand):
    help = 'copies data from nightly bed check into d:/temp/sagely.csv and emails it to Sagely DL'

    def add_arguments(self, parser):
        pass
        

    def send_email(self, sendto=['frederick.sells@riverspring.org'], subject='RXNT Export', text='', html='testing', folder='D:\Temp', attachments=[]):
        outer = MIMEMultipart("alternative")
        outer['Subject'] = subject
        outer['From'] = 'rxnt_test@hebrewhome.org'
        outer['To'] = ', '.join(sendto)
        part1 = MIMEText(text, "plain")
        part2 = MIMEText('<h3>'+html+'</h3>', "html")
        outer.attach(part1)
        outer.attach(part2)
        for path in attachments:
            with open(path, 'rb') as fp:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(fp.read())
                    part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(path))
                    outer.attach(part)
        s = smtplib.SMTP(settings.EMAIL_HOST)
        s.send_message(outer)
        s.quit()

    def write_file(self, db, name, sql):
        print(name)
        path =  os.path.join('D:\\', 'temp', 'rxnt', name+'.csv')
        #records = [[name]]
        #print (sql)
        records = db.get_values(sql)
        with open(path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(records)
        return path

    

    def handle(self, *args, **options):
        db = sql_api.DatabaseQueryManager()

        ############################################print('options', options)
        timestamp = datetime.date.today().strftime('%Y%m%d')
        ####################print (timestamp)  
        exports = dict(patients=rxnt_sql.INHOUSE_PATIENTS, payers = rxnt_sql.PAYERS, case = rxnt_sql.CASES)
        attachments = []
        for name, sql in exports.items():
            path = self.write_file(db, name+timestamp, sql)
            attachments.append(path)
        self.send_email(attachments=attachments)
        return
        records = self.get_data() 
        path = self.write_file(records)
        self.send_email(path)
        
            
            
    
        