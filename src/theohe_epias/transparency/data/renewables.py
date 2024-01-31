import requests
import pandas as pd

from theohe_epias.transparency.utils.get_time import get_today, get_year, get_yesterday, get_tomorrow, get_this_month, get_current_settlement_fday, get_current_settlement_lday, get_last_year
from theohe_epias.transparency.utils.time_format import tuple_to_datetime

class Renewables():
    def __init__(self):
        self.information = dict()
        self.information["data"] = dict({
#"generation_forecast": {"list":"renewables/data/generation-forecast","export":"renewables/export/generation-forecast"},
#"imbalance_cost": {"list":"renewables/data/imbalance-cost","export":"renewables/export/imbalance-cost"},
#"imbalance_quantity": {"list":"renewables/data/imbalance-quantity","export":"renewables/export/imbalance-quantity"},
"licensed_generation_cost": {"list":"renewables/data/licensed-generation-cost","export":"renewables/export/licensed-generation-cost"},
"licensed_powerplant_list": {"list":"renewables/data/licensed-powerplant-list"},
"licensed_realtime_generation": {"list":"renewables/data/licensed-realtime-generation","export":"renewables/export/licensed-realtime-generation"},
"new_installed_capacity": {"list":"renewables/data/new-installed-capacity","export":"renewables/export/new-installed-capacity"},
"old_installed_capacity": {"list":"renewables/data/old-installed-capacity","export":"renewables/export/old-installed-capacity"},
#"portfolio_income": {"list":"renewables/data/portfolio-income","export":"renewables/export/portfolio-income"},
"renewable_sm_licensed_injection_quantity": {"list":"renewables/data/renewable-sm-licensed-injection-quantity","export":"renewables/export/renewable-sm-licensed-injection-quantity"},
"renewables_participant": {"list":"renewables/data/renewables-participant","export":"renewables/export/renewables-participant"},
"renewables_support_mechanism_income": {"list":"renewables/data/renewables-support-mechanism-income","export":"renewables/export/renewables-support-mechanism-income"},
"res_generation_and_forecast": {"list":"renewables/data/res-generation-and-forecast","export":"renewables/export/res-generation-and-forecast"},
#"spot_order": {"list":"renewables/data/spot-order","export":"renewables/export/spot-order"},
"total_cost": {"list":"renewables/data/total-cost","export":"renewables/export/total-cost"},
"unit_cost": {"list":"renewables/data/unit-cost","export":"renewables/export/unit-cost"},
"unlicensed_generation_amount": {"list":"renewables/data/unlicensed-generation-amount","export":"renewables/export/unlicensed-generation-amount"},
"unlicensed_generation_cost": {"list":"renewables/data/unlicensed-generation-cost","export":"renewables/export/unlicensed-generation-cost"},

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
            if url in ["https://seffaflik.epias.com.tr/electricity-service/v1/consumption/data/consumer-sector-list",
"https://seffaflik.epias.com.tr/electricity-service/v1/main/province-list",
"https://seffaflik.epias.com.tr/electricity-service/v1/consumption/data/distribution-region",
"https://seffaflik.epias.com.tr/electricity-service/v1/consumption/data/multiple-factor-meter-reading-type",
"https://seffaflik.epias.com.tr/electricity-service/v1/consumption/data/get-distribution-companies",

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

    # def generation_forecast(self, 
    #                     startDate = get_today(),
    #                     endDate = get_today(),
    #                     function = "export"):
    #     """
    #     Üretim Tahmini Data Listeleme Servisi 
    #     ----------------------
    #     YEKDEM kapsamındaki santrallerin, Milli Yük Tevzi Merkezi’ne bildirdikleri tahmini üretimleridir.29 Nisan 2016 tarihli ve 29698 sayılı Yenilenebilir Enerji Kaynaklarının Belgelendirilmesi ve Desteklenmesine İlişkin Yönetmelikte Değişiklik Yapılmasına İlişkin yönetmeliğin, Resmi Gazete'de yayımlanmasını takiben Üretim Tahmini raporunun en son 30 Nisan 2016 tarihli verisi görüntülenebilecektir.' Bilgisi görüntülenecektir. Kullanıcı bu bilgilendirmeyi kapatmadan ekranda işlem yapamaz.
    #     Güncel değil!
    #     ----------------------
    #     startDate = (2023,1,1) default: today
    #     endDate = (2023,1,1) default: today
    #     function = list veya export
    #     """

    #     url = self._get_url("generation_forecast", function)

    #     check = self._control_and_format_time_between(url, startDate, endDate)
    #     if check == False:
    #         return
    #     else:
    #         startDate, endDate = check

    #     data = dict(startDate = startDate,
    #                 endDate = endDate)
    #     self.final_result = self._request_data(url, data, function)
    #     return self.final_result
    # def imbalance_cost(self, 
    #                     startDate = get_today(),
    #                     endDate = get_today(),
    #                     function = "export"):
    #     """
    #     Dengesizlik Maliyeti Listeleme Servisi 
    #     ----------------------
    #     YEKDEM kapsamındaki portföyün uzlaştırmaya esas veriş değerine göre oluşturduğu dengesizlikdir.29 Nisan 2016 tarihli ve 29698 sayılı Yenilenebilir Enerji Kaynaklarının Belgelendirilmesi ve Desteklenmesine İlişkin Yönetmelikte Değişiklik Yapılmasına İlişkin yönetmeliğin, Resmi Gazete'de yayımlanmasını takiben Üretim Tahmini raporunun en son 30 Nisan 2016 tarihli verisi görüntülenebilecektir.
    #     Güncel Değil!
    #     ----------------------
    #     startDate = (2023,1,1) default: today
    #     endDate = (2023,1,1) default: today
    #     function = list veya export
    #     """

    #     url = self._get_url("imbalance_cost", function)

    #     check = self._control_and_format_time_between(url, startDate, endDate)
    #     if check == False:
    #         return
    #     else:
    #         startDate, endDate = check

    #     data = dict(startDate = startDate,
    #                 endDate = endDate)
    #     self.final_result = self._request_data(url, data, function)
    #     return self.final_result
    # def imbalance_quantity(self, 
    #                     startDate = get_today(),
    #                     endDate = get_today(),
    #                     function = "export"):
    #     """
    #     Dengesizlik Miktarı Listeleme Servisi 
    #     ----------------------
    #     YEKDEM kapsamındaki portföyün uzlaştırmaya esas veriş değerine göre oluşturduğu dengesizlik miktarıdır.29 Nisan 2016 tarihli ve 29698 sayılı Yenilenebilir Enerji Kaynaklarının Belgelendirilmesi ve Desteklenmesine İlişkin Yönetmelikte Değişiklik Yapılmasına İlişkin yönetmeliğin, Resmi Gazete'de yayımlanmasını takiben Üretim Tahmini raporunun en son 30 Nisan 2016 tarihli verisi görüntülenebilecektir.
    #     ----------------------
    #     startDate = (2023,1,1) default: today
    #     endDate = (2023,1,1) default: today
    #     function = list veya export
    #     """

    #     url = self._get_url("imbalance_quantity", function)

    #     check = self._control_and_format_time_between(url, startDate, endDate)
    #     if check == False:
    #         return
    #     else:
    #         startDate, endDate = check

    #     data = dict(startDate = startDate,
    #                 endDate = endDate)
    #     self.final_result = self._request_data(url, data, function)
    #     return self.final_result
    def licensed_generation_cost(self, 
                        startDate = get_current_settlement_fday(),
                        endDate = get_current_settlement_lday(),
                        function = "export"):
        """
        YEK Bedeli (YEKBED) Listeleme Servisi 
        ----------------------
        İlgili fatura dönemi için YEKDEM kapsamındaki lisanssız üretim santrallerine sahip katılımcılara ödenecek YEK bedelini (TL) ifade etmektedir. https://www.epias.com.tr/wp-content/uploads/2023/10/z27csrjmDz4qqJ6b9mj2.jpg https://www.epias.com.tr/wp-content/uploads/2023/10/DPgcwzhsEjfRWWcEzsKx.png
        ----------------------
        startDate = (2023,1,1) default: last settlement
        endDate = (2023,1,1) default: last settlement
        function = list veya export
        """

        url = self._get_url("licensed_generation_cost", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result


    def licensed_powerplant_list(self, 
                                date = get_this_month(),
                        function = "list"):
        """
        Lisanslı Santral Listeleme Servisi 
        ----------------------
        Lisanslı Santral Listeleme Servisi
        ----------------------
        date = (2023,1,1) default: today
        function = list
        """

        url = self._get_url("licensed_powerplant_list", function)

        date = self._control_and_format_time(url, date)
        if date == False:
            return

        data = dict(period = date)
        self.final_result = self._request_data(url, data, function)
        return self.final_result


    def licensed_realtime_generation(self, 
                        powerPlantId = None,
                        startDate = get_today(),
                        endDate = get_today(),
                        function = "export"):
        """
        Gerçek Zamanlı Üretim Dışa Aktarım Servisi 
        ----------------------
        Lisanslı YEKDEM santrallerine ait elektrik üretiminin kaynak bazında saatlik gösterimine ilişkin veri seti.
        ----------------------
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self._get_url("licensed_realtime_generation", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(
            powerPlantId = powerPlantId,
            startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result


    def new_installed_capacity(self, 
                        date = get_today(),
                        function = "export"):
        """
        Kurulu Güç YEKDEM Son Tarih Sonrası Veri Listeleme Servisi 
        ----------------------
        YEKDEM kapsamındaki üretim tesislerinin kurulu güç miktarıdır. Lisanslı kurulu güç bilgileri EPİAŞ'a kayıtlı santraller olup, lisanssız kurulu güç bilgisi dağıtım şirketlerinden temin edilmektedir.YEKDEM kapsamındaki üretim tesislerinin kurulu güç miktarıdır.
        ----------------------
        date = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self._get_url("new_installed_capacity", function)

        date = self._control_and_format_time(url, date)
        if date == False:
            return

        data = dict(period = date)
        self.final_result = self._request_data(url, data, function)
        return self.final_result



    def old_installed_capacity(self, 
                        date = get_today(),
                        function = "export"):
        """
        Kurulu Güç YEKDEM Son Tarih ve Öncesi Veri Listeleme Servisi 
        ----------------------
        YEKDEM kapsamındaki üretim tesislerinin kurulu güç miktarıdır. Lisanslı kurulu güç bilgileri EPİAŞ'a kayıtlı santraller olup, lisanssız kurulu güç bilgisi dağıtım şirketlerinden temin edilmektedir.YEKDEM kapsamındaki üretim tesislerinin kurulu güç miktarıdır.
        ----------------------
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self._get_url("old_installed_capacity", function)

        date = self._control_and_format_time(url, date)
        if date == False:
            return

        data = dict(period = date)
        self.final_result = self._request_data(url, data, function)
        return self.final_result


    # def portfolio_income(self, 
    #                     startDate = get_today(),
    #                     endDate = get_today(),
    #                     function = "export"):
    #     """
    #     Yekdem Portföy Geliri Listeleme Servisi 
    #     ----------------------
    #     YEKDEM kapsamındaki portföyün saatlik toplam geliridir.29 Nisan 2016 tarihli ve 29698 sayılı Yenilenebilir Enerji Kaynaklarının Belgelendirilmesi ve Desteklenmesine İlişkin Yönetmelikte Değişiklik Yapılmasına İlişkin yönetmeliğin, Resmi Gazete'de yayımlanmasını takiben Üretim Tahmini raporunun en son 30 Nisan 2016 tarihli verisi görüntülenebilecektir.
    #     ----------------------
    #     startDate = (2023,1,1) default: today
    #     endDate = (2023,1,1) default: today
    #     function = list veya export
    #     """

    #     url = self._get_url("portfolio_income", function)

    #     check = self._control_and_format_time_between(url, startDate, endDate)
    #     if check == False:
    #         return
    #     else:
    #         startDate, endDate = check

    #     data = dict(startDate = startDate,
    #                 endDate = endDate)
    #     self.final_result = self._request_data(url, data, function)
    #     return self.final_result
    def renewable_sm_licensed_injection_quantity(self, 
                        startDate = get_current_settlement_fday(),
                        endDate = get_current_settlement_lday(),
                        function = "export"):
        """
        Uzlaştırma Esas Veriş Miktarı (UEVM) Listeleme Servisi 
        ----------------------
        Elektrik üretiminin kaynak bazında saatlik gösterimidir.
        ----------------------
        startDate = (2023,1,1) default: last settlement
        endDate = (2023,1,1) default: last settlement
        function = list veya export
        """

        url = self._get_url("renewable_sm_licensed_injection_quantity", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result

        
    def renewables_participant(self, 
                        date = get_year(),
                        function = "export"):
        """
        YEKDEM Katılımcı Listesi Listeleme Servisi 
        ----------------------
        İlgili yıl içerisinde Yenilenebilir Enerji Destekleme Mekanizmasına dahil olan lisanslı üretim santraline sahip tüzel kişilerin listesidir. 2020 yılından itibaren “Önceki Yıl gerçekleştirilen Üretim (MWh)” yayınlanmamaktadır
        ----------------------
        startDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self._get_url("renewables_participant", function)

        if date not in [2016,2017,2018,2019,2020,2021,2022,2023,2024,2025,2026,2027,2028]:
            return

        data = dict(year = date)
        self.final_result = self._request_data(url, data, function)
        return self.final_result


    def renewables_support_mechanism_income(self, 
                        startDate = get_current_settlement_fday(),
                        endDate = get_current_settlement_lday(),
                        function = "export"):
        """
        YEK Geliri (YG) Listeleme Servisi 
        ----------------------
        YEKDEM gelirine ilişkin veri setidir.
        ----------------------
        startDate = (2023,1,1) default: last settlement
        endDate = (2023,1,1) default: last settlement
        function = list veya export
        """

        url = self._get_url("renewables_support_mechanism_income", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result


    def res_generation_and_forecast(self, 
                        startDate = get_tomorrow(),
                        endDate = get_tomorrow(),
                        function = "export"):
        """
        RES Üretim ve Tahmin Listeleme Servisi 
        ----------------------
        Türkiye geneli izlenebilen RES’lerin toplam güç üretimi ve tahiminidir.Veriler rüzgar gücü izleme ve tahmin merkezinden temin edilmektedir. Veriler 10 dk arayla güncellenmektedir. Q5, Q25,Q75,Q95 tahmin aralıklarını ifade etmektedir. Band tahmin aralıkları minimum ve maksimum risk senaryolarına göre oluşturulmuştur.Türkiye geneli izlenebilen RES’lerin toplam güç üretimi ve tahiminidir.
        ----------------------
        startDate = (2023,1,1) default: tomorrow
        endDate = (2023,1,1) default: tomorrow
        function = list veya export
        """

        url = self._get_url("res_generation_and_forecast", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result
        
    # def spot_order(self, 
    #                     startDate = get_today(),
    #                     endDate = get_today(),
    #                     function = "export"):
    #     """
    #     Spot Teklifi Listeleme Servisi 
    #     ----------------------
    #     Milli Yük Tevzi Merkezi’nin spot piyasaya sunduğu YEKDEM portföyü teklif miktarıdır.29 Nisan 2016 tarihli ve 29698 sayılı Yenilenebilir Enerji Kaynaklarının Belgelendirilmesi ve Desteklenmesine İlişkin Yönetmelikte Değişiklik Yapılmasına İlişkin yönetmeliğin, Resmi Gazete'de yayımlanmasını takiben Spot Teklifleri raporunun en son 30 Nisan 2016 tarihli verisi görüntülenebilecektir.' Bilgisi görüntülenecektir. Kullanıcı bu bilgilendirmeyi kapatmadan ekranda işlem yapamaz.
    #     ----------------------
    #     startDate = (2023,1,1) default: today
    #     endDate = (2023,1,1) default: today
    #     function = list veya export
    #     """

    #     url = self._get_url("spot_order", function)

    #     check = self._control_and_format_time_between(url, startDate, endDate)
    #     if check == False:
    #         return
    #     else:
    #         startDate, endDate = check

    #     data = dict(startDate = startDate,
    #                 endDate = endDate)
    #     self.final_result = self._request_data(url, data, function)
    #     return self.final_result

    def total_cost(self, 
                        startDate = get_current_settlement_fday(),
                        endDate = get_current_settlement_lday(),
                        function = "export"):
        """
        Toplam Gider (YEKTOB) Listeleme Servisi 
        ----------------------
        İlgili fatura dönemi için YEKDEM kapsamındaki hem lisanslı hem de lisanssız üretim santraline sahip katılımcılara ödenecek toplam YEK bedelini (TL) ifade eder.
        ----------------------
        startDate = (2023,1,1) default: last settlement
        endDate = (2023,1,1) default: last settlement
        function = list veya export
        """

        url = self._get_url("total_cost", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result


    def unit_cost(self, 
                        startDate = get_last_year(),
                        endDate = get_current_settlement_lday(),
                        function = "export"):
        """
        Birim Maliyeti Listeleme Servisi 
        ----------------------
        Tedarik edilen birim enerji miktarı başına, hesaplanan YEKDEM maliyetidir. YEKDEM birim maliyeti ilgili aylar için versiyonlu olarak yayımlanmaktadır. Bir fatura döneminde, YEKDEM gelirinin YEK toplam bedelinden fazla olması durumunda, Yenilenebilir Enerji Kaynaklarının Belgelendirilmesi ve Desteklenmesine İlişkin Yönetmenliğin 13üncü maddesinin dördüncü fıkrası uyarınca hesaplama yapılmaktadır.Bir fatura döneminde YEKDEM gelirinin YEK toplam bedelinden fazla olması durumunda, Yenilenebilir Enerji Kaynaklarının Belgelendirilmesi ve Desteklenmesine İlişkin Yönetmeliğin 13 üncü maddesinin dördüncü fıkrası uyarınca hesaplama yapılmakta olup, Görevli Tedarik Şirketlerinin K1 kapsamındaki satışları hariç tüm satışlar için tedarikçilere uygulanan birim fiyat 0 TL/MWh olmaktadır.
        ----------------------
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self._get_url("unit_cost", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result


    def unlicensed_generation_amount(self, 
                        startDate = get_current_settlement_fday(),
                        endDate = get_current_settlement_lday(),
                        function = "export"):
        """
        Lisanssız Üretim Miktarı Listeleme Servisi 
        ----------------------
        YEKDEM kapsamındaki lisanssız santrallerin kaynak bazında saatlik olarak uzlaştırmaya esas lisanssız veriş değerleridir.YEKDEM kapsamındaki lisanssız santraller
        ----------------------
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self._get_url("unlicensed_generation_amount", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result


    def unlicensed_generation_cost(self, 
                        startDate = get_current_settlement_fday(),
                        endDate = get_current_settlement_lday(),
                        function = "export"):
        """
        Lisanssız Üretim Bedeli Listeleme Servisi 
        ----------------------
        İlgili fatura dönemi için YEKDEM kapsamındaki lisanssız üretim santrallerine sahip katılımcılara ödenecek YEK bedelini (TL) ifade etmektedir.
        ----------------------
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self._get_url("unlicensed_generation_cost", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result
