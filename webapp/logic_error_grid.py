import sys, os, datetime, random, calendar, itertools

from django.db.models import Count, Max, Avg, Sum, F
from django.db.models.functions import Lower
from django.db import connection
from django.conf import settings

from webapp import models
from webapp import utilities
################from setuptools._vendor.six import _meth_self


DEBUG = settings.DEBUG  #not used, but need to know how to get it if using DEBUG in settings

EMPTY = 0

class Cell(object):
    def __init__(self):
        self.totals  = 0
        self.yescount = 0
        self.errorcount = 0
        self.notdonecount=0

    def add_error():
        self.total += 1
        self.errors += 1

    def update(self, inbed, reason):
        self.total += 1
        if inbed == 'Yes': self.yescount=1
        elif inbed=='': self.notdonecount +=1
        elif inbed=='No' and reason == '': self.errorcount += 1

    def __repr__(self):
        if self.errorcount == 0: value = '0'
        return '?'


def get_filler(n):
    return [Cell()] *n       

class MonthlySummaryComputer(object):  #red/green grid
    def __init__(self, startdate):
        ndays = calendar.monthrange(startdate.year, startdate.month)[1]
        enddate = datetime.date(year=startdate.year, month=startdate.month, day=ndays)
        daily_residents_queryset = models.NightlyBedCheck.objects.filter(RepDate__range=[startdate, enddate]).exclude(ResidentName=' ').order_by('RepDate', 'Unit')
        units = daily_residents_queryset.order_by('Unit').values_list('Unit', flat=True).distinct()
        repdates =  daily_residents_queryset.order_by('RepDate').values_list('RepDate', flat=True).distinct()
        self.create_empty_grid(repdates, units)
        self.populate_grid( daily_residents_queryset)
        # self.grid=grid
        # ########################################################################self.print_grid(grid)
        # self.units_with_errors = dict(zip(units, zeroes[:]))
        # self.total_days_with_nothing_done_by_unit = dict(zip(units, zeroes))
        # self.get_totals(units, grid)

    def create_empty_grid(self, repdates, units):
        grid = {}
        for date in repdates: 
            grid[date]=dict(zip(units, get_filler(len(units))))
        self.grid = grid

    def populate_grid(self, residents):
        for x in residents:
            cell = self.grid[x.RepDate][x.Unit]
            cell.update(x.Inbed, x.Reason)
        

    def reorganize_grid_by_unit(self, units, grid):
        simple = {}
        for row in grid.values():
            for unit in units:
                simple.setdefault(unit, []).append(row[unit])
        for x in simple.items():    print(x)
        return simple
    
    def get_totals(self, units, grid):
        self.maxdays = max_days = len(set(grid.keys()))
        zeroes = [0] * len(units)
        fullcensus = dict(zip(units, zeroes[:]))
        nocensus = dict(zip(units, zeroes[:]))
        partialcensus = dict(zip(units, zeroes[:]))
        totals = dict(zip(units, zeroes[:]))
        values_by_unit = self.reorganize_grid_by_unit(units, grid)
        for unit, values in values_by_unit.items():
            totals[unit] = max_days
            nocensus[unit] = len([x for x in values if x==EMPTY])
            partialcensus[unit] = len([x for x in values if x!=EMPTY ])
            fullcensus[unit] = totals[unit] - nocensus[unit] - partialcensus[unit]
   
        self.totals = [fullcensus, nocensus, partialcensus, totals]
        for row in self.totals:  row['total']= sum(row.values())
        fullcensus['title'] = 'Days of Full Census Done'
        nocensus['title'] = 'Days of No Census Done'
        partialcensus['title'] = 'Days of Partial Census Done'
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
 