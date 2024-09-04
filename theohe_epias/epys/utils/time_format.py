from datetime import datetime,timedelta

def control_time(date):
    if type(date) != tuple and type(date) != list:
        print("Date has to be tuple or list.")
        return False
    try:
        start_date = datetime(year = 2021,month=1,day=1)
        end_date = (datetime.now()+timedelta(days=2)).replace(hour=0,minute=0,second = 0, microsecond = 0 )
        if len(date) == 2:
            given_date = datetime(year = date[0], month=date[1], day=1)
        elif len(date) == 3:
            given_date = datetime(year = date[0], month=date[1], day=date[2])
        elif len(date) == 4:
            given_date = datetime(year = date[0], month=date[1], day=date[2], hour = date[3])
        else:
            print("Time format is not correct. try: (2023,1,1,0) 2023 January 1 00:00")
            return False
    except Exception as e:
        print(e)
        return False
        
    if start_date <= given_date <= end_date:
        return True
    else:
        print("Date has to be in between {} and {}.".format(start_date,end_date))
        return False

def tuple_to_datetime(date, string_ = True):
    if control_time(date) == False:
        return False
    if string_ ==True:
        hour = "T{:02}:00:00+03:00".format(date[3] if len(date) == 4 else 0)
        if len(date) == 2:
            day = "{:04}-{:02}-01".format(*date)
        elif len(date) == 3:
            day = "{:04}-{:02}-{:02}".format(*date)
        elif len(date) == 4:
            day = "{:04}-{:02}-{:02}".format(*date[:-1])

        return day+hour
    else:
        return datetime(year = date[0], month = date[1], day = date[2], hour = hour)


def control_times(low, high, equal = True, label = "period"):
    time_format = "%Y-%m-%dT%H:00:00+03:00"
    low = datetime.strptime(low, time_format)
    high = datetime.strptime(high, time_format)

    if label == "period":
        low_label = "period"
        high_label = "version"
    elif label == "date":
        low_label = "startDate"
        high_label = "endDate"    
    elif label == "period-date":
        low_label = "period"
        high_label = "startDate"
    else:
        return False
        
    if equal:
        if low > high:
            print("please check: {} > {}.".format(low_label, high_label))
            return False
        else:
            return True
    else:
        if low >= high:
            print("please check: {} > {}.".format(low_label, high_label))
            return False
        else:
            return True
