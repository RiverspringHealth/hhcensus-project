'''
Created on Jul 10, 2019

This is a Django command that copies data from MyData to the kronos table.

@author: fsells
'''
import datetime, csv, os, smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from webapp import sql_api

SHIFTMAPS = [   (5,   7,'Day'), (13, 15,'Eve'),  (21, 23,'Night') ]

SEND_EMAIL_TO = ['frederick.sells@RiverSpringHealth.org',
                 'david.finkelstein@riverspringhealth.org',
                 'antonique.martin@RiverSpringHealth.org'
                 ]        

KRONOS_DETAIL_CSV = 'D:/Temp/KronosDetail.csv'        

def get_shift(hour):
    for (start, stop, name) in SHIFTMAPS:
        if start<=hour<=stop: return name
    return '%s ERROR' % hour

def write_file(path, records):
    with open(path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(records)
    return path


class Command(BaseCommand):
    help = 'USEAGE: python manage.py kronos [--save]'


    def add_arguments(self, parser):
        parser.add_argument('--save', action= 'store_true', help = 'required to write data to target', default=False)              

    def update_kronos(self, date, shift):
        totals = self.DBAPI.get_unit_totals()
        self.DBAPI.insert_unit_totals( date, shift, totals[1:]) #skip header record
        return totals

    def compose_email(self, date, shift, totals):
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

    def send_email(self, sendto=None, subject='none defined', text='', html='', path=None):
        outer = MIMEMultipart("alternative")
        outer['Subject'] = subject
        outer['From'] = 'kronostesting@hebrewhome.org'
        outer['To'] = ', '.join(sendto)
        part1 = MIMEText(text, "plain")
        part2 = MIMEText('<p>'+html+'</p>', "html")
        outer.attach(part1)
        outer.attach(part2)
        if path:
            with open(path, 'rb') as fp:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(fp.read())
            part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(path))
            outer.attach(part)
        s = smtplib.SMTP(settings.EMAIL_HOST)
        s.send_message(outer)
        s.quit()


    def handle(self, *args, **options):
        self.DBAPI =  sql_api.DatabaseQueryManager(DEBUG=False)
        save = options['save']
        now = datetime.datetime.now()
        shift = get_shift(now.hour)
        date = now.date()
        #print(date, shift)
        if save:
            totals = self.update_kronos(date, shift)
        if now.date() < datetime.date(year=2021, month=1, day=5):
            self.compose_email(date, shift, totals)




    

        
            
            
            
        