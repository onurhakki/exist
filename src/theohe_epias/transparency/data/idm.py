from ..utils.get_time import get_today

class IDM():
    information = dict()
    information["data"] = dict({
"bid_offer_quantities": {"list":"markets/idm/data/bid-offer-quantities","export":"markets/idm/export/bid-offer-quantities"},
"matching_quantity": {"list":"markets/idm/data/matching-quantity","export":"markets/idm/export/matching-quantity"},
"min_max_bid_price": {"list":"markets/idm/data/min-max-bid-price","export":"markets/idm/export/min-max-bid-price"},
"min_max_matching_price": {"list":"markets/idm/data/min-max-matching-price","export":"markets/idm/export/min-max-matching-price"},
"min_max_sales_offer_price": {"list":"markets/idm/data/min-max-sales-offer-price","export":"markets/idm/export/min-max-sales-offer-price"},
"trade_value": {"list":"markets/idm/data/trade-value","export":"markets/idm/export/trade-value"},
"transaction_history": {"list":"markets/idm/data/transaction-history","export":"markets/idm/export/transaction-history"},
"weighted_average_price": {"list":"markets/idm/data/weighted-average-price","export":"markets/idm/export/weighted-average-price"},

    })

    information["details"] = {'bid_offer_quantities': ['startDate', 'endDate', 'function'],
 'matching_quantity': ['organizationId', 'startDate', 'endDate', 'function'],
 'min_max_bid_price': ['startDate', 'endDate', 'function'],
 'min_max_matching_price': ['startDate', 'endDate', 'function'],
 'min_max_sales_offer_price': ['startDate', 'endDate', 'function'],
 'trade_value': ['startDate', 'endDate', 'function'],
 'transaction_history': ['startDate', 'endDate', 'function'],
 'weighted_average_price': ['startDate', 'endDate', 'function']}
    
    information["rename_columns"] = dict(
        PTF="PTF (TL/MWh)",
        SMF="SMF (TL/MWh)",
        )
    def __init__(self, root_url, master):
        self.main_url = root_url + "electricity-service/v1/"
        self.master = master
        self.headers = {"TGT":self.master.tgt_response, "Content-Type": "application/json"}


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

        url = self.master.get_url(self.main_url, self.information, "bid_offer_quantities", function)

        check = self.master.control_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result


    def matching_quantity(self, 
                          organizationId = None,
                        startDate = get_today(),
                        endDate = get_today(),
                        function = "export"):
        """
        GİP Eşleşme Miktarı Listeleme Servisi 
        ----------------------
        Gün İçi Piyasası’nda kontrat türüne göre saatlik veya blok olarak gösterilen toplam eşleşme miktarıdır.
        ----------------------
        organizationId = int default: None
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "matching_quantity", function)

        check = self.master.control_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(
            organizationId = organizationId,
            startDate = startDate,
                    endDate = endDate)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result


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

        url = self.master.get_url(self.main_url, self.information, "min_max_bid_price", function)

        check = self.master.control_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result


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

        url = self.master.get_url(self.main_url, self.information, "min_max_matching_price", function)

        check = self.master.control_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result


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

        url = self.master.get_url(self.main_url, self.information, "min_max_sales_offer_price", function)

        check = self.master.control_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result


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

        url = self.master.get_url(self.main_url, self.information, "trade_value", function)

        check = self.master.control_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result


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

        url = self.master.get_url(self.main_url, self.information, "transaction_history", function)

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
