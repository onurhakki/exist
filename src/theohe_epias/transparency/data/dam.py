import requests
import pandas as pd

from theohe_epias.transparency.utils.get_time import get_today, get_yesterday, get_this_month, get_time_dam
from theohe_epias.transparency.utils.time_format import tuple_to_datetime

class DAM():
    def __init__(self):
        self.information = dict()
        self.information["data"] = dict({
      #      "mcp": {"list":"markets/dam/data/mcp", "export":"markets/dam/export/mcp"},
       #     "interim_mcp": {"list":"markets/dam/data/interim-mcp", "export":"markets/dam/export/interim-mcp"},


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
#"supply_demand_chart_data": {"list":"markets/dam/data/supply-demand-chart-data"},
#"supply_demand_chart_ptf_data": {"list":"markets/dam/data/supply-demand-chart-ptf-data"},
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

        url = self._get_url("amount_of_block_buying", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result

        
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

        url = self._get_url("amount_of_block_selling", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result


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

        url = self._get_url("clearing_quantity", function)

        if check_list == True:
            orgs = self.clearing_quantity_organization_list(date = startDate)["items"]
            org_list = [k["organizationId"] for k in orgs]
            if organizationId not in org_list:
                print("organizationId is not in clearing_quantity_organization_list. check these:")
                return orgs

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

        url = self._get_url("clearing_quantity_organization_list", function)

        date = self._control_and_format_time(url, date)
        if date == False:
            return

        data = dict(period = date)
        self.final_result = self._request_data(url, data, function)
        return self.final_result


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

        url = self._get_url("day_ahead_market_trade_volume", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result


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

        url = self._get_url("flexible_offer_buying_quantity", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result


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

        url = self._get_url("flexible_offer_selling_quantity", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result


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

        url = self._get_url("interim_mcp", function)

        date = self._control_and_format_time(url, date)
        if date == False:
            return

        data = dict(startDate = date)
        self.final_result = self._request_data(url, data, function)
        return self.final_result



    def interim_mcp_published_status(self, 
                        function = "list"):
        """
        Kesinleşmemiş Piyasa Takas Fiyatı (K.PTF) yayınlanma durumunu dönen servis 
        ----------------------
        Kesinleşmemiş Piyasa Takas Fiyatı (K.PTF) yayınlanma durumunu dönen servis
        ----------------------
        function = list veya export
        """

        url = self._get_url("interim_mcp_published_status", function)
        data = dict()
        self.final_result = self._request_data(url, data, function)
        return self.final_result


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

        url = self._get_url("matched_flexible_offer_quantity", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result


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

        url = self._get_url("mcp", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result


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

        url = self._get_url("price_independent_bid", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result


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

        url = self._get_url("price_independent_offer", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result


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

        url = self._get_url("side_payments", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result


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

        url = self._get_url("submitted_bid_order_volume", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result


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

        url = self._get_url("submitted_sales_order_volume", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result


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

        url = self._get_url("supply_demand", function)

        date = self._control_and_format_time(url, date, hour=hour)
        if date == False:
            return

        data = dict(date = date)
        self.final_result = self._request_data(url, data, function)
        return self.final_result


    # def supply_demand_chart_data(self, 
    #                     startDate = get_today(),
    #                     endDate = get_today(),
    #                     function = "export"):
    #     """
    #     Arz Talep Grafik Verisi Veri Listeleme Servisi 
    #     ----------------------
    #     Arz Talep grafik gösterimi için gelmesi gereken verileri getirir.
    #     ----------------------
    #     startDate = (2023,1,1) default: today
    #     endDate = (2023,1,1) default: today
    #     function = list veya export
    #     """

    #     url = self._get_url("supply_demand_chart_data", function)

    #     check = self._control_and_format_time_between(url, startDate, endDate)
    #     if check == False:
    #         return
    #     else:
    #         startDate, endDate = check

    #     data = dict(startDate = startDate,
    #                 endDate = endDate)
    #     self.final_result = self._request_data(url, data, function)
    #     return self.final_result
    # def supply_demand_chart_ptf_data(self, 
    #                     startDate = get_today(),
    #                     endDate = get_today(),
    #                     function = "export"):
    #     """
    #     Arz Talep Grafik Saatlik Ptf Verisi Servisi 
    #     ----------------------
    #     Arz Talep grafik gösterimi için Fiyat,Eşleştirme Miktarı verilerini getirir.
    #     ----------------------
    #     startDate = (2023,1,1) default: today
    #     endDate = (2023,1,1) default: today
    #     function = list veya export
    #     """

    #     url = self._get_url("supply_demand_chart_ptf_data", function)

    #     check = self._control_and_format_time_between(url, startDate, endDate)
    #     if check == False:
    #         return
    #     else:
    #         startDate, endDate = check

    #     data = dict(startDate = startDate,
    #                 endDate = endDate)
    #     self.final_result = self._request_data(url, data, function)
    #     return self.final_result
