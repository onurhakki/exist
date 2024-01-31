import requests
import pandas as pd

from theohe_epias.transparency.utils.get_time import get_today, get_tomorrow, get_this_month
from theohe_epias.transparency.utils.time_format import tuple_to_datetime

class AS():
    def __init__(self):
        self.information = dict()
        self.information["data"] = dict({
"primary_frequency_capacity_amount": {"list":"markets/ancillary-services/data/primary-frequency-capacity-amount","export":"markets/ancillary-services/export/primary-frequency-capacity-amount"},
"primary_frequency_capacity_price": {"list":"markets/ancillary-services/data/primary-frequency-capacity-price","export":"markets/ancillary-services/export/primary-frequency-capacity-price"},
"secondary_frequency_capacity_amount": {"list":"markets/ancillary-services/data/secondary-frequency-capacity-amount","export":"markets/ancillary-services/export/secondary-frequency-capacity-amount"},
"secondary_frequency_capacity_price": {"list":"markets/ancillary-services/data/secondary-frequency-capacity-price","export":"markets/ancillary-services/export/secondary-frequency-capacity-price"},


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

    def primary_frequency_capacity_amount(self, 
                        startDate = get_tomorrow(),
                        endDate = get_tomorrow(),
                        function = "export"):
        """
        Primer Frekans Rezerv Miktarı Listeleme Servisi 
        ----------------------
        Katılımcıların gerçek zamanlı frekans dengeleme için ayırması gereken saatlik toplam birincil frekans kapasite hacimleridir.
        ----------------------
        startDate = (2023,1,1) default: tomorrow
        endDate = (2023,1,1) default: tomorrow
        function = list veya export
        """

        url = self._get_url("primary_frequency_capacity_amount", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result
    def primary_frequency_capacity_price(self, 
                        startDate = get_tomorrow(),
                        endDate = get_tomorrow(),
                        function = "export"):
        """
        Primer Frekans Kontrolü (PFK) Fiyat Listeleme Servisi 
        ----------------------
        Saatlik bazda ihale ile belirlenen PFK kapasite bedelidir.
        ----------------------
        startDate = (2023,1,1) default: tomorrow
        endDate = (2023,1,1) default: tomorrow
        function = list veya export
        """

        url = self._get_url("primary_frequency_capacity_price", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result
    def secondary_frequency_capacity_amount(self, 
                        startDate = get_tomorrow(),
                        endDate = get_tomorrow(),
                        function = "export"):
        """
        Sekonder Frekans Rezerv Miktarı Listeleme Servisi 
        ----------------------
        Saatlik toplam belirlenen rezerv miktarlarıdır.
        ----------------------
        startDate = (2023,1,1) default: tomorrow
        endDate = (2023,1,1) default: tomorrow
        function = list veya export
        """

        url = self._get_url("secondary_frequency_capacity_amount", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result
    def secondary_frequency_capacity_price(self, 
                        startDate = get_tomorrow(),
                        endDate = get_tomorrow(),
                        function = "export"):
        """
        Sekonder Frekans Kontrolü (SFK) Fiyat Listeleme Servisi 
        ----------------------
        Saatlik bazda ihale ile belirlenen SFK kapasite bedelidir.
        ----------------------
        startDate = (2023,1,1) default: tomorrow
        endDate = (2023,1,1) default: tomorrow
        function = list veya export
        """

        url = self._get_url("secondary_frequency_capacity_price", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result
