from datetime import datetime,timedelta
from calendar import monthrange


def get_time_dam():
    now = datetime.now()
    if now.hour < 14:
        return get_today()
    else:
        return get_tomorrow()

def get_time_bpm():
    now = datetime.now()
    if now.hour < 16:
        return get_today()
    else:
        return get_tomorrow()


def get_this_month():
    now = datetime.now()
    return (now.year, now.month, 1) 


def get_today():
    now = datetime.now()
    return (now.year, now.month, now.day) 

def get_year():
    now = datetime.now()
    return (now.year, 1, 1) 

def get_last_year():
    now = datetime.now()
    return (now.year-1, 1, 1) 

def get_yesterday():
    now = datetime.now() - timedelta(days = 1)
    return (now.year, now.month, now. day) 


def get_tomorrow():
    now = datetime.now() + timedelta(days = 1)
    return (now.year, now.month, now. day) 


def get_settlement_date(date):
    y,m,d = date
    period = datetime(y,m,1)
    _,days = monthrange(y,m)
    settlement_date = datetime(period.year, period.month, 15)
    if settlement_date.weekday() == 5:
        settlement_date = settlement_date + timedelta(days = 2)
    elif settlement_date.weekday() == 6:
        settlement_date = settlement_date + timedelta(days = 1)
    
    ### Şeffaflıkta Bir gün sonra yayınlanır
    transparency_date = settlement_date + timedelta(days = 1)
    transparency_date_day = transparency_date.day 
    if d < transparency_date_day:
        selected_period = (period-timedelta(days = 35)).replace(day=1)
        yd, md = selected_period.year, selected_period.month
    else:
        selected_period = (period-timedelta(days = 1)).replace(day=1)
        yd, md = selected_period.year, selected_period.month
    _, dd = monthrange(yd,md)
    return (yd,md,1), (yd,md,dd)

def get_current_settlement_day():
    now = datetime.now()
    y,m,d = now.year, now.month, now.day
    
    fday, lday = get_settlement_date((y,m,d))
    return fday, lday

def get_current_settlement_fday():
    now = datetime.now()
    y,m,d = now.year, now.month, now.day
    
    fday, lday = get_settlement_date((y,m,d))
    return fday

def get_current_settlement_lday():
    now = datetime.now()
    y,m,d = now.year, now.month, now.day
    
    fday, lday = get_settlement_date((y,m,d))
    return lday

