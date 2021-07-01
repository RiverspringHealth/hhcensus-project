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

SENDTO=['development-census@riverspring.org']
              







class Command(BaseCommand):
    help = '''USEAGE: email admissions between start and stop dates or for prior week if not specified
                this program will attach files as .csv to email send to raisersedge distribution list
    '''
              
    def add_arguments(self, parser):
        parser.add_argument('--start', action= 'store', help = 'admissions after this date mm/dd/yyyy', default = None)
        parser.add_argument('--stop', action= 'store', help = 'last day of copy mm/dd/yyyy',  
                            #type=lambda s: datetime.datetime.strptime(s, '%m/%d/%Y'),
                            default = None)

        

    def ooocompose_email(self, date, shift, totals):
        texttitle = 'Kronos was updated at %s with date=%s and shift=%s\n\n' % (datetime.datetime.now(), date, shift)
        texttotals = ['%10s = %s' % row for row in totals]
        textbody = texttitle + '\n'.join(texttotals)
        #print(textbody)
        subject = 'TESTING ONLY:Kronos update date=%s shift=%s' % (date, shift)
        htmlrecords = ['<TR><TD>%s</TD><TD>%s</TD></TR>' % row for row in totals]
        htmlbody = '<H2>%s</H2><TABLE border="1">%s</TABLE>' % (texttitle, ''.join(htmlrecords))
        #print(htmlbody)
        patients=self.DBAPI.get_inhouse_patients()
        write_file(KRONOS_DETAIL_CSV, patients)
        self.send_email(sendto=SEND_EMAIL_TO, subject=subject, text=textbody, html=htmlbody, path=KRONOS_DETAIL_CSV)

    def send_email(self, sendto=SENDTO, subject='testing raisers edge', text='', html='testing', folder='D:\Temp', attachments=[]):
        outer = MIMEMultipart("alternative")
        outer['Subject'] = subject
        outer['From'] = 'donotreply@hebrewhome.org'
        outer['To'] = ', '.join(sendto)
        part1 = MIMEText(text, "plain")
        part2 = MIMEText('<p>'+html+'</p>', "html")
        outer.attach(part1)
        outer.attach(part2)
        for attachment in attachments:
            path = os.path.join(folder, attachment)
            with open(path, 'rb') as fp:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(fp.read())
            part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(path))
            outer.attach(part)
        s = smtplib.SMTP(settings.EMAIL_HOST)
        s.send_message(outer)
        s.quit()

    def write_file(self, filename, records):
        path = os.path.join('D:/Temp/', filename)
        with open(path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(records)
        return path

    def get_sample_period(self, options):
        begin = options.get('start', None)
        stop  = options.get('stop', None)
        today = datetime.date.today()#.replace(hour=0, minute=0, second=0, microsecond=0) 
        prior_sunday = today - datetime.timedelta((today.weekday() + 1) % 7)
        begin = begin or (prior_sunday + relativedelta.relativedelta(weekday=relativedelta.SU(-2)) )
        stop = stop or (prior_sunday + relativedelta.relativedelta(weekday=relativedelta.SA(-1)) )
        return (begin, stop)
       
        
    def handle(self, *args, **options):
        (start, stop)self.get_sample_period(options)
        print(start)
        print(stoop)
        return
        now = datetime.datetime.now()
        print('handle', args, options)
        db = sql_api.DatabaseQueryManager()
        admissions = db.get_admissions(start, stop)
        contacts = db.get_contacts(start, stop)
        self.write_file('admissions.csv', admissions)
        self.write_file('contacts.csv', contacts)
        self.send_email(sendto=SENDTO, subject='testing raisers edge', text='', html='testing', folder='D:\Temp', 
                        attachments=('admissions.csv', 'contacts.csv'))
        print('done')


    

        
            
            
            
        