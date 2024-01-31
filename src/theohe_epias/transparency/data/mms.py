import requests
import pandas as pd

from theohe_epias.transparency.utils.get_time import get_today, get_year, get_yesterday, get_tomorrow, get_this_month, get_current_settlement_fday, get_current_settlement_lday
from theohe_epias.transparency.utils.time_format import tuple_to_datetime

class MMS():
    def __init__(self):
        self.information = dict()
        self.information["data"] = dict({
"organization_list": {"list":"generation/data/organization-list"},
"power_plant_list_by_organization_id": {"list":"markets/data/power-plant-list-by-organization-id"},
"uevcb_list_by_power_plant_id": {"list":"markets/data/uevcb-list-by-power-plant-id"},
"market_message_system": {"list":"markets/data/market-message-system","export":"markets/export/market-message-system"},

        })

        self.information["details"] = dict({
        })

        self.information["rename_columns"] = dict(
            PTF="PTF (TL/MWh)",
            SMF="SMF (TL/MWh)",
            )

        self.main_url = "https://seffaflik.epias.com.tr/electricity-service/v1/"
        self.region = "TR1"
        self.regionId = 1


    def _get_url(self, attr, function):
        if function in ["export","list"]:
            url = self.main_url + self.information["data"][attr][function]
            return url
        else:
            print("Not Defined Function.")
            return None
        

    def _request_data(self, url, data, function):
        if function == "list":
            if url in ["https://seffaflik.epias.com.tr/electricity-service/v1/transmission/data/capacity-demand-direction",
"https://seffaflik.epias.com.tr/electricity-service/v1/transmission/data/line-capacities-direction",

            ]:
                return requests.get(url, json=data).json()
            else:
                return requests.post(url, json=data).json()
        elif function == "export":
            data["exportType"] = "XLSX"
            val = requests.post(url, json=data).content
            res = pd.read_excel(val)
            res = res.rename(columns = self.information["rename_columns"]) 
            return res

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

    def _control_and_format_time_between_settlement(self, url, startDate, endDate):
        lday = get_current_settlement_lday()
        lastDate_tuple = tuple_to_datetime(lday, string_=False)
        startDate_tuple = tuple_to_datetime(startDate, string_=False)
        endDate_tuple = tuple_to_datetime(endDate, string_=False)
        settlement_check = True
        check = True if startDate_tuple <= endDate_tuple else False
        if check == False:
            print("EndDate has to be greater or equal to StartDate.")
        if lastDate_tuple < startDate_tuple:
            print("StartDate has to be lower than settlement date {}-{}-{}.".format(*lday))
            settlement_check = False
        if lastDate_tuple < endDate_tuple:
            print("EndDate has to be lower than settlement date {}-{}-{}.".format(*lday))
            settlement_check = False
        if url == None or startDate_tuple == False or endDate_tuple == False or check == False or settlement_check == False:
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


    def organization_list(self, 
                        startDate = get_today(),
                        endDate = get_today(),
                        function = "list"):
        """
        Organizasyon Listesi Getirme Servisi 
        ----------------------
        İstekte verilen başlangıç ve bitiş tarihleri arasında tanımlı organizasyonların listesini döner.
        ----------------------
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self._get_url("organization_list", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result

    def power_plant_list_by_organization_id(self, 
                        organizationId = None,
                        date = get_today(),
                        function = "list"):
        """
        Organizasyon Listesi Getirme Servisi 
        ----------------------
        İstekte verilen başlangıç ve bitiş tarihleri arasında tanımlı organizasyonların listesini döner.
        ----------------------
        organizationId = int default: None
        date = (2023,1,1) default: today
        function = list veya export
        """

        url = self._get_url("power_plant_list_by_organization_id", function)

        date = self._control_and_format_time(url, date)
        if date == False:
            return

        data = dict(startDate = date,
                    organizationId = organizationId)
        self.final_result = self._request_data(url, data, function)
        return self.final_result


    def uevcb_list_by_power_plant_id(self, 
                        powerPlantId,
                        date = get_today(),
                        function = "list"):
        """
        Piyasa Mesaj Sistemi Uevçb Listeleme Servisi 
        ----------------------
        Verilen santral id’ye ait UEVÇB’lerin listesini döner.
        ----------------------
        organizationId = int default: None
        date = (2023,1,1) default: today
        function = list veya export
        """

        url = self._get_url("uevcb_list_by_power_plant_id", function)

        date = self._control_and_format_time(url, date)
        if date == False:
            return

        data = dict(startDate = date,
                    powerPlantId = powerPlantId)
        self.final_result = self._request_data(url, data, function)
        return self.final_result



    def market_message_system(self, 
                        mesajTipId = None,
                        organizationId = None,
                        powerPlantId = None,
                        uevcbId = None,
                        startDate = get_today(),
                        endDate = get_today(),
                        function = "export"):
        """
        Piyasa Mesaj Sistemi Listeleme Servisi
        ----------------------
        İlgili santralin arıza veya bakım bilgileridir.
        ----------------------
        mesajTipId = 0 [0: Arıza, 2: Bakım]
        organizationId = int default: None
        date = (2023,1,1) default: today
        function = list veya export
        """

        url = self._get_url("market_message_system", function)
        if mesajTipId not in [0,2, None]:
            print("mesajTipId should be 0 or 2. [0: Arıza, 2: Bakım]")
            return

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(mesajTipId = mesajTipId,
                        organizationId = organizationId,
                        powerPlantId = powerPlantId,
                        uevcbId = uevcbId,
                        startDate = startDate,
                        endDate = endDate,
                        regionId = self.regionId)
        self.final_result = self._request_data(url, data, function)
        return self.final_result
