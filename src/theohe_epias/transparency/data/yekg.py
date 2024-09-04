import requests
import pandas as pd


from ..utils.get_time import get_today, get_last_year

class YEKG():
    information = dict()
    information["data"] = dict({
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

    information["details"] = {'bilateral_contract_list': ['startDate', 'endDate', 'function'],
 'cancelation_quantity': ['startDate', 'endDate', 'function'],
 'expiry_quantity': ['startDate', 'endDate', 'function'],
 'exported_document_quantity': ['startDate', 'endDate', 'function'],
 'market_bid_ask_quantity': ['startDate', 'endDate', 'function'],
 'min_max_match_amount_list': ['startDate', 'endDate', 'function'],
 'trading_volume': ['startDate', 'endDate', 'function'],
 'weighted_average_price': ['startDate', 'endDate', 'function'],
 'withdrawal_quantity': ['startDate', 'endDate', 'function'],
 'yekg_matching_quantity': ['startDate', 'endDate', 'function']}
 
    information["rename_columns"] = dict(
        PTF="PTF (TL/MWh)",
        SMF="SMF (TL/MWh)",
        )


    def __init__(self, root_url, master):
        self.main_url = root_url + "electricity-service/v1/"
        self.master = master
        self.headers = {"TGT":self.master.tgt_response, "Content-Type": "application/json"}


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

        url = self.master.get_url(self.main_url, self.information, "bilateral_contract_list", function)

        check = self.master.control_time_between(url, startDate, endDate)

        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result

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

        url = self.master.get_url(self.main_url, self.information, "cancelation_quantity", function)

        check = self.master.control_time_between(url, startDate, endDate)

        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result

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

        url = self.master.get_url(self.main_url, self.information, "expiry_quantity", function)

        check = self.master.control_time_between(url, startDate, endDate)

        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result

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

        url = self.master.get_url(self.main_url, self.information, "exported_document_quantity", function)

        check = self.master.control_time_between(url, startDate, endDate)

        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result

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

        url = self.master.get_url(self.main_url, self.information, "market_bid_ask_quantity", function)

        check = self.master.control_time_between(url, startDate, endDate)

        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result

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

        url = self.master.get_url(self.main_url, self.information, "min_max_match_amount_list", function)

        check = self.master.control_time_between(url, startDate, endDate)

        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result

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

        url = self.master.get_url(self.main_url, self.information, "trading_volume", function)

        check = self.master.control_time_between(url, startDate, endDate)

        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result

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

        url = self.master.get_url(self.main_url, self.information, "weighted_average_price", function)

        check = self.master.control_time_between(url, startDate, endDate)

        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result

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

        url = self.master.get_url(self.main_url, self.information, "withdrawal_quantity", function)

        check = self.master.control_time_between(url, startDate, endDate)

        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result

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

        url = self.master.get_url(self.main_url, self.information, "yekg_matching_quantity", function)

        check = self.master.control_time_between(url, startDate, endDate)

        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result