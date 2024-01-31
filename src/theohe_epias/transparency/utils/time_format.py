from datetime import datetime,timedelta

def control_time(date,hour):
    if type(date) != tuple and type(date) != list:
        print("Date has to be tuple or list.")
        return False
    try:
        start_date = datetime(year = 2010,month=1,day=1)
        end_date = (datetime.now()+timedelta(days=2)).replace(hour=0,minute=0,second = 0, microsecond = 0 )
        given_date = datetime(year = date[0], month=date[1], day=date[2], hour = hour)
    except Exception as e:
        print(e)
        return False
        
    if start_date <= given_date <= end_date:
        return True
    else:
        print("Date has to be in between {} and {}.".format(start_date,end_date))
        return False

def tuple_to_datetime(date, hour = 0, string_ = True):
    if control_time(date, hour) == False:
        return False
    if string_ ==True:
        hour = "T{:02}:00:00+03:00".format(hour)
        day = "{:04}-{:02}-{:02}".format(*date)
        return day+hour
    else:
        return datetime(year = date[0], month = date[1], day = date[2], hour = hour)
