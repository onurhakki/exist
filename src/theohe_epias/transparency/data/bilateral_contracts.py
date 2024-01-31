import requests
import pandas as pd

from theohe_epias.transparency.utils.get_time import get_today, get_yesterday, get_this_month, get_year
from theohe_epias.transparency.utils.time_format import tuple_to_datetime

class BC():
    def __init__(self):
        self.information = dict()
        self.information["data"] = dict({
"amount_of_bilateral_contracts": {"list":"markets/bilateral-contracts/data/amount-of-bilateral-contracts","export":"markets/bilateral-contracts/export/amount-of-bilateral-contracts"},
"bilateral_contracts_bid_quantity": {"list":"markets/bilateral-contracts/data/bilateral-contracts-bid-quantity","export":"markets/bilateral-contracts/export/bilateral-contracts-bid-quantity"},
"bilateral_contracts_offer_quantity": {"list":"markets/bilateral-contracts/data/bilateral-contracts-offer-quantity","export":"markets/bilateral-contracts/export/bilateral-contracts-offer-quantity"},
"clearing_quantity_organization_list": {"list":"markets/dam/data/clearing-quantity-organization-list"},

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

    def amount_of_bilateral_contracts(self, 
                        startDate = get_year(),
                        endDate = get_today(),
                        function = "export"):
        """
        EÜAŞ - GTŞ İkili Anlaşmalar Listeleme Servisi 
        ----------------------
        Düzenlemeye tabi tarife kapsamına göre EÜAŞ ile GTŞ’lerin arasında yapılan ikili anlaşmaların aylık toplamlarını göstermektedir.
        ----------------------
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self._get_url("amount_of_bilateral_contracts", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result


    def bilateral_contracts_bid_quantity(self,
                        organizationId,
                        startDate = get_today(),
                        endDate = get_today(),
                        function = "export"):
        """
        İkili Anlaşma (İA) Alış Miktarı Listeleme Servisi 
        ----------------------
        İkili anlaşmalara ait alış miktarları verisidir.
        ----------------------
        organizationId = int
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self._get_url("bilateral_contracts_bid_quantity", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(
            organizationId = organizationId,
            startDate = startDate,
            endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result

    def bilateral_contracts_offer_quantity(self, 
                        organizationId,
                        startDate = get_today(),
                        endDate = get_today(),
                        function = "export"):
        """
        İkili Anlaşma (İA) Satış Miktarı Listeleme Servisi 
        ----------------------
        İkili anlaşmalara ait satış miktarı verisidir.
        ----------------------
        organizationId = int
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self._get_url("bilateral_contracts_offer_quantity", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(
            organizationId = organizationId,
            startDate = startDate,
            endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result

    def clearing_quantity_organization_list(self, 
                        period = get_this_month(),
                        function = "list"):
        """
        İkili Anlaşma Eşleşme Miktarı Organizasyon Listeleme Servisi 
        ----------------------
        İkili Anlaşma Eşleşme Miktarı için organizasyonları listeler.
        ----------------------
        period = (2023,1, 1) default: this month
        function = list
        """

        url = self._get_url("clearing_quantity_organization_list", function)

        period = self._control_and_format_time(url, period)
        if period == False:
            return

        data = dict(period = period)
        self.final_result = self._request_data(url, data, function)
        return self.final_result

