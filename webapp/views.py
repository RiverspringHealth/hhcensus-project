'''
Created on Jul 7, 2019

@author: fsells
'''

import json
import sys, os, datetime, random
from dateutil.relativedelta import relativedelta
import calendar

from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.db.models import Count, Max, Avg, Sum, F
from django.db.models.functions import Lower
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache, cache_control
#from django.contrib.auth.decorators import login_required
#from setuptools._vendor.six import _urllib_request_moved_attributes, _meth_self
import django.db.models.functions as x
from django.contrib.auth.decorators import permission_required


from .models import NightlyBedCheck, INBED_CHOICES, REASON_CHOICES, CensusChangeLog
from webapp import logic_census
from webapp import logic_error_grid
from webapp import utilities
from webapp import sql_api 
from webapp import forms
from . import sql_api
from webapp import email_sender
from webapp.utilities import record_elapsed_time



DEFAULT_UNIT = 'G1'

class MyObject:
    def __init__(self, kwargs):
        self.__dict__.update(kwargs)
        
    def __repr__(self):
        pairs = list(self.__dict__.items())
        pairs.sort()
        pairs = ['%s=%s'%p for p in pairs]
        text = ', '.join(pairs)
        return text

@never_cache
def home(request):
    user = request.META['REMOTE_USER']
    context = dict(user=user, now=datetime.datetime.now().timestamp())#, authenticated=request.user.is_authenticated)
    return render(request, 'webapp/home.html', context)
        
@never_cache     
def logout(request):
    user = request.META['REMOTE_USER']
    context = dict(user=user)#, authenticated=request.user.is_authenticated)
    return render(request, 'webapp/logout.html', context)    

def _update_bed(change, user, now):
    bed = NightlyBedCheck.objects.get(pk=change.id)
    bed.inbed=change.inbed
    bed.reason=change.reason
    bed.comment=change.comment
    bed.updatedby = user
    bed.updatetime = now
    errors = bed.save()
    return True

@never_cache
def daily_error_details(request): ###############################################################
    now=datetime.datetime.now().timestamp()
    user = request.META['REMOTE_USER']
    date = request.GET.get("date", None) 
    TEMPLATE = 'webapp/daily_error_details.html'
    if date:
        date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    else:
        date = datetime.date.today()
    residents = NightlyBedCheck.objects.filter(RepDate=date).exclude(ResidentName='').order_by('Unit', 'Room', )
    NotYes = residents.exclude(Inbed='YES')
    InbedBlank = NotYes.filter(Inbed='')
    InbedNoReasonBlank = NotYes.filter(Inbed='No', Reason='')
    errors = InbedBlank | InbedNoReasonBlank
    errors.order_by('unit', 'Room')
    totals = residents.values_list('Unit').annotate(total=Count('Unit')).order_by('Unit')
    context = dict(date=date, beds=errors, totals=totals, user=user, now=now)
    return render(request, TEMPLATE, context)

@never_cache        
def resident_location(request):
    user = request.META['REMOTE_USER']
    now=datetime.datetime.now().timestamp()
    unit = request.GET.get('unit', DEFAULT_UNIT)
    date = request.GET.get('date', datetime.date.today() )
    beds = logic_census.get_beds(unit, date).exclude(ResidentName=' ')
    ##################################################for b in beds: print( (b) )
    context = dict(user=user, 
                    unit=unit, 
                    units = logic_census.get_units(),
                    beds = beds,
                    now = now,
                    repdate = date
                    )
    return render(request, 'webapp/resident_location.html', context)


#@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
@never_cache
def census_edit(request):
    user = request.META['REMOTE_USER']
    if request.method=='GET':
        locked = datetime.datetime.now().hour >= settings.BED_STATUS_LOCK_HOUR
        unit = request.GET.get('unit', DEFAULT_UNIT)
        beds = logic_census.get_beds(unit)
        for bed in beds:
            if (bed.ResidentNumber == None or bed.ResidentNumber == ' ' or bed.ResidentNumber==''):
                bed.RowClass = "not-occupied" #@todo not-occupied
            else:
                bed.RowClass = "occupied"
            if bed.CurrentAdmitDate == None: continue #nobody in the bed
            bed.CurrentAdmitDate = bed.CurrentAdmitDate.strftime('%#m/%#d/%Y')
        maxdate = datetime.date.today()
        context = dict(user=user, 
                       unit = unit,
                       locked = locked,
                       now = datetime.datetime.now(),
                       units=logic_census.get_units(),
                       inbed_choices = INBED_CHOICES, 
                       reason_choices = REASON_CHOICES,
                       beds=beds, 
                       sweepdate = maxdate.strftime('%A -  %B %#d, %Y'))
        return render(request, 'webapp/censusedit.html', context)


@csrf_exempt
def save_changes(request):  ###########saves changes to In Bed status page.
    user = request.META['REMOTE_USER']
    locked = datetime.datetime.now().hour >= settings.BED_STATUS_LOCK_HOUR
    if not locked:
        now = datetime.datetime.now()
        if request.is_ajax(): 
            data = json.loads(request.body.decode("UTF-8"))
            ###############################################################print('json data', data)
            unit = data.get('unit', 'xxx' )
            patients = data.get('patients', [])
            for p in patients: 
                bed = NightlyBedCheck.objects.get(pk=p['id'])
                bed.Inbed=p['inbed']
                bed.Reason=p['reason']
                bed.Comments=p['comment']
                bed.UpdatedByName = user.replace('HHAR\\', '')
                bed.UpdateDatetime=now
                bed.save()
            context = {'comment': 'update successful'}
            return JsonResponse(context)
        else:
            return HttpResponse('request was not json', request)
    else:
        return HttpResponse('It is too late to make changes')

@never_cache
def monthly_summary(request):
    user = request.META['REMOTE_USER']
    now=datetime.datetime.now().timestamp()
    units=logic_census.get_units()
    this_month = datetime.date.today().replace(day=1)
    months = [ this_month-relativedelta(months=i) for i in range(12)]
    startdate = request.GET.get('start', None)
    if startdate:
        startdate = datetime.datetime.strptime(startdate, '%Y-%m-%d').date()
    else:
        startdate = this_month
    ndays = calendar.monthrange(startdate.year, startdate.month)[1]
    enddate = datetime.date(year=startdate.year, month=startdate.month, day=ndays)
    Summarizer = logic_census.MonthlySummaryComputer(startdate)
    errors = Summarizer.get_details_by_day_x_unit()
    context = dict(user=user, months=months, selectedmonth=startdate, units=units, now=now,
                errors=errors, maxdays=Summarizer.maxdays,  totals=Summarizer.totals)
    return render(request, 'webapp/month_summary.html', context)
    
    
###############################################################################################
@never_cache
def notifications(request):
    user = request.META['REMOTE_USER']
    now=datetime.datetime.now().timestamp()
    TEMPLATE = 'webapp/notifications.html'
    FORM_CLASS = forms.CensusChangeForm
    if request.method == 'POST':
        values =  dict(request.POST.items())
        values.pop('csrfmiddlewaretoken', None)  #don't need this
        values.pop('btnSubmit', None)
        values['timestamp'] = datetime.datetime.now()
        email_sender.email_census_edit_notification(settings.CENSUS_RECIPIENTS, **values)
        date = values.pop('date')
        time = values.pop('time')
        values['eventtime'] = datetime.datetime.strptime( date+time, '%m/%d/%Y%H:%M')
        values['user']  = user.replace('HHAR\\','')
        record = CensusChangeLog(**values)
        record.save()
        return redirect('/webapp/notifications')
    else:  ####################################  GET method ##################################
        action = request.GET.get('action', '0')
        if action == None:
            return render(request, TEMPLATE)
        else:
            patients=forms.CHOICES.Patients
            status_choices=forms.CHOICES.StatusChoices
            form = FORM_CLASS(initial= dict(action=action, user=user))
            context = dict(user=user, form=form, action=action, patients=patients, status_choices = status_choices, now=now)
            return render(request, TEMPLATE, context)
        
# def daily_census_report(request):
#     TEMPLATE = 'webapp/daily_census_report.html'
#     unit = request.GET.get('unit', None)
#     date = request.GET.get('date', None)
#     date = datetime.datetime.strptime('%Y-%m-%d')
#     print(unit, date)
#     context = dict()
#     return render(request, TEMPLATE, context)

