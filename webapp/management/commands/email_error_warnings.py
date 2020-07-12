'''
Created on Feb 27, 2020
The purpose of this module is to send emails to a specified distribution list
for all residents where the inbed status is blank or is no and the reason is blank.
It is executed from an external scheduler at predefined times.

@author: fsells
'''

import sys, os, datetime

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from webapp.constants import *
from webapp import logic_census as logic
from webapp import email_sender

HTML_WRAPPER = '''<meta http-equiv="Content-Type" content="text/html; charset=us-ascii">
                    <h1>CENSUS UPDATE REPORT</h1>
                    <table border="1"><tbody>
                    {}
                    </tbody></table>
                    <br/>
                    Please do not reply to this email; this address is not monitored.
                    '''

def TR(tds):
    text = ' '.join(tds)
    return '<tr>{}</tr>'.format(text or '')

def TH(text):
    return '<th>{}</th>'.format(text or '')

def TD(text):
    return '<td>{}</td>'.format(text or '')

class Command(BaseCommand):
    help = 'Sends Warnings of errors in NightlyBedcheck data'

    def add_arguments(self, parser):
        parser.add_argument('--testonly', action= 'store_true', help = 'print info only, dont send', default=False)
        
    def format_email_body(self, errors):
        header = ['Unit', 'Incomplete Census Records']
        rows = [TR([TH(x) for x in header])]
        totals = {}
        for error in errors:
            unit = error['Unit']
            totals.setdefault(unit,0)
            totals[unit] = totals[unit]+1
        tds = [ [TD(unit), TD(count)] for unit,count in totals.items()]
        [rows.append(TR( x)) for x in tds]
        return HTML_WRAPPER.format( '\n'.join(rows) )

    def send_email(self, errors):
        subject = '{} CENSUS UPDATE REPORT '.format(settings.EMAIL_SUBJECT_PREFIX)
        body=self.format_email_body(errors)
        email_sender.email_anything(settings.CENSUS_UPDATE_REPORT_RECIPIENTS, subject, body)

    def handle(self, *args, **options):
        errors = logic.get_errors() 
        self.send_email(errors)
        
            
            
    
        