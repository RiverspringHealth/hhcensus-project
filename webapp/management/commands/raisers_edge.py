'''
Created May 17. 2021

This is a Django command copies "recent" admissions to .csv files
and then emails those files to a distribution list
If no arguments are defined. 
     a. The end of the sample will be the preceeding Saturday night at midnight
     b. The start of the sample will be the Sunday 7 days prior to the end
     c, Start/stop can be overridden on the command line

@author: fsells
'''
import datetime, csv, os, smtplib
from dateutil import relativedelta
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from webapp import sql_api

help = 'blah blah blah 4/9/2020 [--save]'
MIDNIGHT = datetime.timedelta(hours=23, minutes=59)

QUERY = '''select * from CensusApps.dbo.vwEXPORTToRaisersEdge
 WHERE OriginalAdmtDt >= '{}' AND OriginalAdmtDt <='{} 23:59'
  ORDER BY IRLastName, IRFirstName'''

SENDTO=['frederick.sells@riverspring.org',
        'Neusa.Delgado@riverspring.org',
       # 'johanna.perez@riverspring.org',
        #'CensusDev@hebrewhome.org',   ############ WARNING, this distro list fails the send process !!!!
       ]
              
class Command(BaseCommand):
    help = '''USEAGE: email admissions between start and stop dates or for prior week if not specified
                this program will attach files as .csv to email send to raisersedge distribution list
    '''
              
    def add_arguments(self, parser):
        parser.add_argument('--start', action= 'store', help = 'admissions after this date mm/dd/yyyy', 
                           type=lambda s: datetime.datetime.strptime(s, '%m/%d/%Y'),
                            default = None)
        parser.add_argument('--stop', action= 'store', help = 'last day of copy mm/dd/yyyy',  
                           type=lambda s: datetime.datetime.strptime(s, '%m/%d/%Y'),
                            default = None)

        



    def send_email(self, sendto=SENDTO, subject='testing raisers edge', text='', html='testing',  attachments=[]):
        outer = MIMEMultipart("alternative")
        outer['Subject'] = subject
        outer['From'] = 'no-reply@hebrewhome.org'
        outer['To'] = ', '.join(sendto)
        part1 = MIMEText(text, "plain")
        part2 = MIMEText('<p>'+html+'</p>', "html")
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



    def get_sample_period(self, options):
        begin = options.get('start', None)
        stop  = options.get('stop', None)
        today = datetime.date.today()#.replace(hour=0, minute=0, second=0, microsecond=0) 
        prior_sunday = today - datetime.timedelta((today.weekday() + 1) % 7)
        begin = begin or (prior_sunday + relativedelta.relativedelta(weekday=relativedelta.SU(-2)) )
        stop = stop or (prior_sunday + relativedelta.relativedelta(weekday=relativedelta.SA(-1)) )
        begin = begin.strftime('%Y-%m-%d')
        stop = stop.strftime('%Y-%m-%d')
        #print('date range', begin, stop)
        return (begin, stop)

    def scrub_data(self, records):
        PHONE_TYPES = 38, 42, 46  #the columns where the phone types are located
        xxx = records[0].index('xxx')
        records[0][xxx+1] = 'ImportID'  #sql does not allow identical column names in a view.
        for row in records[1:]:
            row[0] = row[0].strftime('%Y-%m-%d %H:%M')
            key = row[1][1:]
            size = len(row)
            for i in range(2,size):
                row[i] = row[i].replace('???', key) 
                for c in PHONE_TYPES:
                    if row[c] == '': row[c-1]=row[c-2]=row[c-3] = ''
        relations = [row[:xxx]for row in records]
        contacts  =[row[xxx+1:] for row in records] 
        return relations, contacts

    def get_admissions_and_contacts(self, start, stop):
        db = sql_api.DatabaseQueryManager()
        sql = QUERY.format(start, stop)
        #print(sql)
        records = db.get_values(sql)
        records = [list(row) for row in records]
        return records
 

    def write_files(self, suffix, records):
        prefix = 'mx_EXPORT_ToRE_'
        datasets =  list(self.scrub_data(records))
        paths = [ os.path.join('D:/Temp/', x.format(prefix,suffix)) for x in ['{}IndividualRelations{}', '{}Constituents{}']]
        merged = zip(datasets, paths)
        for (records, path) in merged:
            #print(path)
            with open(path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(records)
        return paths
        
    def handle(self, *args, **options):
        (start, stop) = self.get_sample_period(options)
        now = datetime.datetime.now()
        suffix = '_{}_to_{}.csv'.format(start, stop)
        #print('xxx{}xxx'.format(suffix))
        text_body = 'Computed on {}'.format(now)
        html_body = 'Computed on {}'.format(now)
        subject='RE Admissions {}...{}'.format(start,stop)
        records = self.get_admissions_and_contacts(start, stop)
        attachments = self.write_files(suffix, records)
        self.send_email(sendto=SENDTO, subject=subject, text=text_body, html=html_body, attachments=attachments)
        print('done {}  records= {} '.format(suffix, len(records)))


    

        
            
            
            
        