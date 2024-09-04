from ..utils.get_time import get_today, get_last_year

class PFM():
    information = dict()
    information["data"] = dict({
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

    information["details"] = {'contract_price_summary': ['deliveryPeriod',   'loadType',   'year',   'startDate',   'endDate',   'function'],  'ggf': ['deliveryPeriod',   'loadType',   'year',   'startDate',   'endDate',   'function'],  'offer_price': ['startDate', 'endDate', 'function'],  'open_position': ['deliveryPeriod',   'loadType',   'year',   'startDate',   'endDate',   'function'],  'pfm_trade_value': ['deliveryPeriod',   'loadType',   'year',   'startDate',   'endDate',   'function'],  'pfm_transaction_history': ['deliveryPeriod',   'loadType',   'year',   'startDate',   'endDate',   'function'],  'vep_matching_quantity': ['deliveryPeriod',   'loadType',   'year',   'startDate',   'endDate',   'function'],  'load_type_list': ['startDate', 'endDate', 'function'],
 'delivery_period_list': ['startDate', 'endDate', 'function'],
 'delivery_year_list': ['startDate', 'endDate', 'function'],
 'th_delivery_period_list': ['startDate', 'endDate', 'function'],
 'ggf_delivery_period_list': ['startDate', 'endDate', 'function']}


    information["rename_columns"] = dict(
        PTF="PTF (TL/MWh)",
        SMF="SMF (TL/MWh)",
        )

    def __init__(self, root_url, master):
        self.main_url = root_url + "electricity-service/v1/"
        self.master = master
        self.headers = {"TGT":self.master.tgt_response, "Content-Type": "application/json"}

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

        url = self.master.get_url(self.main_url, self.information, "contract_price_summary", function)

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

        check = self.master.control_time_between(url, startDate, endDate)
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
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result

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

        url = self.master.get_url(self.main_url, self.information, "delivery_period_list", function)

        check = self.master.control_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate,
                    )
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result

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

        url = self.master.get_url(self.main_url, self.information, "delivery_year_list", function)

        check = self.master.control_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate,
                    )
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result

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

        url = self.master.get_url(self.main_url, self.information, "ggf", function)

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

        check = self.master.control_time_between(url, startDate, endDate)
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
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result

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

        url = self.master.get_url(self.main_url, self.information, "ggf_delivery_period_list", function)

        check = self.master.control_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate,
                    )
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result

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

        url = self.master.get_url(self.main_url, self.information, "load_type_list", function)

        check = self.master.control_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate,
                    )
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result

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

        url = self.master.get_url(self.main_url, self.information, "offer_price", function)

        check = self.master.control_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate,
                    )
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result

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

        url = self.master.get_url(self.main_url, self.information, "open_position", function)

        check = self.master.control_time_between(url, startDate, endDate)
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
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result

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

        url = self.master.get_url(self.main_url, self.information, "pfm_trade_value", function)

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

        check = self.master.control_time_between(url, startDate, endDate)
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
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result

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

        url = self.master.get_url(self.main_url, self.information, "pfm_transaction_history", function)

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

        check = self.master.control_time_between(url, startDate, endDate)
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
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result

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

        url = self.master.get_url(self.main_url, self.information, "th_delivery_period_list", function)

        check = self.master.control_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate,
                    )
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result

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

        url = self.master.get_url(self.main_url, self.information, "vep_matching_quantity", function)

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

        check = self.master.control_time_between(url, startDate, endDate)
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
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result
