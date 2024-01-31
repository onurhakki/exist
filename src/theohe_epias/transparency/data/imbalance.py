import requests
import pandas as pd

from theohe_epias.transparency.utils.get_time import get_today, get_yesterday, get_this_month, get_current_settlement_day, get_current_settlement_fday, get_current_settlement_lday, get_last_year

from theohe_epias.transparency.utils.time_format import tuple_to_datetime

class IB():
    def __init__(self):
        self.information = dict()
        self.information["data"] = dict({
"dsg_imbalance_quantity": {"list":"markets/imbalance/data/dsg-imbalance-quantity","export":"markets/imbalance/export/dsg-imbalance-quantity"},
"dsg_organization_list": {"list":"markets/imbalance/data/dsg-organization-list"},
"imbalance_amount": {"list":"markets/imbalance/data/imbalance-amount","export":"markets/imbalance/export/imbalance-amount"},
"imbalance_quantity": {"list":"markets/imbalance/data/imbalance-quantity","export":"markets/imbalance/export/imbalance-quantity"},

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
        fday, lday = get_current_settlement_day()
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

    def dsg_imbalance_quantity(self, 
                        dsg = None,
                        startDate = get_last_year(),
                        endDate = get_current_settlement_lday(),
                        function = "export"):
        """
        Dengeden Sorumlu Grup (DSG) Dengesizlik Miktarı Listeleme Servisi 
        ----------------------
        Dengeden sorumlu taraflar dengeleme yükümlülükleri kapsamında bir araya gelerek dengeden sorumlu grup oluşturabilirler. Dengeden sorumlu grup adına grup içinden bir dengeden sorumlu taraf, dengeden sorumlu grubun enerji dengesizliğine ilişkin Piyasa İşletmecisine karşı mali sorumluluğunu üstlenir. Dengeden sorumlu taraflarının portföyünde yer alan organizasyonların piyasa işlemleri neticesinde gerçekleşen üretim/tüketim değerlerinden ne kadar saptığını gösteren miktardır.
        ----------------------
        dsg = int default: None
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self._get_url("dsg_imbalance_quantity", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(dsg = dsg,
                    startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result


    def dsg_organization_list(self,
                        startDate = get_current_settlement_fday(),
                        endDate = get_current_settlement_lday(),
                        function = "list"):
        """
        DSG Organizasyon Listesi Servisi 
        ----------------------
        Dengeden Sorumlu Grup servisinde kullanılan Organizasyon Listesi
        ----------------------
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self._get_url("dsg_organization_list", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result


    def imbalance_amount(self, 
                        startDate = get_current_settlement_fday(),
                        endDate = get_current_settlement_lday(),
                        function = "export"):
        """
        Dengesizlik Tutarı Listeleme Servisi 
        ----------------------
        Piyasa katılımcılarının Gün Öncesi Piyasasındaki Gün İçi Piyasası, Dengeleme Güç Piyasası ve ikili Anlaşma işlemleri neticesinde gerçekleşen üretim/tüketim değerlerinden sapmaları durumunda alacaklı/borçlu olduğu tutardır.
        ----------------------
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self._get_url("imbalance_amount", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result


    def imbalance_quantity(self, 
                        startDate = get_current_settlement_fday(),
                        endDate = get_current_settlement_lday(),
                        function = "export"):
        """
        Dengesizlik Miktarı Listeleme Servisi 
        ----------------------
        Piyasa katılımcılarının Gün Öncesi Piyasasındaki Gün İçi Piyasası, Dengeleme Güç Piyasası ve ikili Anlaşma işlemleri neticesinde gerçekleşen üretim/tüketim değerlerinden ne kadar saptığını gösteren miktardır.
        ----------------------
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self._get_url("imbalance_quantity", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result
