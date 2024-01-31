import requests
import pandas as pd

from theohe_epias.transparency.utils.get_time import get_today, get_yesterday, get_this_month, get_last_year
from theohe_epias.transparency.utils.time_format import tuple_to_datetime

class PFM():
    def __init__(self):
        self.information = dict()
        self.information["data"] = dict({
"contract_price_summary": {"list":"markets/pfm/data/contract-price-summary","export":"markets/pfm/export/contract-price-summary"},
"ggf": {"list":"markets/pfm/data/ggf","export":"markets/pfm/export/ggf"},
"offer_price": {"list":"markets/pfm/data/offer-price","export":"markets/pfm/export/offer-price"},
"open_position": {"list":"markets/pfm/data/open-position","export":"markets/pfm/export/open-position"},
"pfm_trade_value": {"list":"markets/pfm/data/pfm-trade-value","export":"markets/pfm/export/pfm-trade-value"},
"pfm_transaction_history": {"list":"markets/pfm/data/pfm-transaction-history","export":"markets/pfm/export/pfm-transaction-history"},
"vep_matching_quantity": {"list":"markets/pfm/data/vep-matching-quantity","export":"markets/pfm/export/vep-matching-quantity"},

"load_type_list": {"list":"markets/pfm/data/load-type-list"},
"delivery_period_list": {"list":"markets/pfm/data/delivery-period-list"},
"delivery_year_list": {"list":"markets/pfm/data/delivery-year-list"},
"th_delivery_period_list": {"list":"markets/pfm/data/th-delivery-period-list"},
"ggf_delivery_period_list": {"list":"markets/pfm/data/ggf-delivery-period-list"},

        })

        self.information["details"] = dict({
            "mcp": ["startDate", "endDate", "function"],
            "interim_mcp": ["date", "function"],
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
            if url in ["https://seffaflik.epias.com.tr/electricity-service/v1/markets/dam/data/interim-mcp-published-status"]:
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
        print(startDate_tuple, endDate_tuple)
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


    def contract_price_summary(self, 
                        deliveryPeriod = None,
                        loadType = None,
                        year = None, 
                        startDate = get_last_year(),
                        endDate = get_today(),
                        function = "export"):
        """
        VEP Kontrat Fiyatları Özet Listeleme Servisi 
        ----------------------
        Seçilen tarihte işleme açık + işlem yapılan kontratların seans içinde ilk, son, en düşük, en yüksek eşleşme fiyatlarını ve GGF’yi göstermektedir.
        ----------------------
        deliveryPeriod = str default: None
        loadType = str default: None
        year = int default: None 
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self._get_url("contract_price_summary", function)

        if deliveryPeriod != None:
            v = self.delivery_period_list(startDate,endDate)["items"]
            v = [i["value"] for i in v]
            if deliveryPeriod not in v:
                print("deliveryPeriod should be in {}.".format(v))
                return

        if loadType != None:
            v = self.load_type_list(startDate,endDate)["items"]
            v = [i["value"] for i in v]
            if loadType not in v:
                print("loadType should be in {}.".format(v))
                return

        if year != None:
            v = self.delivery_year_list(startDate,endDate)["items"]
            v = [int(i["year"]) for i in v]
            if year not in v:
                print("year should be in {}.".format(v))
                return

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check


        data = dict(startDate = startDate,
                    endDate = endDate,
                    deliveryPeriod = deliveryPeriod,
                    loadType = loadType,
                    year = year, 
                    )
        self.final_result = self._request_data(url, data, function)
        return self.final_result

    def delivery_period_list(self, 
                        startDate = get_today(),
                        endDate = get_today(),
                        function = "list"):
        """
        Teslimat Dönemi Listeleme Servisi 
        ----------------------
        VEP sayfaları için Teslimat Dönemi Listesi verir
        ----------------------
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list
        """

        url = self._get_url("delivery_period_list", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate,
                    )
        self.final_result = self._request_data(url, data, function)
        return self.final_result

    def delivery_year_list(self, 
                        startDate = get_today(),
                        endDate = get_today(),
                        function = "list"):
        """
        Teslimat Yılı Listeme Servisi 
        ----------------------
        VEP sayfaları için Teslimat Yılı Listesini verir.
        ----------------------
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list
        """

        url = self._get_url("delivery_year_list", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate,
                    )
        self.final_result = self._request_data(url, data, function)
        return self.final_result

    def ggf(self, 
                        deliveryPeriod = None,
                        loadType = None,
                        year = None, 
                        startDate = get_last_year(),
                        endDate = get_today(),
                        function = "export"):
        """
        VEP Günlük Gösterge Fiyatı Listeleme Servisi 
        ----------------------
        Seçilen tarihte işleme açık kontratların Günlük Gösterge Fiyatını göstermektedir. Seansın açık olduğu her gün işleme açık kontratların ilgili gün için Günlük Gösterge fiyatı saat 16:45'te yayımlanır. Dolar ve Euro kuru olarak fiyatın ait olduğu günden önceki ikinci iş gününe ait Türkiye Cumhuriyet Merkez Bankası efektif alış kuru dikkate alınmaktadır.
        ----------------------
        deliveryPeriod = str default: None
        loadType = str default: None
        year = int default: None 
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self._get_url("ggf", function)

        if deliveryPeriod != None:
            v = self.ggf_delivery_period_list(startDate,endDate)["items"]
            v = [i["value"] for i in v]
            if deliveryPeriod not in v:
                print("deliveryPeriod should be in {}.".format(v))
                return

        if loadType != None:
            v = self.load_type_list(startDate,endDate)["items"]
            v = [i["value"] for i in v]
            if loadType not in v:
                print("loadType should be in {}.".format(v))
                return

        if year != None:
            v = self.delivery_year_list(startDate,endDate)["items"]
            v = [int(i["year"]) for i in v]
            if year not in v:
                print("year should be in {}.".format(v))
                return

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate,
                    deliveryPeriod = deliveryPeriod,
                    loadType = loadType,
                    year = year, 
                    )
        self.final_result = self._request_data(url, data, function)
        return self.final_result

    def ggf_delivery_period_list(self, 
                        startDate = get_today(),
                        endDate = get_today(),
                        function = "list"):
        """
        GGF Teslimat Dönemi Listesi 
        ----------------------
        GGF Teslimat Dönemi Listesi
        ----------------------
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list
        """

        url = self._get_url("ggf_delivery_period_list", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate,
                    )
        self.final_result = self._request_data(url, data, function)
        return self.final_result

    def load_type_list(self, 
                        startDate = get_today(),
                        endDate = get_today(),
                        function = "list"):
        """
        Yük Tipi Listeme Servisi 
        ----------------------
        VEP sayfaları için Yük Tipi listesini verir.
        ----------------------
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list
        """

        url = self._get_url("load_type_list", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate,
                    )
        self.final_result = self._request_data(url, data, function)
        return self.final_result

    def offer_price(self, 
                        startDate = get_last_year(),
                        endDate = get_today(),
                        function = "export"):
        """
        VEP Teklif Fiyatları Listeleme Servisi 
        ----------------------
        VEP'teki her bir kontrata ait en iyi alış ve satış tekliflerine sait fiyat bilgisi, son eşleşme fiyatı ve bir önceki eşleşmeye göre değişimi.
        ----------------------
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self._get_url("offer_price", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate,
                    )
        self.final_result = self._request_data(url, data, function)
        return self.final_result

    def open_position(self, 
                        deliveryPeriod = None,
                        loadType = None,
                        year = None, 
                        startDate = get_last_year(),
                        endDate = get_today(),
                        function = "export"):
        """
        VEP Açık Pozisyon Listeleme Servisi 
        ----------------------
        Seçilen tarihte işleme açık + işlem yapılan kontratların açık pozisyon miktarını göstermektedir.
        ----------------------
        deliveryPeriod = str default: None
        loadType = str default: None
        year = int default: None 
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self._get_url("open_position", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate,
                    deliveryPeriod = deliveryPeriod,
                    loadType = loadType,
                    year = year, 
                    )
        self.final_result = self._request_data(url, data, function)
        return self.final_result

    def pfm_trade_value(self, 
                        deliveryPeriod = None,
                        loadType = None,
                        year = None, 
                        startDate = get_last_year(),
                        endDate = get_today(),
                        function = "export"):
        """
        VEP İşlem Hacmi Listeleme Servisi 
        ----------------------
        Seçilen tarihte işleme açık + işlem yapılan kontratların işlem hacmini göstermektedir.
        ----------------------
        deliveryPeriod = str default: None
        loadType = str default: None
        year = int default: None 
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self._get_url("pfm_trade_value", function)

        if deliveryPeriod != None:
            v = self.delivery_period_list(startDate,endDate)["items"]
            v = [i["value"] for i in v]
            if deliveryPeriod not in v:
                print("deliveryPeriod should be in {}.".format(v))
                return

        if loadType != None:
            v = self.load_type_list(startDate,endDate)["items"]
            v = [i["value"] for i in v]
            if loadType not in v:
                print("loadType should be in {}.".format(v))
                return

        if year != None:
            v = self.delivery_year_list(startDate,endDate)["items"]
            v = [int(i["year"]) for i in v]
            if year not in v:
                print("year should be in {}.".format(v))
                return

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate,
                    deliveryPeriod = deliveryPeriod,
                    loadType = loadType,
                    year = year, 
                    )
        self.final_result = self._request_data(url, data, function)
        return self.final_result

    def pfm_transaction_history(self, 
                        deliveryPeriod = None,
                        loadType = None,
                        year = None, 
                        startDate = get_last_year(),
                        endDate = get_today(),
                        function = "export"):
        """
        VEP İşlem Akışı Listeleme Servisi 
        ----------------------
        Seçilen tarihte işleme açık + işlem yapılan kontratların işlem akışını göstermektedir.
        ----------------------
        deliveryPeriod = str default: None
        loadType = str default: None
        year = int default: None 
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self._get_url("pfm_transaction_history", function)

        if deliveryPeriod != None:
            v = self.th_delivery_period_list(startDate,endDate)["items"]
            v = [i["value"] for i in v]
            if deliveryPeriod not in v:
                print("deliveryPeriod should be in {}.".format(v))
                return

        if loadType != None:
            v = self.load_type_list(startDate,endDate)["items"]
            v = [i["value"] for i in v]
            if loadType not in v:
                print("loadType should be in {}.".format(v))
                return

        if year != None:
            v = self.delivery_year_list(startDate,endDate)["items"]
            v = [int(i["year"]) for i in v]
            if year not in v:
                print("year should be in {}.".format(v))
                return

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check


        data = dict(startDate = startDate,
                    endDate = endDate,
                    deliveryPeriod = deliveryPeriod,
                    loadType = loadType,
                    year = year, 
                    )
        self.final_result = self._request_data(url, data, function)
        return self.final_result

    def th_delivery_period_list(self, 
                        startDate = get_today(),
                        endDate = get_today(),
                        function = "list"):
        """
        VEP İşlem Akışı Teslimat Dönemi Listesi 
        ----------------------
        VEP İşlem Akışı Teslimat Dönemi Listesi
        ----------------------
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list
        """

        url = self._get_url("th_delivery_period_list", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate,
                    )
        self.final_result = self._request_data(url, data, function)
        return self.final_result

    def vep_matching_quantity(self, 
                        deliveryPeriod = None,
                        loadType = None,
                        year = None, 
                        startDate = get_last_year(),
                        endDate = get_today(),
                        function = "export"):
        """
        VEP Eşleşme Miktarı Listeleme Servisi 
        ----------------------
        Seçilen tarihte işleme açık + işlem yapılan kontratların eşleşme miktarını göstermektedir.
        ----------------------
        deliveryPeriod = str default: None
        loadType = str default: None
        year = int default: None 
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self._get_url("vep_matching_quantity", function)

        if deliveryPeriod != None:
            v = self.delivery_period_list(startDate,endDate)["items"]
            v = [i["value"] for i in v]
            if deliveryPeriod not in v:
                print("deliveryPeriod should be in {}.".format(v))
                return

        if loadType != None:
            v = self.load_type_list(startDate,endDate)["items"]
            v = [i["value"] for i in v]
            if loadType not in v:
                print("loadType should be in {}.".format(v))
                return

        if year != None:
            v = self.delivery_year_list(startDate,endDate)["items"]
            v = [int(i["year"]) for i in v]
            if year not in v:
                print("year should be in {}.".format(v))
                return

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate,
                    deliveryPeriod = deliveryPeriod,
                    loadType = loadType,
                    year = year, 
                    )
        self.final_result = self._request_data(url, data, function)
        return self.final_result
