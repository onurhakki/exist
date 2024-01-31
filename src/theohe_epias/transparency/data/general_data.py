import requests
import pandas as pd

from theohe_epias.transparency.utils.get_time import get_today, get_yesterday, get_this_month
from theohe_epias.transparency.utils.time_format import tuple_to_datetime

class GD():
    def __init__(self):
        self.information = dict()
        self.information["data"] = dict({
"market_participants": {"list":"markets/general-data/data/market-participants","export":"markets/general-data/export/market-participants"},
"market_participants_organization_filter_list": {"list":"markets/general-data/data/market-participants-organization-filter-list"},
"participant_count_based_upon_license_type": {"list":"markets/general-data/data/participant-count-based-upon-license-type","export":"markets/general-data/export/participant-count-based-upon-license-type"},

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
            if url in ["https://seffaflik.epias.com.tr/electricity-service/v1/markets/general-data/data/market-participants-organization-filter-list"]:
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


    def _control_and_format_time(self, url, date, hour = 0):
        date = tuple_to_datetime(date, hour= hour)
        if url == None or date == False:
            return False
        else:
            return date

    def market_participants(self, 
                        organizationId = None,
                        function = "export"):
        """
        Piyasa Katılımcıları Listeleme Servisi 
        ----------------------
        Piyasa Katılımcıları’nın GÖP, GİP, VEP, YEK-G piyasalarına katılım durumunu belirtir. Ayrıca Tüzel kişilik olarak firmanın aktiflik/pasiflik durumunu bildirir.
        ----------------------
        organizationId = int default: None
        function = list veya export
        """

        url = self._get_url("market_participants", function)
        data = dict(organizationId = organizationId)
        self.final_result = self._request_data(url, data, function)
        return self.final_result


    def market_participants_organization_filter_list(self, 
                        function = "list"):
        """
        Piyasa Katılımcıları Organizasyon Filtre Listesi Servisi 
        ----------------------
        Piyasa Katılımcıları Organizasyon Filtre Listesi
        ----------------------
        function = list veya export
        """

        url = self._get_url("market_participants_organization_filter_list", function)
        data = dict()
        self.final_result = self._request_data(url, data, function)
        return self.final_result


    def participant_count_based_upon_license_type(self, 
                        date = get_today(),
                        function = "export"):
        """
        Lisans Türüne Göre Katılımcı Sayısı Listeleme Servisi 
        ----------------------
        Kamu ve Özel Sektör piyasa katılımcılarının Üretim, Tedarik, Dağıtım, OSB Üretim, İletim ve Görevli Tedaril lisansları türlerine göre toplam sayılarını gösterir. Görevli tedarik şirketleri tüketici grupları için K1 (21), K2 (21) ve K3 (21) olacak şekilde kategorize edilmiştir.
        ----------------------
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self._get_url("participant_count_based_upon_license_type", function)

        date = self._control_and_format_time(url, date)
        if date == False:
            return

        data = dict(startDate = date)
        self.final_result = self._request_data(url, data, function)
        return self.final_result
