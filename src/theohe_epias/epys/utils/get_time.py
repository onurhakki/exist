
from datetime import datetime,timedelta
from calendar import monthrange

def get_settlement_date(date, finalised = True):
    y,m,d = date
    period = datetime(y,m,1)
    _,days = monthrange(y,m)
    if finalised:
        settlement_date = datetime(period.year, period.month, 15)
        if settlement_date.weekday() == 5:
            settlement_date = settlement_date + timedelta(days = 2)
        elif settlement_date.weekday() == 6:
            settlement_date = settlement_date + timedelta(days = 1)
    else:
        settlement_date = datetime(period.year, period.month, 6)
        
    settlement_date_day = settlement_date.day 
    if d < settlement_date_day:
        selected_period = (period-timedelta(days = 33)).replace(day=1)
        yd, md = selected_period.year, selected_period.month
    else:
        selected_period = (period-timedelta(days = 1)).replace(day=1)
        yd, md = selected_period.year, selected_period.month
    _, dd = monthrange(yd,md)
    return (yd,md,1), (yd,md,dd)

def get_current_settlement_days(first_day = True, finalised = True):
    now = datetime.now()
    y,m,d = now.year, now.month, now.day
    fday, lday = get_settlement_date((y,m,d), finalised = finalised)
    if first_day:
        return fday
    else:
        return lday


def get_current_month(first_day = True):
    now = datetime.now()
    y,m,d = now.year, now.month, now.day
    _,days = monthrange(y,m)
    if first_day:
        return (y,m,d)
    else:
        return (y,m,days)

def get_last_day_of_month(date):
    time_format = "%Y-%m-%dT%H:00:00+03:00"
    dt = datetime.strptime(date, time_format)
    mday = monthrange(dt.year, dt.month)[1]
    return dt.replace(day=mday, hour=23).strftime(format = time_format)
