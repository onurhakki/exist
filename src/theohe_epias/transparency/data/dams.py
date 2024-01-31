import requests
import pandas as pd

from theohe_epias.transparency.utils.get_time import get_today, get_year, get_yesterday, get_tomorrow, get_this_month, get_current_settlement_fday, get_current_settlement_lday
from theohe_epias.transparency.utils.time_format import tuple_to_datetime

class Dams():
    def __init__(self):
        self.information = dict()
        self.information["data"] = dict({
"active_fullness": {"list":"dams/data/active-fullness","export":"dams/export/active-fullness"},
"active_volume": {"list":"dams/data/active-volume","export":"dams/export/active-volume"},
"basin_list": {"list":"dams/data/basin-list"},
"daily_kot": {"list":"dams/data/daily-kot","export":"dams/export/daily-kot"},
"daily_volume": {"list":"dams/data/daily-volume","export":"dams/export/daily-volume"},
"dam_kot": {"list":"dams/data/dam-kot","export":"dams/export/dam-kot"},
"dam_list": {"list":"dams/data/dam-list"},
"dam_volume": {"list":"dams/data/dam-volume","export":"dams/export/dam-volume"},
"flow_rate_and_installed_power": {"list":"dams/data/flow-rate-and-installed-power","export":"dams/export/flow-rate-and-installed-power"},
"water_energy_provision": {"list":"dams/data/water-energy-provision","export":"dams/export/water-energy-provision"},

        })

        self.information["details"] = dict({
        })

        self.information["rename_columns"] = dict(
            PTF="PTF (TL/MWh)",
            SMF="SMF (TL/MWh)",
            )

        self.main_url = "https://seffaflik.epias.com.tr/electricity-service/v1/"
        self.region = "TR1"


    def _get_url(self, attr, function):
        if function in ["export","list"]:
            url = self.main_url + self.information["data"][attr][function]
            return url
        else:
            print("Not Defined Function.")
            return None
        

    def _request_data(self, url, data, function):
        if function == "list":
            if url in ["https://seffaflik.epias.com.tr/electricity-service/v1/dams/data/basin-list"]:
                return requests.get(url, json=data).json()
            else:
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


    def active_fullness(self, 
                        basinName = None,
                        damName = None,
                        function = "export"):
        """
        Aktif Doluluk Listeleme Servisi 
        ----------------------
        Bir barajın maksimum ve minimum işletme seviyeleri arasındaki hacimin yüzdesidir. Formül: Aktif Doluluk= [( İlgili Tarihteki Seviyeye Karşılık Gelen Hacim – Minimum Hacim ) / ( Maksimum Hacim – Minimum Hacim )] * 100. Veriler saat 17:00 itibariyle nihai halini almaktadır. Baraj verileri günlük olarak verilmektedir. Geriye dönük veri bulunmamaktadır.
        ----------------------
        basinName = str default: None
        damName = str default: None
        function = list veya export
        """

        url = self._get_url("active_fullness", function)
        if basinName != None:
            vals = self.basin_list()
            if basinName not in vals:
                print("basinName is not in vals. check",vals)
                return

        if damName != None:
            vals = self.dam_list()["damList"]
            if damName not in vals:
                print("basinName is not in vals. check",vals)
                return

        data = dict(basinName = basinName,damName=damName)
        self.final_result = self._request_data(url, data, function)
        return self.final_result

    def active_volume(self, 
                        basinName = None,
                        damName = None,
                        function = "export"):
        """
        Aktif Hacim Listeleme Servisi 
        ----------------------
        Bir barajın ilgili tarihteki seviyeye karşılık gelen hacmi ve minimum işletme seviyeleri arasındaki hacimdir. Veriler saat 17:00 itibariyle nihai halini almaktadır. Baraj verileri günlük olarak verilmektedir. Geriye dönük veri verilmemektedir.
        ----------------------
        basinName = str default: None
        damName = str default: None
        function = list veya export
        """

        url = self._get_url("active_volume", function)
        if basinName != None:
            vals = self.basin_list()
            if basinName not in vals:
                print("basinName is not in vals. check",vals)
                return

        if damName != None:
            vals = self.dam_list()["damList"]
            if damName not in vals:
                print("basinName is not in vals. check",vals)
                return

        data = dict(basinName = basinName,damName=damName)
        self.final_result = self._request_data(url, data, function)
        return self.final_result
        
    def basin_list(self, 
                        function = "list"):
        """
        Havza listesini dönen servisir. 
        ----------------------
        Havza listesini dönen servisir.
        ----------------------
        function = list
        """

        url = self._get_url("basin_list", function)

        data = dict()
        self.final_result = self._request_data(url, data, function)
        return self.final_result

    def daily_kot(self, 
                        basinName = None,
                        damName = None,
                        function = "export"):
        """
        Günlük Kot Listeleme Servisi 
        ----------------------
        Barajın ilgili gündeki su yüksekliğini belirtir. Veriler saat 17:00 itibariyle nihai halini almaktadır. Baraj verileri günlük olarak verilmektedir. Geriye dönük veri bulunmamaktadır.
        ----------------------
        basinName = str default: None
        damName = str default: None
        function = list veya export
        """

        url = self._get_url("daily_kot", function)
        if basinName != None:
            vals = self.basin_list()
            if basinName not in vals:
                print("basinName is not in vals. check",vals)
                return

        if damName != None:
            vals = self.dam_list()["damList"]
            if damName not in vals:
                print("basinName is not in vals. check",vals)
                return

        data = dict(basinName = basinName,damName=damName)
        self.final_result = self._request_data(url, data, function)
        return self.final_result

    def daily_volume(self, 
                        basinName = None,
                        damName = None,
                        function = "export"):
        """
        Günlük Hacim Listeleme Servisi 
        ----------------------
        Bir barajın ilgili tarihteki seviyesine karşılık gelen hacimdir. Veriler saat 17:00 itibariyle nihai halini almaktadır. Baraj verileri günlük olarak verilmektedir. Geriye dönük veri verilmemektedir.
        ----------------------
        basinName = str default: None
        damName = str default: None
        function = list veya export
        """

        url = self._get_url("daily_volume", function)
        if basinName != None:
            vals = self.basin_list()
            if basinName not in vals:
                print("basinName is not in vals. check",vals)
                return

        if damName != None:
            vals = self.dam_list()["damList"]
            if damName not in vals:
                print("basinName is not in vals. check",vals)
                return

        data = dict(basinName = basinName,damName=damName)
        self.final_result = self._request_data(url, data, function)
        return self.final_result

    def dam_kot(self, 
                        basinName = None,
                        damName = None,
                        function = "export"):
        """
        Kot Listeleme Servisi 
        ----------------------
        İlgili barajın maximum ve minumum seviyesini gösterir.
        ----------------------
        basinName = str default: None
        damName = str default: None
        function = list veya export
        """

        url = self._get_url("dam_kot", function)
        if basinName != None:
            vals = self.basin_list()
            if basinName not in vals:
                print("basinName is not in vals. check",vals)
                return

        if damName != None:
            vals = self.dam_list()["damList"]
            if damName not in vals:
                print("basinName is not in vals. check",vals)
                return

        data = dict(basinName = basinName,damName=damName)
        self.final_result = self._request_data(url, data, function)
        return self.final_result


    def dam_list(self, 
                        basinName = None,
                        function = "list"):
        """
        Havza ismi ile Barajlar listesini dönen servisir. 
        ----------------------
        Havza ismi ile Barajlar listesini dönen servisir.
        ----------------------
        basinName = str default: None
        function = list veya export
        """

        url = self._get_url("dam_list", function)
        if basinName != None:
            vals = self.basin_list()
            print(vals)


        data = dict(basinName = basinName)
        self.final_result = self._request_data(url, data, function)
        return self.final_result
    def dam_volume(self, 
                        basinName = None,
                        damName = None,
                        function = "export"):
        """
        Hacim Listeleme Servisi 
        ----------------------
        İlgili barajın maksimum ve minumum hacim seviyesini gösterir.
        ----------------------
        basinName = str default: None
        damName = str default: None
        function = list veya export
        """

        url = self._get_url("dam_volume", function)
        if basinName != None:
            vals = self.basin_list()
            if basinName not in vals:
                print("basinName is not in vals. check",vals)
                return

        if damName != None:
            vals = self.dam_list()["damList"]
            if damName not in vals:
                print("basinName is not in vals. check",vals)
                return

        data = dict(basinName = basinName,damName=damName)
        self.final_result = self._request_data(url, data, function)
        return self.final_result

    def flow_rate_and_installed_power(self, 
                        basinName = None,
                        damName = None,
                        function = "export"):
        """
        Debi ve Kurulu Güç Listeleme Servisi 
        ----------------------
        İlgili barajda üniteden geçen suyun miktarını ve barajın kurulu gücünü gösterir.
        ----------------------
        basinName = str default: None
        damName = str default: None
        function = list veya export
        """

        url = self._get_url("flow_rate_and_installed_power", function)
        if basinName != None:
            vals = self.basin_list()
            if basinName not in vals:
                print("basinName is not in vals. check",vals)
                return

        if damName != None:
            vals = self.dam_list()["damList"]
            if damName not in vals:
                print("basinName is not in vals. check",vals)
                return

        data = dict(basinName = basinName,damName=damName)
        self.final_result = self._request_data(url, data, function)
        return self.final_result

    def water_energy_provision(self, 
                        basinName = None,
                        damName = None,
                        function = "export"):
        """
        Suyun Enerji Karşılığı Listeleme Servisi 
        ----------------------
        Barajda yer alan suyun hesaplanan MWh cinsinden enerji karşılığıdır. Veriler saat 17:00 itibariyle nihai halini almaktadır. Baraj verileri günlük olarak verilmektedir. Geriye dönük veri verilmemektedir.
        ----------------------
        basinName = str default: None
        damName = str default: None
        function = list veya export
        """

        url = self._get_url("water_energy_provision", function)
        if basinName != None:
            vals = self.basin_list()
            if basinName not in vals:
                print("basinName is not in vals. check",vals)
                return

        if damName != None:
            vals = self.dam_list()["damList"]
            if damName not in vals:
                print("basinName is not in vals. check",vals)
                return

        data = dict(basinName = basinName,damName=damName)
        self.final_result = self._request_data(url, data, function)
        return self.final_result

