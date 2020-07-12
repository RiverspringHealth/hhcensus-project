import pyodbc
import datetime
DEBUG = True
PRODUCTION = (r'DRIVER={SQL Server};'
            r'SERVER=HHARWEB2\SQLEXPRESS;'
            r'DATABASE=PositiveCensusReport;'
            r'Trusted_Connection=yes;'    )

TEST = (r'DRIVER={SQL Server};'
            r'SERVER=HHARWEB2\SQLEXPRESS;'
            r'DATABASE=PositiveCensus_Test;'
            r'Trusted_Connection=yes;'    )

LOCAL = (r'DRIVER={SQL Server};'
                r'SERVER=HHSWLSQLDEV01;'
                r'DATABASE=FredTesting;'
                r'Trusted_Connection=yes;'    )

def get_records(conn_str, RepDate):
    sql = '''SELECT * FROM dbo.PositiveCensusReport 
                      WHERE RepDate ='{}'
                      ORDER BY Unit, Room, ResidentName
                      '''.format(RepDate)
    Connection = pyodbc.connect(conn_str)
    Cursor = Connection.cursor()
    Cursor.execute(sql)
    rows = Cursor.fetchall()
    for r in rows:
        r[2] = r[1].strip() + '-' + r[2].strip()
        if r[4]: r[4] = r[4].strip()  #remove whitespace from name
    rows = [r[2:-8] for r in rows if r[1] not in ('M1', 'M2', 'MM')] #eliminate units and fields that should not be compared
    Cursor.close()
    Connection.close()
    return rows

def match_empty_beds(old, new):
    errors = []
    old = [x[0] for x in old if x[1].strip()=='']
    oldset = set(old)
    new = [x[0] for x in new if x[1].strip()=='']
    newset = set(new)
    if len(old) != len(oldset): errors.append("there are duplicates in old")
    if len(new) != len(newset): errors.append("there are duplicates in new")
    intersection = newset & oldset  #intersection
    oldexceptions = oldset-intersection
    newexceptions = newset-intersection
    print('common empty beds ', sorted(intersection))
    print('empty beds in old but not in new', sorted(oldset-intersection))
    print('empty beds in new but not in old', sorted(newset - intersection))
    # extra_old = [x for x in old if x not in new]
    # extra_new = [x for x in new if x not in old]
    # if DEBUG :
    #     for x in zip(old,new):
    #         print(x)
    #
    # if extra_old or extra_new:
    #     error = 'Empty Bed Mismatch: old={}, new={}'.format(str(old), str(new))
    # else:
    #     error = 'Empty Beds all Match'
    return '\n'.join(errors)

def execute(baseline, qa, RepDate):
    old = get_records(baseline, RepDate)
    new = get_records(qa, RepDate)
    if len(old) != len(new): print ('new has {} records and old has {} records')
    #for x,y in zip(old,new):        print(x)
    print( match_empty_beds(old, new))



if __name__=='__main__':
    execute(PRODUCTION, TEST, '2019-10-31')