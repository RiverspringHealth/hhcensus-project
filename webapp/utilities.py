'''
Created on Dec 28, 2019

@author: fsells
'''

import time, sys , datetime, calendar, os       



class DataObject:
    def __init__(self, kwargs):
        self.__dict__.update(kwargs)
        
    def __repr__(self):
        pairs = list(self.__dict__.items())
        pairs.sort()
        pairs = ['%s=%s'%p for p in pairs]
        text = ', '.join(pairs)
        return text
                                 

def record_elapsed_time(method):

    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print ('%r executed in  %2.2f sec' % (method.__name__,  te-ts) )
        return result

    return timed

@record_elapsed_time
def testor(n):
    for i in range(n):
        x = i**i
    return 'done'

def get_list_of_dates_for_first_of_month(startingdate=None, number_of_months=12):
    date = startingdate or datetime.date.today()
    date = datetime.date(year=date.year, month=date.month, day=1)
    dates = [date]
    year = date.year
    month = date.month
    for i in range(number_of_months):
        month = month - 1  #note the first time i = 0
        if month==0:
            year -= 1
            month = 12
        date = datetime.date(year=year, month=month, day=1)
        dates.append(date)
    return dates

def is_bedcheck_editing_allowed(hour=None):
    hour = hour or 8  #allows you to specify hour for testing, otherwise 8 am.
    now = datetime.datetime.now()
    d = now.replace(hour=hour, minute=0, second=0, microsecond=0)
    return now <= d


def unittest():
    results = is_bedcheck_editing_allowed(9)
    print(results)
    
if __name__=='__main__':

    unittest()    
    
