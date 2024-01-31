import requests
import pandas as pd

from theohe_epias.transparency.utils.get_time import get_today, get_yesterday, get_this_month, get_year, get_last_year
from theohe_epias.transparency.utils.time_format import tuple_to_datetime

class YEKG():
    def __init__(self):
        self.information = dict()
        self.information["data"] = dict({
"bilateral_contract_list": {"list":"markets/yek-g/data/bilateral-contract-list","export":"markets/yek-g/export/bilateral-contract-list"},
"cancelation_quantity": {"list":"markets/yek-g/data/cancelation-quantity","export":"markets/yek-g/export/cancelation-quantity"},
"expiry_quantity": {"list":"markets/yek-g/data/expiry-quantity","export":"markets/yek-g/export/expiry-quantity"},
"exported_document_quantity": {"list":"markets/yek-g/data/exported-document-quantity","export":"markets/yek-g/export/exported-document-quantity"},
"market_bid_ask_quantity": {"list":"markets/yek-g/data/market-bid-ask-quantity","export":"markets/yek-g/export/market-bid-ask-quantity"},
"min_max_match_amount_list": {"list":"markets/yek-g/data/min-max-match-amount-list","export":"markets/yek-g/export/min-max-match-amount-list"},
"trading_volume": {"list":"markets/yek-g/data/trading-volume","export":"markets/yek-g/export/trading-volume"},
"weighted_average_price": {"list":"markets/yek-g/data/weighted-average-price","export":"markets/yek-g/export/weighted-average-price"},
"withdrawal_quantity": {"list":"markets/yek-g/data/withdrawal-quantity","export":"markets/yek-g/export/withdrawal-quantity"},
"yekg_matching_quantity": {"list":"markets/yek-g/data/yekg-matching-quantity","export":"markets/yek-g/export/yekg-matching-quantity"},

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


    def bilateral_contract_list(self, 
                        startDate = get_last_year(),
                        endDate = get_today(),
                        function = "export"):
        """
        YEK-G İkili Anlaşma Miktarları Listeleme Servisi 
        ----------------------
        Seçilen tarihte hesaplar arası transfer edilen YEK-G Belgelerinin sayısı kaynak ve adet bazlı gösterilir. İkili Anlaşma Piyasasında veriler takip eden iş günü 15:00'dan sonra yayımlanır.
        ----------------------
        startDate = (2023,1,1) default: this year
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self._get_url("bilateral_contract_list", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result
    def cancelation_quantity(self, 
                        startDate = get_last_year(),
                        endDate = get_today(),
                        function = "export"):
        """
        YEK-G İtfa İşlem Miktarları Listeleme Servisi 
        ----------------------
        Seçilen tarihte YEK-G Belgesinin ifşa amacıyla kullanılmak üzere itfa edilme sayısını göstermektedir. Veriler Organize YEK-G ve YEK-G İkili Anlaşmalar Piyasasının takip eden iş günü 15:00'dan sonra yayımlanır.
        ----------------------
        startDate = (2023,1,1) default: this year
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self._get_url("cancelation_quantity", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result
    def expiry_quantity(self, 
                        startDate = get_last_year(),
                        endDate = get_today(),
                        function = "export"):
        """
        İlga edilen YEK-G Belge Miktarı Listeleme Servisi 
        ----------------------
        Seçilen tarihte üretim tarihinden itibaren 12 ay geçmesine rağmen itfa edilmemiş olması sebebiyle İlga edilen YEK-G Belgelerinin sayısını kaynak ve adet bazlı gösterir. İkili Anlaşma Piyasasında veriler takip eden iş günü 15:00'dan sonra, Organize Piyasada ise seans sonrası sürecinden sonra yayımlanır.
        ----------------------
        startDate = (2023,1,1) default: this year
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self._get_url("expiry_quantity", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result
    def exported_document_quantity(self, 
                        startDate = get_last_year(),
                        endDate = get_today(),
                        function = "export"):
        """
        İhraç edilen YEK-G Belge Miktarı Listeleme Servisi 
        ----------------------
        Seçilen tarihte kaynak bazında kullanıcı hesaplarına ihraç edilen toplam YEK-G Belgesi sayısını gösterir. Veriler Organize YEK-G ve YEK-G İkili Anlaşmalar Piyasasının takip eden iş günü 15:00'dan sonra yayımlanır.
        ----------------------
        startDate = (2023,1,1) default: this year
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self._get_url("exported_document_quantity", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result
    def market_bid_ask_quantity(self, 
                        startDate = get_last_year(),
                        endDate = get_today(),
                        function = "export"):
        """
        YEK-G Org. Piyasa Alış/Satış Teklif Miktarı Listeleme Servisi 
        ----------------------
        Kaynak bazlı açılan her bir kontrata ilişkin verilmiş olan alış ve satış teklif miktarlarını göstermektedir.
        ----------------------
        startDate = (2023,1,1) default: this year
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self._get_url("market_bid_ask_quantity", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result
    def min_max_match_amount_list(self, 
                        startDate = get_last_year(),
                        endDate = get_today(),
                        function = "export"):
        """
        YEK-G Min-Max Eşleşme Fiyatları Listeleme Servisi 
        ----------------------
        Seçilen Tarihte YEK-G Belgelerinin kaynak bazında minimum ve maksimum eşleşme fiyatlarını gösterir. Veriler Organize YEK-G Piyasasında seans süresince yayımlanır.
        ----------------------
        startDate = (2023,1,1) default: this year
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self._get_url("min_max_match_amount_list", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result
    def trading_volume(self, 
                        startDate = get_last_year(),
                        endDate = get_today(),
                        function = "export"):
        """
        YEK-G Org. Piyasa İşlem Hacmi Listeleme Servisi 
        ----------------------
        Her bir kaynakta açılan kontratlara verilmiş olan tekliflerin eşleşmesi ile oluşan işlem hacminin gösterilmesi.
        ----------------------
        startDate = (2023,1,1) default: this year
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self._get_url("trading_volume", function)

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
                        startDate = get_last_year(),
                        endDate = get_today(),
                        function = "export"):
        """
        Org. YEK-G Piyasa Ağırlıklı Ortalama Fiyat Listeleme Servisi 
        ----------------------
        Seçilen Tarihte Organize YEK-G Piyasasında belirli bir enerji kaynağına ilişkin YEK-G Belgelesinin eşleştiği fiyatlara göre Ağırlıklı Ortalama Fiyat olarak gösterir.
        ----------------------
        startDate = (2023,1,1) default: this year
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
    def withdrawal_quantity(self, 
                        startDate = get_last_year(),
                        endDate = get_today(),
                        function = "export"):
        """
        İptal edilen YEK-G Belge Miktarı Listeleme Servisi 
        ----------------------
        Seçilen tarihte ihraç ve transfer süresinde oluşabilecek hatalar sebebiyle iptal edilen YEK-G Belgelerinin sayısını kaynak ve adet bazlı gösterir. İkili Anlaşma Piyasası’nda veriler takip eden iş günü 15:00’dan sonra, Organize Piyasa’da ise sean sonrası sürecinden sonra yayımlanır. İkili Anlaşma Piyasası’nda veriler takip eden iş günü 15:00’dan sonra, Organize Piyasa’da ise seans sonrası sürecinden sonra yayımlanır.
        ----------------------
        startDate = (2023,1,1) default: this year
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self._get_url("withdrawal_quantity", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result
    def yekg_matching_quantity(self, 
                        startDate = get_last_year(),
                        endDate = get_today(),
                        function = "export"):
        """
        Org. YEK-G Piyasa Eşleşme Miktarları Listeleme Servisi 
        ----------------------
        Seçilen tarihte YEK-G Belgelerinin kaynak bazında gerçekleşen son eşleşme miktarı ve işlem miktarlarını gösterir. Veriler Organize YEK-G Piyasası’nda seans süresince yayımlanır.
        ----------------------
        startDate = (2023,1,1) default: this year
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self._get_url("yekg_matching_quantity", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result
