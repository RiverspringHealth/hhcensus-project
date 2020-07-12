import datetime
import mydatav02
import hharweb2db_api
import argparse
from argparse import RawTextHelpFormatter
from logging.handlers import _MIDNIGHT

ONEDAY = datetime.timedelta(days=1)

YESTERDAY = datetime.date.today() = ONEDAY


MIDNIGHT_YESTERDAY_TEXT =   YESTERDAY.strftime('%m/%d/%Y') + ' 23:45:00 '
print((_MIDNIGHT))

SWEEPTIME = datetime.datetime.strptime( YESTERDAY.strftime('%m/%d/%Y :%H:%') + )

PRODUCTION = (r'DRIVER={SQL Server};'
            r'SERVER=HHARWEB2\SQLEXPRESS;'
            r'DATABASE=PositiveCensusReport;'
            r'Trusted_Connection=yes;'    )

TEST = (r'DRIVER={SQL Server};'
            r'SERVER=HHARWEB2\SQLEXPRESS;'
            r'DATABASE=PositiveCensus_Test;'
            r'Trusted_Connection=yes;'    )

HHSWLSQLDEV01 = (r'DRIVER={SQL Server};'
                r'SERVER=HHSWLSQLDEV01;'
                r'DATABASE=FredTesting;'
                r'Trusted_Connection=yes;'    )

LAPTOP= (
        r'DRIVER={SQL Server};'
        r'SERVER=.;'
        r'DATABASE=PositiveCensusReport_Test;'
        r'Trusted_Connection=yes;'
    )
CONNECTIONS = dict(prod=PRODUCTION, laptop=LAPTOP, dev=HHSWLSQLDEV01, test=TEST)

KEYS = ', '.join( [key for key in CONNECTIONS.keys()])
NOTE = ('prod: writes to HHARWEB2,PositiveCensusReport',
        '\ntest: writes to HHARWEB2.PositiveCensus_Test',
        '\ndev: writes to HHSWLSQLDEV01.FredTesting'
        '\nlaptop: writes to Freds Laptop db=PositiveCensusReport_Test'
        '\ndefault query mydata but do not save to database'
        )
NOTE = ''.join(NOTE)


parser = argparse.ArgumentParser(description='copies PositiveCensusReport records from local DB to Specified output', formatter_class=RawTextHelpFormatter)
parser.add_argument('--sweeptime', action= 'store', help = 'effective sweep date and time mm/dd/yyyy-hh:mm, for testing',
                            type=lambda s: datetime.datetime.strptime(s, '%m/%d/%Y-%H:%M'),
                            default = datetime.datetime.now())
parser.add_argument('--repdate', action= 'store', help = 'Date Saved in PositiveCensusReport, unusally day after sweep date', 
                    type=lambda s: datetime.datetime.strptime(s, '%m/%d/%Y').date(),
                    default = datetime.date.today()+ONEDAY
                    )
parser.add_argument('--database', action='store', help =  NOTE, 
                    default = None
                    )
parser.add_argument('--print', action= 'store_true', help = "print to stdout (default=False)" , default=False)


def execute(args):
    print('xxxxxxxxxxxxxxxxxxx',args)
    target = parser.database()
    conn_str = CONNECTIONS.get(target, None)

    mydata = mydatav02.MyDataQueryManager()
    beds = mydata.get_beds_x_patients(args.sweeptime)
    if args.print:
        for b in beds: print(b)
    if conn_str:
        #hharweb2db_api.insert_bed_occupancy(conn_str, beds, args.repdate.strftime('%Y-%m-%d'))
        print( 'Sweep Completed at', args.sweeptime, 'repdate=', args.repdate, 'records=', len(beds), 'save to %s', conn_str)
    return len(beds)
 
 
if __name__ == '__main__':
    args = parser.parse_args()
    print(args)
    #parser.print_help()
    #print(args)   
    #nbeds = execute(args)
