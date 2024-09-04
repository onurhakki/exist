from ..utils.get_time import get_this_month, get_time_dam


class DAM():
    information = dict()
    information["data"] = dict({
        "amount_of_block_buying": {"list":"markets/dam/data/amount-of-block-buying","export":"markets/dam/export/amount-of-block-buying"},
        "amount_of_block_selling": {"list":"markets/dam/data/amount-of-block-selling","export":"markets/dam/export/amount-of-block-selling"},
        "clearing_quantity": {"list":"markets/dam/data/clearing-quantity","export":"markets/dam/export/clearing-quantity"},
        "clearing_quantity_organization_list": {"list":"markets/dam/data/clearing-quantity-organization-list"},
        "day_ahead_market_trade_volume": {"list":"markets/dam/data/day-ahead-market-trade-volume","export":"markets/dam/export/day-ahead-market-trade-volume"},
        "flexible_offer_buying_quantity": {"list":"markets/dam/data/flexible-offer-buying-quantity","export":"markets/dam/export/flexible-offer-buying-quantity"},
        "flexible_offer_selling_quantity": {"list":"markets/dam/data/flexible-offer-selling-quantity","export":"markets/dam/export/flexible-offer-selling-quantity"},
        "interim_mcp": {"list":"markets/dam/data/interim-mcp","export":"markets/dam/export/interim-mcp"},
        "interim_mcp_published_status": {"list":"markets/dam/data/interim-mcp-published-status"},
        "matched_flexible_offer_quantity": {"list":"markets/dam/data/matched-flexible-offer-quantity","export":"markets/dam/export/matched-flexible-offer-quantity"},
        "mcp": {"list":"markets/dam/data/mcp","export":"markets/dam/export/mcp"},
        "price_independent_bid": {"list":"markets/dam/data/price-independent-bid","export":"markets/dam/export/price-independent-bid"},
        "price_independent_offer": {"list":"markets/dam/data/price-independent-offer","export":"markets/dam/export/price-independent-offer"},
        "side_payments": {"list":"markets/dam/data/side-payments","export":"markets/dam/export/side-payments"},
        "submitted_bid_order_volume": {"list":"markets/dam/data/submitted-bid-order-volume","export":"markets/dam/export/submitted-bid-order-volume"},
        "submitted_sales_order_volume": {"list":"markets/dam/data/submitted-sales-order-volume","export":"markets/dam/export/submitted-sales-order-volume"},
        "supply_demand": {"list":"markets/dam/data/supply-demand","export":"markets/dam/export/supply-demand"},
        })
    information["details"] = {
        'amount_of_block_buying': ['startDate', 'endDate', 'function'],
        'amount_of_block_selling': ['startDate', 'endDate', 'function'],
        'clearing_quantity': ['organizationId', 'startDate', 'endDate', 'function'],
        'clearing_quantity_organization_list': ['date', 'function'],
        'day_ahead_market_trade_volume': ['startDate', 'endDate', 'function'],
        'flexible_offer_buying_quantity': ['startDate', 'endDate', 'function'],
        'flexible_offer_selling_quantity': ['startDate', 'endDate', 'function'],
        'interim_mcp': ['date', 'function'],
        'interim_mcp_published_status': ['function'],
        'matched_flexible_offer_quantity': ['startDate', 'endDate', 'function'],
        'mcp': ['startDate', 'endDate', 'function'],
        'price_independent_bid': ['startDate', 'endDate', 'function'],
        'price_independent_offer': ['startDate', 'endDate', 'function'],
        'side_payments': ['startDate', 'endDate', 'function'],
        'submitted_bid_order_volume': ['startDate', 'endDate', 'function'],
        'submitted_sales_order_volume': ['startDate', 'endDate', 'function'],
        'supply_demand': ['hour', 'date', 'function']}
    
    information["rename_columns"] = dict(
        PTF="PTF (TL/MWh)",
        SMF="SMF (TL/MWh)",
        )

    def __init__(self, root_url, master):
        self.main_url = root_url + "electricity-service/v1/"
        self.master = master
        self.headers = {"TGT":self.master.tgt_response, "Content-Type": "application/json"}



    def amount_of_block_buying(self, 
                        startDate = get_time_dam(),
                        endDate = get_time_dam(),
                        function = "export"):
        """
        GÖP Blok Alış Miktarı Listeleme Servisi 
        ----------------------
        Gün Öncesi Piyasası'nda sunulan en az 4 en fazla 24 saati kapsayan ve eşleşen blok alış tekliflerinin toplam miktarıdır.
        ----------------------
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "amount_of_block_buying", function)

        check = self.master.control_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result

        
    def amount_of_block_selling(self, 
                        startDate = get_time_dam(),
                        endDate = get_time_dam(),
                        function = "export"):
        """
        GÖP Blok Satış Miktarı Listeleme Servisi 
        ----------------------
        Gün Öncesi Piyasası'nda sunulan en az 4 en fazla 24 saati kapsayan ve eşleşen blok satış tekliflerinin toplam miktarıdır.
        ----------------------
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "amount_of_block_selling", function)

        check = self.master.control_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result

    def clearing_quantity(self, 
                        organizationId,
                        startDate = get_time_dam(),
                        endDate = get_time_dam(),
                        function = "export",
                        check_list = True):
        """
        GÖP Eşleşme Miktarı Listeleme Servisi 
        ----------------------
        Gün Öncesi Piyasası'nda eşleşen tekliflerin saatlik toplam miktardır.
        ----------------------
        organizationId = int
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "clearing_quantity", function)

        if check_list == True:
            orgs = self.clearing_quantity_organization_list(date = startDate)["items"]
            org_list = [k["organizationId"] for k in orgs]
            if organizationId not in org_list:
                print("organizationId is not in clearing_quantity_organization_list. check these:")
                return orgs

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


    def clearing_quantity_organization_list(self, 
                        date = get_this_month(),
                        function = "list"):
        """
        Göp Eşleşme Miktarı Organizasyon Listeleme Servisi 
        ----------------------
        Göp Eşleşme Miktarı için organizasyonları listeler.
        ----------------------
        date = (2023,1, 1) default: this month
        function = list
        """

        url = self.master.get_url(self.main_url, self.information, "clearing_quantity_organization_list", function)

        date = self.master.control_time(url, date)
        if date == False:
            return

        data = dict(period = date)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result


    def day_ahead_market_trade_volume(self, 
                        startDate = get_time_dam(),
                        endDate = get_time_dam(),
                        function = "export"):
        """
        GÖP İşlem Hacmi Listeleme Servisi 
        ----------------------
        Gün Öncesi Piyasası’nda eşleşen alış tekliflerinin saatlik toplam mali değeridir.
        ----------------------
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "day_ahead_market_trade_volume", function)

        check = self.master.control_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result


    def flexible_offer_buying_quantity(self, 
                        startDate = get_this_month(),
                        endDate = get_time_dam(),
                        function = "export"):
        """
        GÖP Esnek Alış Teklif Miktarı Listeleme Servisi 
        ----------------------
        Gün öncesi piyasasına katılan piyasa katılımcısının, belirli bir teklif zaman aralığında belirtilen teklif süresi için, lot cinsinden uzlaştırma dönemi bazlı değişebilen alış miktarlarını eşleşen ve eşleşmeyen teklif kırılımında içerir.
        ----------------------
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "flexible_offer_buying_quantity", function)

        check = self.master.control_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result


    def flexible_offer_selling_quantity(self, 
                        startDate = get_this_month(),
                        endDate = get_time_dam(),
                        function = "export"):
        """
        GÖP Esnek Satış Teklif Miktarı Listeleme Servisi 
        ----------------------
        Gün öncesi piyasasına katılan piyasa katılımcısının, belirli bir teklif zaman aralığında belirtilen teklif süresi için, lot cinsinden uzlaştırma dönemi bazlı değişebilen satış miktarlarını eşleşen ve eşleşmeyen teklif kırılımında içerir.
        ----------------------
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "flexible_offer_selling_quantity", function)

        check = self.master.control_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result


    def interim_mcp(self, 
                          date = get_time_dam(),
                        function = "export"):
        """
        Kesinleşmemiş Piyasa Takas Fiyatı (K.PTF) Listeme Servisi 
        ----------------------
        Kesinleşmemiş Piyasa Takas Fiyatı , Gün Öncesi Piyasası'na sunulan tekliflerin arz ve talebe göre eşleşmesiyle oluşan itiraz süreci tamamlanmamış saatlik elektrik enerjisi fiyatıdır.İtiraz süreci tamamlanmamış saatlik elektrik enerjisi fiyatıdır.
        ----------------------
        date = (2023,1,1) default: today
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "interim_mcp", function)

        date = self.master.control_time(url, date)
        if date == False:
            return

        data = dict(startDate = date)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result



    def interim_mcp_published_status(self, 
                        function = "list"):
        """
        Kesinleşmemiş Piyasa Takas Fiyatı (K.PTF) yayınlanma durumunu dönen servis 
        ----------------------
        Kesinleşmemiş Piyasa Takas Fiyatı (K.PTF) yayınlanma durumunu dönen servis
        ----------------------
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "interim_mcp_published_status", function)

        data = dict()
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result


    def matched_flexible_offer_quantity(self, 
                        startDate = get_time_dam(),
                        endDate = get_time_dam(),
                        function = "export"):
        """
        GÖP Esnek Teklif Eşleşme Miktarları Listeleme Servisi 
        ----------------------
        Esnek Teklif Eşleşme Miktarları Belirli bir teklif zaman aralığı boyunca belirli bir teklif süresi için değişebilen miktarlardan ve bu miktarlar için tek fiyat bilgilerinden oluşan esnek tekliflerin alış ve satış yönlü eşleşme miktarları
        ----------------------
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "matched_flexible_offer_quantity", function)

        check = self.master.control_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result


    def mcp(self, 
                        startDate = get_time_dam(),
                        endDate = get_time_dam(),
                        function = "export"):
        """
        Piyasa Takas Fiyatı (PTF) Listeleme Servisi 
        ----------------------
        Piyasa Takas Fiyatı, Gün Öncesi Piyasası'na sunulan tekliflerin arz ve talebe göre eşleşmesiyle oluşan saatlik elektrik enerjisi fiyatıdır.Gösterge niteliğindeki Türkiye Cumhuriyet Merkez Bankası döviz alış kuru esas alınmıştır.
        ----------------------
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "mcp", function)

        check = self.master.control_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result


    def price_independent_bid(self, 
                        startDate = get_time_dam(),
                        endDate = get_time_dam(),
                        function = "export"):
        """
        GÖP Fiyattan Bağımsız Alış Teklifi Listeleme Servisi 
        ----------------------
        Gün öncesi piyasasında saatlik olarak fiyat kırılımı oluşturulmadan sunulan alış tekliflerinin toplamıdır.
        ----------------------
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "price_independent_bid", function)

        check = self.master.control_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result


    def price_independent_offer(self, 
                        startDate = get_time_dam(),
                        endDate = get_time_dam(),
                        function = "export"):
        """
        GÖP Fiyattan Bağımsız Satış Teklifi Listeleme Servisi 
        ----------------------
        Gün öncesi piyasasında saatlik olarak fiyat kırılımı oluşturulmadan sunulan satış tekliflerinin toplamıdır.
        ----------------------
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "price_independent_offer", function)

        check = self.master.control_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result


    def side_payments(self, 
                        startDate = get_this_month(),
                        endDate = get_time_dam(),
                        function = "export"):
        """
        GÖP Fark Tutarı Listeleme Servisi 
        ----------------------
        Alış tekliflerinden kaynaklı fark tutarı alış yönlü blok ve esnek teklif eşleşmelerinden, satış tekliflerinden kaynaklı fark tutarı satış yönlü blok ve esnek teklif eşleşmelerinden kaynaklanmaktadır.Fark tutarı hesaplanması ve dağıtılmasına ilişkin detaylar Fark Tutarı Prosedürü’nde yer almaktadır.
        ----------------------
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "side_payments", function)

        check = self.master.control_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result


    def submitted_bid_order_volume(self, 
                        startDate = get_time_dam(),
                        endDate = get_time_dam(),
                        function = "export"):
        """
        GÖP Teklif Edilen Alış Miktarları Listeleme Servisi 
        ----------------------
        Gün Öncesi Piyasası’nda 0 TL/MWh fiyat seviyesine sunulan saatlik, blok ve esnek alış teklif miktarlarının toplamıdır.
        ----------------------
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "submitted_bid_order_volume", function)

        check = self.master.control_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result


    def submitted_sales_order_volume(self, 
                        startDate = get_time_dam(),
                        endDate = get_time_dam(),
                        function = "export"):
        """
        GÖP Teklif Edilen Satış Miktarları Listeleme Servisi 
        ----------------------
        Gün Öncesi Piyasası’nda azami uzlaştırma fiyat seviyesine sunulan saatlik, blok ve esnek satış teklif miktarlarının toplamıdır.Azami Uzlaştırma Fiyatı 01.10.2023 tarihinden itibaren kaldırılmıştır.
        ----------------------
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "submitted_sales_order_volume", function)

        check = self.master.control_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result




    def supply_demand(self, 
                        hour = 0,
                        date = get_time_dam(),
                        function = "export"):
        """
        GÖP Arz-Talep Listeleme Servisi 
        ----------------------
        Her bir fiyat kırılımındaki saatlik teklif miktarına, kabul edilen blok ve esnek teklif miktarlarının ilave edilmesiyle oluşturulmuş teklif setlerinin gösterilmesidir.Arz miktarı: Her bir fiyat kırılımındaki saatlik arz ile kabul edilen blok ve esnek arz miktarının toplamıdır. Talep miktarı: Her bir fiyat kırılımındaki saatlik talep ile kabul edilen blok ve esnek talep miktarının toplamıdır.
        ----------------------
        hour = [0,1,2...,22,23] default: 0
        date = (2023,1,1) default: today
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "supply_demand", function)

        date = self.master.control_time(url, date, hour=hour)
        if date == False:
            return

        data = dict(date = date)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result

