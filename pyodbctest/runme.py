import datetime
import mydata_api
import hharweb2db_api


def execute():
    mydata = mydata_api.MyDataQueryManager()
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    rptdate = tomorrow.strftime('%Y-%m-%d')
    beds = mydata.get_beds_x_patients()
    ##########for b in beds: print(b)
    now = datetime.datetime.now()

    hharweb2db_api.insert_bed_occupancy(beds, rptdate, now)


if __name__ == '__main__':
    execute()
