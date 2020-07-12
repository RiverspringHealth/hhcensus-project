'''
Business logic to connect views/urls to database/models
This module SHOULD contain no logic specific to the 
web api
 Author: Fred Sells  10/29/2019
 '''

import sys, os, datetime, random, calendar, itertools

from django.db.models import Count, Max, Avg, Sum, F
from django.db.models.functions import Lower
from django.db import connection
from django.conf import settings

from webapp import models
from webapp import utilities
from setuptools._vendor.six import _meth_self


DEBUG = settings.DEBUG  #not used, but need to know how to get it if using DEBUG in settings
ONEDAY = datetime.timedelta(days=1)

def get_latest_repdate():
    results = models.NightlyBedCheck.objects.all().aggregate(Max('RepDate'))#.values_list('RepDate', flat=True).distinct()
    return results['RepDate__max']



######################################################################print( 'atest', get_latest_repdate())

def get_units( ): 
    units = models.NightlyBedCheck.objects.order_by('Unit').values_list('Unit', flat=True).distinct()
    return list(units)

def get_beds(unit, repdate=None):
    date = repdate or datetime.date.today()
    return models.NightlyBedCheck.objects.filter(RepDate=date, Unit=unit).order_by('Unit', 'Room')

class MonthlySummaryComputer(object):  #red/green grid
    def __init__(self, startdate):
        ndays = calendar.monthrange(startdate.year, startdate.month)[1]
        enddate = datetime.date(year=startdate.year, month=startdate.month, day=ndays)
        queryset = models.NightlyBedCheck.objects.filter(RepDate__range=[startdate, enddate]).order_by('RepDate', 'Unit')
        units = queryset.order_by('Unit').values_list('Unit', flat=True).distinct()
        repdates =  queryset.order_by('RepDate').values_list('RepDate', flat=True).distinct()
        zeroes = [0] * len(units)
        grid = self.get_empty_grid(repdates, units)
        grid = self.populate_grid(grid, queryset)
        self.grid=grid
        ####################################self.print_grid(grid)
        self.units_with_errors = dict(zip(units, zeroes))
        self.total_days_with_nothing_done_by_unit = dict(zip(units, zeroes))
        self.get_totals(units, grid)

    def get_empty_grid(self, repdates, units):
        grid = {}
        zeroes = [0] * len(units)
        for date in repdates: grid[date]=dict(zip(units, zeroes))
        return grid

    def populate_grid(self, grid, queryset):
        residents = queryset.exclude(ResidentName='').exclude( Inbed='YES')
        for x in residents:
            if  (x.Inbed=='No' and x.Reason != ''): 
                pass
            else:
                grid[x.RepDate][x.Unit] += 1
        return grid
    
    def get_totals(self, units, grid):
        self.maxdays = max_days = len(set(grid.keys()))
        zeroes = [0] * len(units)
        fullcensus = dict(zip(units, zeroes))
        nocensus = dict(zip(units, zeroes))
        partialcensus = dict(zip(units, zeroes))
        totals = dict(zip(units, zeroes))
        for row in grid.values():
            for unit in units:
                if row[unit] == max_days:        nocensus[unit] += 1
                elif row[unit] > 0:              partialcensus[unit] += 1
                else:                            fullcensus[unit] += 1
                totals[unit] = max_days
        ##########################self.totals = [fullcensus, nocensus, partialcensus, totals]
        self.totals = [fullcensus, partialcensus, totals]
        for row in self.totals:  row['total']= sum(row.values())
        for row in [fullcensus, totals]: row['total']=''
        fullcensus['title'] = 'Days of Full Census Done'
        nocensus['title'] = ''
        partialcensus['title'] = 'Days of Errors/Incomplete Census'
        totals['title'] = 'Totals'
        fullcensus['background'] = 'green'
        nocensus['background'] = '#cc3300'
        partialcensus['background'] = 'red'
        totals['background'] = 'blue'
 
 
    def print_grid(self, grid):
        print ('----------------------------------------------------')
        for date in grid.keys():
            print(date, grid[date])

    def get_details_by_day_x_unit(self):
        return self.grid
 

def get_errors(unit=None, startdate=None, enddate=None):
    start = startdate or datetime.date.today()  #today if not specified
    end   = enddate or start  #startdate if not specified
    queryset = models.NightlyBedCheck.objects.filter(RepDate__range=(start,end)).exclude(Inbed='Yes').exclude(ResidentName='')
    if unit:
        queryset = queryset.filter(Unit=unit)
    queryset = queryset.exclude(Inbed='NO', Reason__ne='').order_by('Unit', 'Room') #Inbed=blank or Inbed=No and Reason=Blank.
    return queryset.values()  #returns data entry errors.
