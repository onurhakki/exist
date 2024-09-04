from ..utils.get_time import get_today, get_year, get_today, get_year, get_this_month, get_current_settlement_fday, get_current_settlement_lday

class Transmission():
    information = dict()
    information["data"] = dict({

"capacity_demand": {"list":"transmission/data/capacity-demand","export":"transmission/export/capacity-demand-export"},
"capacity_demand_direction": {"list":"transmission/data/capacity-demand-direction"},
"congestion_cost": {"list":"transmission/data/congestion-cost","export":"transmission/export/congestion-cost"},
"entso_w_organization": {"list":"transmission/data/entso-w-organization","export":"transmission/export/entso-w-organization"},
"entso_w_uevcb": {"list":"transmission/data/entso-w-uevcb","export":"transmission/export/entso-w-uevcb"},
"international_line_events": {"list":"transmission/data/international-line-events","export":"transmission/export/international-line-events"},
"iskk_list": {"list":"transmission/data/iskk-list","export":"transmission/export/iskk-list"},
"line_capacities": {"list":"transmission/data/line-capacities","export":"transmission/export/line-capacities"},
"line_capacities_direction": {"list":"transmission/data/line-capacities-direction"},
"nominal_capacity": {"list":"transmission/data/nominal-capacity","export":"transmission/export/nominal-capacity"},
"organization_list": {"list":"transmission/data/organization-list","export":"transmission/export/organization-list"},
"tcat_pre_month_forecast": {"list":"transmission/data/tcat-pre-month-forecast","export":"transmission/export/tcat-pre-month-forecast"},
"tcat_pre_year_forecast": {"list":"transmission/data/tcat-pre-year-forecast","export":"transmission/export/tcat-pre-year-forecast"},
"zero_balance": {"list":"transmission/data/zero-balance","export":"transmission/export/zero-balance"},

        })

    information["details"] = {'capacity_demand': ['direction', 'startDate', 'endDate', 'function'],
 'capacity_demand_direction': ['function'],
 'congestion_cost': ['startDate', 'endDate', 'function'],
 'entso_w_organization': ['organizationId', 'date', 'function'],
#  'entso_w_uevcb': ['uevcbName', 'provinceId', 'date','function'],
 'international_line_events': ['startDate', 'endDate', 'function'],
 'iskk_list': ['startDate', 'endDate', 'function'],
 'line_capacities': ['direction', 'startDate', 'endDate', 'function'],
 'line_capacities_direction': ['function'],
 'nominal_capacity': ['startDate', 'endDate', 'function'],
 'organization_list': ['organizationId', 'date', 'function'],
 'tcat_pre_month_forecast': ['startDate', 'endDate', 'function'],
 'tcat_pre_year_forecast': ['startDate', 'endDate', 'function'],
 'zero_balance': ['startDate', 'endDate', 'function']}



    information["rename_columns"] = dict(
            PTF="PTF (TL/MWh)",
            SMF="SMF (TL/MWh)",
            )


    def __init__(self, root_url, master):
        self.main_url = root_url + "electricity-service/v1/"
        self.master = master
        self.headers = {"TGT":self.master.tgt_response, "Content-Type": "application/json"}

    def capacity_demand(self, 
    direction = "TRGR",
                        startDate = get_today(),
                        endDate = get_today(),
                        function = "export"):
        """
        Kapasite Talepleri Listeleme Servisi 
        ----------------------
        Kapasite ihalelerine ait talepleri ve tahsis edilen kapasiteleri gösterir. Kapasite ihalelerine ait talepleri ve tahsis edilen kapasiteleri gösterir.
        ----------------------
        direction = TRGR or [GRTR, TRBG, BGTR]
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        if direction not in ["TRGR","GRTR", "TRBG", "BGTR"]:
            print("direction is not correct.")
            return 
        url = self.master.get_url(self.main_url, self.information, "capacity_demand", function)

        check = self.master.control_time_between(url, startDate, endDate)

        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(direction = direction, 
                    startDate = startDate,
                    endDate = endDate)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result

    def capacity_demand_direction(self, 
                        function = "list"):
        """
        Kapasite talepleri yön servisleri  
        ----------------------
        Kapasite talepleri yön servisleri
        ----------------------
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "capacity_demand_direction", function)

        data = dict()
        self.result = self.master.request_data_get(url, data, function, self.headers, self.information)
        return self.result


    def congestion_cost(self, 
                        orderType = "BOTH_REGULATIONS",
                        priceType = "MCP",
                        startDate = get_today(),
                        endDate = get_today(),
                        function = "export"):
        """
        Kısıt Maliyeti Listeleme Servisi 
        ----------------------
        Şehir bazında 1 kodlu Yük Alma ve Yük Atma Talimatlarının toplam mali değerine ilişkin veri seti. Formül: Kısıt Maliyeti=(YAL talimat Miktarı)* [YAL Teslimat Fiyatı – Seçilen Fiyat] + (YAL Talimat Miktarı)* [Seçilen Fiyat-YAT Talimat Fiyatı].
        ----------------------
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        if orderType not in ["UP_REGULATION", "DOWN_REGULATION", "BOTH_REGULATIONS"]:
            print("select order type: UP_REGULATION, DOWN_REGULATION or BOTH_REGULATIONS")
            return 
        if priceType not in ["MCP", "SMP"]:
            print("select price type: MCP or SMP")
            return 


        url = self.master.get_url(self.main_url, self.information, "congestion_cost", function)

        check = self.master.control_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(
            orderType = orderType,
            priceType = priceType,
            startDate = startDate,
                    endDate = endDate,
                    region = self.master.region)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result



    def entso_w_organization(self, 
                        organizationId = None,
                        date = get_current_settlement_fday(),
                        function = "export"):
        """
        ENTSO-E (W) Kodları Listeleme Servisi 
        ----------------------
        Avrupa Elektrik İletim Sistemi İşletmecileri Ağı’nın piyasadaki Santral ve UEVÇB’lere, Avrupa standartlarına uygun formatta tanımladığı Enerji Tanımlama Kodu’dur.
        ----------------------
        organizationId = int default: None
        date = (2023,1,1) default: today
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "entso_w_organization", function)

        date = self.master.control_time(url, date)

        if date == False:
            return

        data = dict(organizationId = organizationId,
                    period = date)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result

    def entso_w_uevcb(self, 
    uevcbName = None,
    provinceId = None,
    date = get_current_settlement_fday(),
                        function = "export"):
        """
        ENTSO-E (W) UEVCB Listeleme Servisi 
        ----------------------
        ENTSO-E (W) UEVCB Listeleme Servisi
        ----------------------
        uevcbName = int default: None
        provinceId = int default: None
        date = (2023,1,1) default: today
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "entso_w_uevcb", function)

        date = self.master.control_time(url, date)

        if date == False:
            return

        data = dict(uevcbName = uevcbName,
    provinceId = provinceId,
    period = date)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result


    def international_line_events(self, 
                        startDate = get_year(),
                        endDate = get_today(),
                        function = "export"):
        """
        Enterkonneksiyon Arıza Bakım Bildirimleri Listeleme Servisi 
        ----------------------
        TCAT'ten temin edilen uluslararası hatlarda oluşan kesinti bilgileri sayfasıdır.
        ----------------------
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """
        url = self.master.get_url(self.main_url, self.information, "international_line_events", function)

        check = self.master.control_time_between(url, startDate, endDate)

        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result


    def iskk_list(self, 
                        startDate = get_current_settlement_fday(),
                        endDate = get_current_settlement_lday(),
                        function = "export"):
        """
        İletim Sistemi Kayıp Katsayısı (ISKK) Listeleme Servisi 
        ----------------------
        Uzlaştırma dönemi bazında iletim sistemi veriş ve çekiş miktarları arasındaki farkın veriş miktarına oranlanmasıyla hesaplanan iletim sistemi kayıp katsayısına ilişkin veri seti.
        ----------------------
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "iskk_list", function)

        check = self.master.control_time_between(url, startDate, endDate)
        
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result

    def line_capacities(self, 
    direction = "TRGR",
                        startDate = get_today(),
                        endDate = get_today(),
                        function = "export"):
        """
        Hat Kapasiteleri listeleme servisi 
        ----------------------
        Enterkonneksiyonlara ait hat toplam kapasite ve Kullanıma açık kapasite değerleri gösterilmektedir. Enterkonneksiyonlara ait hat toplam kapasite ve Kullanıma açık kapasite değerleri gösterilmektedir.
        ----------------------
        direction = TRGR or [GRTR, TRBG, BGTR]
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        if direction not in ["TRGR","GRTR", "TRBG", "BGTR"]:
            print("direction is not correct.")
            return 

        url = self.master.get_url(self.main_url, self.information, "line_capacities", function)

        check = self.master.control_time_between(url, startDate, endDate)

        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(direction = direction, 
                    startDate = startDate,
                    endDate = endDate)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result


    def line_capacities_direction(self, 
                        function = "list"):
        """
        Hat kapasiteleri yön listeleme servisi 
        ----------------------
        Hat kapasiteleri yön listeleme servisi
        ----------------------
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "line_capacities_direction", function)

        data = dict()
        self.result = self.master.request_data_get(url, data, function, self.headers, self.information)
        return self.result

    def nominal_capacity(self, 
                        startDate = get_current_settlement_fday(),
                        endDate = get_current_settlement_lday(),
                        function = "export"):
        """
        Nomine Kapasite Listeleme Servisi 
        ----------------------
        Nomine Kapasite değerleri ithalat (satış miktarları) ve ihracat(alış miktarı) için yapılan ikili anlaşmaları göstermektedir.
        ----------------------
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "nominal_capacity", function)

        check = self.master.control_time_between(url, startDate, endDate)

        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result


    def organization_list(self, 
                        organizationId = None,
                        date = get_current_settlement_fday(),
                        function = "export"):
        """
        ENTSO-E (X) Kodları Listeleme Servisi 
        ----------------------
        Avrupa Elektrik İletim Sistemi İşletmecileri Ağı’nın piyasadaki organizasyonlara, Avrupa standartlarına uygun formatta tanımladığı Enerji Tanımlama Kodu’dur.
        ----------------------
        organizationId = int default: None
        date = (2023,1,1) default: today
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "organization_list", function)

        date = self.master.control_time(url, date)

        if date == False:
            return


        data = dict(organizationId = organizationId,
                    period = date)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result


    def tcat_pre_month_forecast(self, 
                        startDate = get_current_settlement_fday(),
                        endDate = get_today(),
                        function = "export"):
        """
        Enterkonneksiyon Kapasitesine İlişkin Ay Öncesi Tahminler Listeleme Servisi 
        ----------------------
        Transfer yönü kapsamında ay öncesi Net Transfer Kapasitesi, Kullanıma Açık Kapasite ve Tahsis Edilmiş Kapasite değerlerinin ay öncesi tahminlerine ilişkin veri seti.
        ----------------------
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "tcat_pre_month_forecast", function)

        check = self.master.control_time_between(url, startDate, endDate)

        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result

    def tcat_pre_year_forecast(self, 
                        startDate = get_this_month(),
                        endDate = get_today(),
                        function = "export"):
        """
        Enterkonneksiyon Kapasitesine İlişkin Yıl Öncesi Tahminler Listeleme Servisi 
        ----------------------
        Transfer yönü kapsamında yıl öncesi Net Transfer Kapasitesi, Kullanıma Açık Kapasite ve Tahsis Edilmiş Kapasite değerlerinin yıl öncesi tahminlerine ilişkin veri seti.
        ----------------------
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "tcat_pre_year_forecast", function)

        check = self.master.control_time_between(url, startDate, endDate)

        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result

    def zero_balance(self, 
                        startDate = get_year(),
                        endDate = get_current_settlement_lday(),
                        function = "export"):
        """
        Sıfır Bakiye Düzeltme Tutarı Aylık Listeleme Servisi 
        ----------------------
        Sıfır bakiye düzeltme tutarı ve bileşenlerine ait aylık tutarlara ilişkin veri seti.Bu veriler uzlaştırmaya esas olarak yayınlanmaktadır. Yük Alma Talimatı:YAL, Yük Atma Talimatı: YAT, Yerine Getirilmeyen Yük Alma Talimat Tutarı: YGYALT, Yerine Getirilmeyen Yük Atma Talimat Tutarı: YGYALT, GDDK: Geçmişe Dönük Düzeltme Kalemi, KÜPST: Kesinleşmiş Üretim Planı Sapma Tutarı.
        ----------------------
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "zero_balance", function)

        check = self.master.control_time_between(url, startDate, endDate)

        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result
