import requests
import pandas as pd

from theohe_epias.transparency.utils.get_time import get_time_bpm, get_today, get_yesterday, get_this_month
from theohe_epias.transparency.utils.time_format import tuple_to_datetime

class BPM():
    def __init__(self):
        self.information = dict()
        self.information["data"] = dict({
"order_summary_down": {"list":"markets/bpm/data/order-summary-down","export":"markets/bpm/export/order-summary-down"},
"order_summary_up": {"list":"markets/bpm/data/order-summary-up","export":"markets/bpm/export/order-summary-up"},
"system_direction": {"list":"markets/bpm/data/system-direction","export":"markets/bpm/export/system-direction"},
"smp": {"list":"markets/bpm/data/system-marginal-price","export":"markets/bpm/export/system-marginal-price"},
        })

        self.information["details"] = dict({
        })

        self.information["rename_columns"] = dict(
            PTF="PTF (TL/MWh)",
            SMF="SMF (TL/MWh)",
            )

        self.main_url = "https://seffaflik.epias.com.tr/electricity-service/v1/"


    def _get_url(self, attr, function):
        if function in ["export","list"]:
            url = self.main_url + self.information["data"][attr][function]
            return url
        else:
            print("Not Defined Function.")
            return None
        

    def _request_data(self, url, data, function):
        if function == "list":
            return requests.post(url, json=data).json()
        elif function == "export":
            data["exportType"] = "XLSX"
            val = requests.post(url, json=data)
            try:
                res = pd.read_excel(val.content)
                res = res.rename(columns = self.information["rename_columns"]) 
                return res
            except:
                print(val.json()["errors"])
                return val.json()

    def _control_and_format_time_between(self, url, startDate, endDate):
        startDate_tuple = tuple_to_datetime(startDate, string_=False)
        endDate_tuple = tuple_to_datetime(endDate, string_=False)
        check = True if startDate_tuple <= endDate_tuple else False
        if check == False:
            print("EndDate has to be greater or equal to StartDate.")
        if url == None or startDate_tuple == False or endDate_tuple == False or check == False:
            return False
        else:
            startDate = tuple_to_datetime(startDate, string_=True)
            endDate = tuple_to_datetime(endDate, string_=True)
            return [startDate, endDate]

    def _control_and_format_time(self, url, date, hour = 0):
        date = tuple_to_datetime(date, hour= hour)
        if url == None or date == False:
            return False
        else:
            return date

    def order_summary_down(self, 
                        startDate = get_yesterday(),
                        endDate = get_today(),
                        function = "export"):
        """
        Yük Atma (YAT) Talimat Miktarı Listeleme Servisi 
        ----------------------
        0, 1, 2 kodlu Alma Talimat Miktarı (YAT), sistem yönünde elektrik fazlası durumlarda sistemi dengelemek için verilen talimat miktarıdır. Veriler 4 saat önceki talimatları yansıtmaktadır.
        ----------------------
        startDate = (2023,1,1) default: yesterday
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self._get_url("order_summary_down", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result


    def order_summary_up(self, 
                        startDate = get_yesterday(),
                        endDate = get_today(),
                        function = "export"):
        """
        Yük Alma (YAL) Talimat Miktarları Listeleme Servisi 
        ----------------------
        0, 1, 2 kodlu Alma Talimat Miktarı (YAL), sistem yönünde elektrik açığı durumlarda sistemi dengelemek için verilen talimat miktarıdır. Veriler 4 saat önceki talimatları yansıtmaktadır.
        ----------------------
        startDate = (2023,1,1) default: yesterday
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self._get_url("order_summary_up", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result


    def system_direction(self, 
                        startDate = get_yesterday(),
                        endDate = get_today(),
                        function = "export"):
        """
        Sistem Yönü Listeleme Servisi 
        ----------------------
        Sistemde elektrik fazlası veya elektrik açığı olduğunu gösterir. Veriler 4 saat önceki talimatları yansıtmaktadır.
        ----------------------
        startDate = (2023,1,1) default: yesterday
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self._get_url("system_direction", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result


    def smp(self, 
                        startDate = get_yesterday(),
                        endDate = get_today(),
                        function = "export"):
        """
        Sistem Marjinal Fiyatı Listeleme Servisi 
        ----------------------
        Sistem Marjinal Fiyatı, Dengeleme Güç Piyasasında net talimat hacmine karşılık gelen teklifin fiyatıdır. Veriler 4 saat önceki talimatları yansıtmaktadır.
        ----------------------
        startDate = (2023,1,1) default: yesterday
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self._get_url("smp", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result
