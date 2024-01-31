import requests
import pandas as pd

from theohe_epias.transparency.utils.get_time import get_today, get_year, get_yesterday, get_tomorrow, get_this_month, get_current_settlement_fday, get_current_settlement_lday
from theohe_epias.transparency.utils.time_format import tuple_to_datetime

class Transmission():
    def __init__(self):
        self.information = dict()
        self.information["data"] = dict({

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

        self.information["details"] = dict({
        })

        self.information["rename_columns"] = dict(
            PTF="PTF (TL/MWh)",
            SMF="SMF (TL/MWh)",
            )

        self.main_url = "https://seffaflik.epias.com.tr/electricity-service/v1/"
        self.region = "TR1"


    def _get_url(self, attr, function):
        if function in ["export","list"]:
            url = self.main_url + self.information["data"][attr][function]
            return url
        else:
            print("Not Defined Function.")
            return None
        

    def _request_data(self, url, data, function):
        if function == "list":
            if url in ["https://seffaflik.epias.com.tr/electricity-service/v1/transmission/data/capacity-demand-direction",
"https://seffaflik.epias.com.tr/electricity-service/v1/transmission/data/line-capacities-direction",

            ]:
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

    def _control_and_format_time_between_settlement(self, url, startDate, endDate):
        lday = get_current_settlement_lday()
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

        url = self._get_url("capacity_demand", function)
        if direction not in ["TRGR","GRTR", "TRBG", "BGTR"]:
            print("direction is not correct.")
            return 

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(direction = direction, 
                    startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result

    def capacity_demand_direction(self, 
                        function = "list"):
        """
        Kapasite talepleri yön servisleri  
        ----------------------
        Kapasite talepleri yön servisleri
        ----------------------
        function = list veya export
        """

        url = self._get_url("capacity_demand_direction", function)
        data = dict()
        self.final_result = self._request_data(url, data, function)
        return self.final_result


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

        url = self._get_url("congestion_cost", function)

        if orderType not in ["UP_REGULATION", "DOWN_REGULATION", "BOTH_REGULATIONS"]:
            print("select order type: UP_REGULATION, DOWN_REGULATION or BOTH_REGULATIONS")
            return 
        if priceType not in ["MCP", "SMP"]:
            print("select price type: MCP or SMP")
            return 


        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(
            orderType = orderType,
            priceType = priceType,
            startDate = startDate,
                    endDate = endDate,
                    region = self.region)
        self.final_result = self._request_data(url, data, function)
        return self.final_result



    def entso_w_organization(self, 
                        organizationId = None,
                        date = get_current_settlement_fday(),
                        function = "export"):
        """
        ENTSO-E (W) Kodları Listeleme Servisi 
        ----------------------
        Avrupa Elektrik İletim Sistemi İşletmecileri Ağı’nın piyasadaki Santral ve UEVÇB’lere, Avrupa standartlarına uygun formatta tanımladığı Enerji Tanımlama Kodu’dur.
        ----------------------
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self._get_url("entso_w_organization", function)

        date = self._control_and_format_time(url, date)
        if date == False:
            return

        data = dict(organizationId = organizationId,
                    period = date)
        self.final_result = self._request_data(url, data, function)
        return self.final_result

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
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self._get_url("entso_w_uevcb", function)

        date = self._control_and_format_time(url, date)
        if date == False:
            return

        data = dict(uevcbName = uevcbName,
    provinceId = provinceId,
    period = date)
        self.final_result = self._request_data(url, data, function)
        return self.final_result


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

        url = self._get_url("international_line_events", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result


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

        url = self._get_url("iskk_list", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result

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

        url = self._get_url("line_capacities", function)

        if direction not in ["TRGR","GRTR", "TRBG", "BGTR"]:
            print("direction is not correct.")
            return 

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(direction = direction, 
                    startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result


    def line_capacities_direction(self, 
                        function = "list"):
        """
        Hat kapasiteleri yön listeleme servisi 
        ----------------------
        Hat kapasiteleri yön listeleme servisi
        ----------------------
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self._get_url("line_capacities_direction", function)
        data = dict()
        self.final_result = self._request_data(url, data, function)
        return self.final_result

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

        url = self._get_url("nominal_capacity", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result


    def organization_list(self, 
                        organizationId = None,
                        date = get_current_settlement_fday(),
                        function = "export"):
        """
        ENTSO-E (X) Kodları Listeleme Servisi 
        ----------------------
        Avrupa Elektrik İletim Sistemi İşletmecileri Ağı’nın piyasadaki organizasyonlara, Avrupa standartlarına uygun formatta tanımladığı Enerji Tanımlama Kodu’dur.
        ----------------------
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self._get_url("organization_list", function)

        date = self._control_and_format_time(url, date)
        if date == False:
            return

        data = dict(organizationId = organizationId,
                    period = date)
        self.final_result = self._request_data(url, data, function)
        return self.final_result


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

        url = self._get_url("tcat_pre_month_forecast", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result

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

        url = self._get_url("tcat_pre_year_forecast", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result

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

        url = self._get_url("zero_balance", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result
