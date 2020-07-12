'''
Created on Jan 16, 2020

@author: fsells
'''

from django.core.mail import send_mail as django_send_mail
import datetime

from webapp import utilities
from webapp import email_notification_templates as templates
from webapp.constants import *
from django.conf import settings






def get_email_body(values):
    #print (values.items())
    timestamp = values['timestamp']
    values['date'] = timestamp.strftime('%m/%d/%Y')
    values['time']= timestamp.strftime('%I:%M %p')
    template = templates.get_html_template(values['action'])
    body = template.format(**values)
    #print (body)
    return body


def email_census_edit_notification(recipients, **values): 
    (subject, html) = templates.get_subject_and_body(values)
    #subject = 'TESTING ONLY' + subject
    django_send_mail(
        subject = subject,
        message = 'plain text not supported',
        from_email = NO_REPLY,
        recipient_list = recipients,
        fail_silently=False,
        html_message = html
    )
    return

def email_anything(recipients, subject, body ):
    django_send_mail(
        subject = subject,
        message = 'plain text not supported',
        from_email = NO_REPLY,
        recipient_list = recipients,
        fail_silently=False,
        html_message = body
        )
    return

