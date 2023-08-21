from calendar import monthrange
import datetime
from timeformat.TimeFormatControl import TimeFormatControl
from param_options.parameters import time_format
class TimeFormat():

    def given_settlement_date_start(period):
        dt = datetime.datetime.strptime(period, time_format)
        return dt.replace(day=1, hour=0).strftime(format = time_format)

    def given_settlement_date_end(period):
        dt = datetime.datetime.strptime(period, time_format)
        mday = monthrange(dt.year, dt.month)[1]
        return dt.replace(day=mday, hour=23).strftime(format = time_format)

    def current_settlement_date_start():
        dt = datetime.datetime.now()

        if dt.day >6:
            ## Get previous month
            dt = dt.replace(day=1)
            dt = dt - datetime.timedelta(days=1)

        else:
            ## Get 2 previous month
            dt = dt - datetime.timedelta(days=dt.day)
            dt = dt - datetime.timedelta(days=monthrange(dt.year, dt.month)[1])            
            dt = dt.replace(day=1)
        
        return dt.replace(day=1, hour=0).strftime(format = time_format)

    def current_settlement_date_end():
        dt = datetime.datetime.now()

        if dt.day >6:
            ## Get previous month
            dt = dt.replace(day=1)
            dt = dt - datetime.timedelta(days=1)

        else:
            ## Get 2 previous month
            dt = dt - datetime.timedelta(days=dt.day)
            dt = dt - datetime.timedelta(days=monthrange(dt.year, dt.month)[1])            
            dt = dt.replace(day=1)
        mday = monthrange(dt.year, dt.month)[1]
        return dt.replace(day=mday, hour=23).strftime(format = time_format)


    def current_settlement_date():
        dt = datetime.datetime.now()

        if dt.day >6:
            ## Get previous month
            dt = dt.replace(day=1)
            dt = dt - datetime.timedelta(days=1)

        else:
            ## Get 2 previous month
            dt = dt - datetime.timedelta(days=dt.day)
            dt = dt - datetime.timedelta(days=monthrange(dt.year, dt.month)[1])            
            dt = dt.replace(day=1)
        
        return dt.replace(day=1, hour=0).strftime(format = time_format)
    
    def get_settlement_date(date):
        if TimeFormatControl.control_month(date):
            try:
                date = (datetime.datetime(year = date[0], month = date[1], day = 1)).strftime(format = time_format)
                return date
            except Exception as err:
                print(err)
                return False
        else:
            return False

            
    def get_settlement_date_day(date):
        if TimeFormatControl.control_day(date):
            try:
                date = (datetime.datetime(year = date[0], month = date[1], day = date[2])).strftime(format = time_format)
                return date
            except Exception as err:
                print(err)
                return False
        else:
            return False

    def get_settlement_date_hour(date):
        if TimeFormatControl.control_hour(date):
            try:
                date = (datetime.datetime(year = date[0], month = date[1], day = date[2], hour = date[3])).strftime(format = time_format)
                return date
            except Exception as err:
                print(err)
                return False
        else:
            return False



    def get_settlement_date_in_period_hour(period):
        try:
            StartDate = TimeFormat.given_settlement_date_start(period)
            EndDate = TimeFormat.given_settlement_date_end(period)

            return StartDate, EndDate
        except Exception as err:
            print(err)
            return False
        
        
        



