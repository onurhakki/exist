import requests
import pandas as pd

from theohe_epias.transparency.utils.get_time import get_today
from theohe_epias.transparency.utils.time_format import tuple_to_datetime

class IDM():
    def __init__(self):
        self.information = dict()
        self.information["data"] = dict({
"bid_offer_quantities": {"list":"markets/idm/data/bid-offer-quantities","export":"markets/idm/export/bid-offer-quantities"},
"matching_quantity": {"list":"markets/idm/data/matching-quantity","export":"markets/idm/export/matching-quantity"},
"min_max_bid_price": {"list":"markets/idm/data/min-max-bid-price","export":"markets/idm/export/min-max-bid-price"},
"min_max_matching_price": {"list":"markets/idm/data/min-max-matching-price","export":"markets/idm/export/min-max-matching-price"},
"min_max_sales_offer_price": {"list":"markets/idm/data/min-max-sales-offer-price","export":"markets/idm/export/min-max-sales-offer-price"},
"trade_value": {"list":"markets/idm/data/trade-value","export":"markets/idm/export/trade-value"},
"transaction_history": {"list":"markets/idm/data/transaction-history","export":"markets/idm/export/transaction-history"},
"weighted_average_price": {"list":"markets/idm/data/weighted-average-price","export":"markets/idm/export/weighted-average-price"},

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

    def bid_offer_quantities(self, 
                        startDate = get_today(),
                        endDate = get_today(),
                        function = "export"):
        """
        GİP Teklif Edilen Alış Satış Miktarları Listeleme Servisi 
        ----------------------
        Gün İçi Piyasasında sunulan tekliflerin alış ve satış tekliflerinin toplam miktarlarıdır.
        ----------------------
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self._get_url("bid_offer_quantities", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result


    def matching_quantity(self, 
                        startDate = get_today(),
                        endDate = get_today(),
                        function = "export"):
        """
        GİP Eşleşme Miktarı Listeleme Servisi 
        ----------------------
        Gün İçi Piyasası’nda kontrat türüne göre saatlik veya blok olarak gösterilen toplam eşleşme miktarıdır.
        ----------------------
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self._get_url("matching_quantity", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result


    def min_max_bid_price(self, 
                        startDate = get_today(),
                        endDate = get_today(),
                        function = "export"):
        """
        GİP Min - Maks Alış Teklif Fiyatı Listeleme Servisi 
        ----------------------
        Gün İçi Piyasası'nda kontrat türüne göre saatlik veya blok olarak gösterilen en yüksek ve en düşük alış teklif fiyatıdır.
        ----------------------
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self._get_url("min_max_bid_price", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result


    def min_max_matching_price(self, 
                        startDate = get_today(),
                        endDate = get_today(),
                        function = "export"):
        """
        GİP Min - Maks Eşleşme Fiyat Listeleme Servisi 
        ----------------------
        Gün İçi Piyasası'nda kontrat türüne göre saatlik veya blok olarak gösterilen en yüksek ve en düşük eşleşme fiyatıdır.
        ----------------------
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self._get_url("min_max_matching_price", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result


    def min_max_sales_offer_price(self, 
                        startDate = get_today(),
                        endDate = get_today(),
                        function = "export"):
        """
        GİP Min - Maks Satış Teklif Fiyatı Listeleme Servisi 
        ----------------------
        Gün İçi Piyasası'nda kontrat türüne göre saatlik veya blok olarak gösterilen en yüksek ve en düşük satış teklif fiyatıdır.
        ----------------------
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self._get_url("min_max_sales_offer_price", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result


    def trade_value(self, 
                        startDate = get_today(),
                        endDate = get_today(),
                        function = "export"):
        """
        GİP İşlem Hacmi Listeleme Servisi 
        ----------------------
        Gün İçi Piyasası’nda eşleşen alış-satış tekliflerinin saatlik toplam mali değeridir.
        ----------------------
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self._get_url("trade_value", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result


    def transaction_history(self, 
                        startDate = get_today(),
                        endDate = get_today(),
                        function = "export"):
        """
        GİP İşlem Akışı Listeleme Servisi 
        ----------------------
        Gün İçi Piyasası’nda gerçekleşen anlık işlemlerin fiyat ve miktarlarıdır.
        ----------------------
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self._get_url("transaction_history", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result

        
    def weighted_average_price(self, 
                        startDate = get_today(),
                        endDate = get_today(),
                        function = "export"):
        """
        GİP Ağırlıklı Ortalama Fiyat Listeleme Servisi 
        ----------------------
        Gün İçi Piyasası'ndaki her bir kontrata ilişkin işlemlerin saatlik bazda hacimsel ağırlıklı ortalama fiyatıdır.
        ----------------------
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self._get_url("weighted_average_price", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result
