import datetime
from param_options.parameters import time_format


class TimeFormatControl():
    def control_order_period_version_equal(low, high):
        low = datetime.datetime.strptime(low, time_format)
        high = datetime.datetime.strptime(high, time_format)
        if low > high:
            print("Version >= Period.")
            return False
        else:
            return True
        
    def control_order_period_version_higher(low, high):
        low = datetime.datetime.strptime(low, time_format)
        high = datetime.datetime.strptime(high, time_format)
        if low >= high:
            print("Version > Period.")
            return False
        else:
            return True
        
    def control_order_dates_higher(low, high):
        low = datetime.datetime.strptime(low, time_format)
        high = datetime.datetime.strptime(high, time_format)
        if low >= high:
            print("End Date > Start Date.")
            return False
        else:
            return True

    def control_order_dates_equal(low, high):
        low = datetime.datetime.strptime(low, time_format)
        high = datetime.datetime.strptime(high, time_format)

        if low > high:
            print("End Date >= Start Date.")
            return False
        else:
            return True

    def control_order_dates_equal_period_date(low, high):
        low = datetime.datetime.strptime(low, time_format)
        high = datetime.datetime.strptime(high, time_format)

        if low > high:
            print("Start Date >= period.")
            return False
        else:
            return True


    def control_month(date):
        if type(date) != tuple:
            print("Given date has to be in tuple. example for January 2023: (2023,1)")
            return False
        else:
            if len(date) < 2:
                print("Given date has not enough information. example for January 2023: (2023,1)")
                return False
            elif len(date) > 4:
                print("Given date has more information. example for January 2023: (2023,1)")
                return False
            else:
                return True
            
    def control_day(date):
        if type(date) != tuple:
            print("Given date has to be in tuple. example for 1 January 2023 : (2023,1,1)")
            return False
        else:
            if len(date) < 3:
                print("Given date has not enough information. example for 1 January 2023 : (2023,1,1)")
                return False
            elif len(date) > 4:
                print("Given date has more information. example for 1 January 2023 : (2023,1,1)")
                return False
            else:
                return True

    def control_hour(date):
        if type(date) != tuple:
            print("Given date has to be in tuple. example for 1 January 2023 - 05:00 : (2023,1,1,5)")
            return False
        else:
            if len(date) != 4:
                print("Given date has not enough information. example for 1 January 2023 - 05:00 : (2023,1,1,5)")
                return False
            else:
                return True

