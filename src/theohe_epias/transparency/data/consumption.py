import requests
import pandas as pd

from theohe_epias.transparency.utils.get_time import get_today, get_year, get_yesterday, get_tomorrow, get_current_settlement_fday, get_current_settlement_lday
from theohe_epias.transparency.utils.time_format import tuple_to_datetime

class Consumption():
    def __init__(self):
        self.information = dict()
        self.information["data"] = dict({
"consumer_quantity": {"list":"consumption/data/consumer-quantity","export":"consumption/export/consumer-quantity"},
"consumer_sector_list": {"list":"consumption/data/consumer-sector-list"},
"consumption_quantity": {"list":"consumption/data/consumption-quantity","export":"consumption/export/consumption-quantity"},
"demand_forecast": {"list":"consumption/data/demand-forecast","export":"consumption/export/demand-forecast-export"},
"distribution_region": {"list":"consumption/data/distribution-region"},
"district_list": {"list":"main/district-list"},

"eligible_consumer_count": {"list":"consumption/data/eligible-consumer-count","export":"consumption/export/eligible-consumer-count"},
"eligible_consumer_quantity": {"list":"consumption/data/eligible-consumer-quantity","export":"consumption/export/eligible-consumer-quantity"},
"get_distribution_companies": {"list":"consumption/data/get-distribution-companies"},
"load_estimation_plan": {"list":"consumption/data/load-estimation-plan","export":"consumption/export/load-estimation-plan"},
"main_tariff_group_list": {"list":"consumption/data/main-tariff-group-list"},

"meter_count": {"list":"consumption/data/meter-count","export":"consumption/export/meter-count-export"},
"monthly_index": {"list":"consumption/data/monthly-index","export":"consumption/export/monthly-index"},
"multiple_factor": {"list":"consumption/data/multiple-factor","export":"consumption/export/multiple-factor"},
"multiple_factor_distribution": {"list":"consumption/data/multiple-factor-distribution"},
"multiple_factor_meter_reading_type": {"list":"consumption/data/multiple-factor-meter-reading-type"},
"multiple_factor_profile_group": {"list":"consumption/data/multiple-factor-profile-group"},
"percentage_consumption_info": {"list":"consumption/data/percentage-consumption-info","export":"consumption/export/percentage-consumption-info"},
"planned_power_outage_info": {"list":"consumption/data/planned-power-outage-info","export":"consumption/export/planned-power-outage-info"},
"profile_subscription_group_list": {"list":"consumption/data/profile-subscription-group-list"},
"province_list": {"list":"main/province-list"},
"realtime_consumption": {"list":"consumption/data/realtime-consumption","export":"consumption/export/realtime-consumption"},
"st_adedi": {"list":"consumption/data/st-adedi","export":"consumption/export/st-adedi"},
"st_uecm": {"list":"consumption/data/st-uecm","export":"consumption/export/st-uecm"},
"uecm": {"list":"consumption/data/uecm","export":"consumption/export/uecm-export"},
"unplanned_power_outage_info": {"list":"consumption/data/unplanned-power-outage-info","export":"consumption/export/unplanned-power-outage-info"},
"withdrawal_quantity_under_supply_liability": {"list":"consumption/data/withdrawal-quantity-under-supply-liability","export":"consumption/export/withdrawal-quantity-under-supply-liability"},

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
"https://seffaflik.epias.com.tr/electricity-service/v1/consumption/data/main-tariff-group-list",
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

    def consumer_quantity(self, 
                        provinceId = None,
                        profileGroupId = None,
                        date  =get_current_settlement_fday(),
                        function = "export"):
        """
        Tüketici Sayısı Listeleme Servisi 
        ----------------------
        İl bazında tüketici sayılarının tüketici türüne ve tüketici profil gruplarına göre ayrımı aylık olarak gösterilmektedir.
        ----------------------
        provinceId = int default: None
        profileGroupId = int default: None
        period = (2023,1,1) default: last settlement period
        function = list veya export
        """

        url = self._get_url("consumer_quantity", function)

        date = self._control_and_format_time(url, date)
        if date == False:
            return

        data = dict(provinceId=provinceId,
                        profileGroupId=profileGroupId,
                        period = date)
        try:
            self.final_result = self._request_data(url, data, function)
            return self.final_result
        except:
            print("There is no data for given period or not valid IDs, check these.")
            return self.consumer_sector_list(), self.province_list()


    def consumption_quantity(self, 
                        provinceId = None,
                        profileGroupId = None,
                        date  =get_current_settlement_fday(),
                        function = "export"):
        """
        Tüketim Miktarları Listeleme Servisi 
        ----------------------
        İl bazında tüketici miktarlarının tüketici türüne ve tüketici profil gruplarına göre ayrımı aylık olarak gösterilmektedir.
        ----------------------
        provinceId = int default: None
        profileGroupId = int default: None
        period = (2023,1,1) default: last settlement period
        function = list veya export
        """

        url = self._get_url("consumption_quantity", function)

        date = self._control_and_format_time(url, date)
        if date == False:
            return

        data = dict(provinceId=provinceId,
                        profileGroupId=profileGroupId,
                        period = date)
        try:
            self.final_result = self._request_data(url, data, function)
            return self.final_result
        except:
            print("There is no data for given period or not valid IDs, check these.")
            return self.consumer_sector_list(), self.province_list()


    def demand_forecast(self, 
                        distrubutionOrganization = None,
                        function = "export"):
        """
        Talep Tahmini Listeleme Servisi 
        ----------------------
        İlgili dağıtım bölgesinde dağıtım şirketine ait 2018-2027 arası tüketicilerin yıllık brüt tahmin değerleridir. Veriler TEAİŞ Raporlarından temin edilmektedir.
        ----------------------
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self._get_url("demand_forecast", function)

        data = dict(distrubutionOrganization = distrubutionOrganization)
        try:
            self.final_result = self._request_data(url, data, function)
            return self.final_result
        except:
            print("Not valid IDs, check these.")
            return self.distribution_region()["items"]
            

    def eligible_consumer_count(self, 
                        provinceId = None,
                        districtName = None,
                        profileGroupName = None,
                        date = get_current_settlement_fday(),
                        function = "export"):
        """
        İl, İlçe ST Adedi Listeleme Servisi 
        ----------------------
        Sayaç kullanım tipi serbest tüketici olan sayaçların ilçe ve profil abone grubu bazındaki sayısıdır. Paylaşılan ilçe bilgilerinde geçmiş ilçe isimleri yer alabilmektedir. Analiz yapılırken bu hususa dikkat edilmesi önemle rica olunur.
        ----------------------
        provinceId = int default: None,
        districtName = str default: None,
        profileGroupName = str default: None,
        period = (2023,1,1) default: last settlement
        function = list veya export
        """

        url = self._get_url("eligible_consumer_count", function)

        date = self._control_and_format_time(url, date)
        if date == False:
            return
        data = dict(districtName = districtName,
                        provinceId = provinceId,
                        profileGroupName = profileGroupName,
                        period = date)
        try:
            self.final_result = self._request_data(url, data, function)
            return self.final_result
        except:
            print("There is no data for given period or not valid IDs, check these.")
            print("profileGroupName should be in upper case. (Aydınlatma => AYDINLATMA)")
            return self.consumer_sector_list(), self.province_list()


    def eligible_consumer_quantity(self, 
                        startDate = get_current_settlement_fday(),
                        endDate = get_current_settlement_lday(),
                        function = "export"):
        """
        Serbest Tüketici Tüketim Miktarı Listeleme Servisi 
        ----------------------
        Sayaç kullanım tipi serbest tüketici olan sayaçların uzlaştırmaya esas çekiş miktarı toplamıdır.
        ----------------------
        startDate = (2023,1,1) default: last settlement
        endDate = (2023,1,1) default: last settlement
        function = list veya export
        """

        url = self._get_url("eligible_consumer_quantity", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result

    def st_adedi(self, 
                        startDate = get_current_settlement_fday(),
                        endDate = get_current_settlement_lday(),
                        function = "export"):
        """
        Serbest Tüketici Adedi Listeleme Servisi 
        ----------------------
        Sayaç kullanım tipi serbest tüketici olan sayaçların sayısıdır.
        ----------------------
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self._get_url("st_adedi", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result


    def load_estimation_plan(self, 
                        startDate = get_today(),
                        endDate = get_today(),
                        function = "export"):
        """
        Yük Tahmin Planı Listeleme Servisi 
        ----------------------
        Bir sonraki gün için yapılan saatlik talep miktarıdır.
        ----------------------
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self._get_url("load_estimation_plan", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result


    def meter_count(self, 
                        function = "export"):
        """
        Sayaç Adedi Listeleme Servisi 
        ----------------------
        İçerisinde bulunana dönemden bir sonraki dönem için açıklanan sayaç adedi verisidir.
        ----------------------
        function = list veya export
        """
        url = self._get_url("meter_count", function)
        data = dict()
        self.final_result = self._request_data(url, data, function)
        return self.final_result


    # def monthly_index(self, 
    #                     startDate = get_today(),
    #                     endDate = get_today(),
    #                     function = "export"):
    #     """
    #     Aylık Endeks Listeleme Servisi 
    #     ----------------------
    #     Piyasa Takas Fiyatı (PTF), Negatif Sistem Dengesizlik Fiyatı, YEKDEM Birim Fiyat, Ulusal Tarife Birim Fiyatları ve Piyasa Yönetim Sistemine kayıtlı tüketicilere ait uzlaştırma dönemi bazındaki çekiş miktarları kullanılarak hesaplanan değere ilişkin veri seti. Referans endeks 100 olarak alınacaktır.
    #     ----------------------
    #     startDate = (2023,1,1) default: today
    #     endDate = (2023,1,1) default: today
    #     function = list veya export
    #     """

    #     url = self._get_url("monthly_index", function)

    #     check = self._control_and_format_time_between(url, startDate, endDate)
    #     if check == False:
    #         return
    #     else:
    #         startDate, endDate = check

    #     data = dict(startDate = startDate,
    #                 endDate = endDate)
    #     self.final_result = self._request_data(url, data, function)
    #     return self.final_result

    def multiple_factor_distribution(self, 
                        date = get_current_settlement_fday(),
                        function = "list"):
        """
        Dağıtım Firmaları Listeleme Servisi 
        ----------------------
        Dağıtım Firmaları Listeleme Servisi
        ----------------------
        date = (2023,1,1)
        function = list
        """

        url = self._get_url("multiple_factor_distribution", function)

        date = self._control_and_format_time(url, date)
        if date == False:
            return

        data = dict(period = date)
        self.final_result = self._request_data(url, data, function)
        return self.final_result


    def multiple_factor_meter_reading_type(self, 
                        function = "list"):
        """
        Sayaç Okuma Tipi Listeleme Servisi 
        ----------------------
        Sayaç Okuma Tipi Listeleme Servisi
        ----------------------
        function = list
        """

        url = self._get_url("multiple_factor_meter_reading_type", function)
        data = dict()
        self.final_result = self._request_data(url, data, function)
        return self.final_result

    def multiple_factor_profile_group(self, 
                        distributionId = None,
                        date = get_current_settlement_fday(),
                        function = "list"):
        """
        Profil Abone Grubu Listeleme Servisi 
        ----------------------
        Profil Abone Grubu Listeleme Servisi
        ----------------------
        distributionId = int default: None
        date = (2023,1,1)
        function = list
        """

        url = self._get_url("multiple_factor_profile_group", function)


        disco_list = self.multiple_factor_distribution(date)
        discos = [k["id"] for k in disco_list]
        if distributionId not in discos:
            print("Select from distribution ids.")
            return disco_list

        date = self._control_and_format_time(url, date)
        if date == False:
            return

        data = dict(distributionId = distributionId, period = date)
        self.final_result = self._request_data(url, data, function)
        return self.final_result

    def multiple_factor(self, 
                        distributionId = None,
                        meterReadingType = None,
                        subscriberProfileGroup = None,
                        date = get_current_settlement_fday(),
                        function = "export"):
        """
        Çarpan Değeri Listeleme Servisi 
        ----------------------
        Uzlaştırma dönemi bazında ölçüm yapılamayan sayaçlar için uygulanan profilleme işleminde kullanılan değerlere ilişkin veri seti.
        ----------------------
        distributionId = int
        subscriberProfileGroup = int
        meterReadingType = 1,3 default:1,
        date = (2023,1,1) default: last settlement
        function = list veya export
        """

        url = self._get_url("multiple_factor", function)
        date_new = self._control_and_format_time(url, date)
        if date_new == False:
            return

        disco_list = self.multiple_factor_distribution(date)
        discos = [k["id"] for k in disco_list]
        if distributionId not in discos:
            print("Select from distribution ids.")
            return disco_list

        profile_list = self.multiple_factor_profile_group(distributionId,date)
        profiles = [k["id"] for k in profile_list]
        if subscriberProfileGroup not in profiles:
            print("Select from profile ids.")
            return profile_list


        data = dict(
            distributionId = distributionId,
            meterReadingType = meterReadingType,
            subscriberProfileGroup = subscriberProfileGroup,
            period = date_new)

        self.final_result = self._request_data(url, data, function)
        return self.final_result
        
        

    def percentage_consumption_info(self, 
                        provinceId = None,
                        date = get_current_settlement_fday(),
                        function = "export"):
        """
        Yüzdesel Tüketim Bilgileri Listeleme Servisi 
        ----------------------
        Fiili tüketimin il bazında ve profil abone grubu bazında yüzdesel kırılımına ilişkin veri seti.
        ----------------------
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self._get_url("percentage_consumption_info", function)

        date = self._control_and_format_time(url, date)
        if date == False:
            return

        data = dict(provinceId = provinceId, period = date)
        self.final_result = self._request_data(url, data, function)
        return self.final_result



    def planned_power_outage_info(self,
                                distributionCompanyId = None,
                                provinceId = None,
                        date = get_tomorrow(),
                        function = "export"):
        """
        Planlı Kesinti Bilgisi Listeleme Servisi 
        ----------------------
        Yapılması planlanan kesinti bilgilerinin sunulduğu ekrandır.
        ----------------------
        distributionCompanyId = int default: None
        provinceId = int default: None
        date = (2023,1,1) default: tomorrow
        function = list veya export
        """

        url = self._get_url("planned_power_outage_info", function)

        date = self._control_and_format_time(url, date)
        if date == False:
            return

        if distributionCompanyId != None:
            disco_list = self.get_distribution_companies()
            discos = [k["companyId"] for k in disco_list]
            if distributionCompanyId not in discos:
                print("Select from distribution ids.")
                return disco_list

        if provinceId != None:
            profile_list = self.province_list()
            profiles = [k["id"] for k in profile_list]
            if provinceId not in profiles:
                print("Select from province ids.")
                return profile_list



        data = dict(distributionCompanyId = distributionCompanyId,
                    provinceId = provinceId,
                        period = date)
        self.final_result = self._request_data(url, data, function)
        return self.final_result


    def unplanned_power_outage_info(self, 
    distributionCompanyId = None,
    provinceId = None,
                        date = get_yesterday(),
                        function = "export"):
        """
        Plansız Kesinti Bilgisi Listeleme Servisi 
        ----------------------
        Plansız kesintilerin sunulduğu ekrandır.
        ----------------------
        distributionCompanyId = int default: None
        provinceId = int default: None
        date = (2023,1,1) default: yesterday
        function = list veya export
        """

        url = self._get_url("unplanned_power_outage_info", function)

        date = self._control_and_format_time(url, date)
        if date == False:
            return

        if distributionCompanyId != None:
            disco_list = self.get_distribution_companies()
            discos = [k["companyId"] for k in disco_list]
            if distributionCompanyId not in discos:
                print("Select from distribution ids.")
                return disco_list

        if provinceId != None:
            profile_list = self.province_list()
            profiles = [k["id"] for k in profile_list]
            if provinceId not in profiles:
                print("Select from province ids.")
                return profile_list



        data = dict(distributionCompanyId = distributionCompanyId,
                    provinceId = provinceId,
                        period = date)
        self.final_result = self._request_data(url, data, function)
        return self.final_result




    def realtime_consumption(self, 
                        startDate = get_today(),
                        endDate = get_today(),
                        function = "export"):
        """
        Gerçek Zamanlı Tüketim Listeleme Servisi 
        ----------------------
        Anlık olarak gerçekleşen tüketim değerinin saatlik bazda gösterildiği veridir. Gerçek Zamanlı Tüketim verisi 2 saat geriden gelecek sekilde yayınlanmaktadır.
        ----------------------
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self._get_url("realtime_consumption", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result

    def st_uecm(self, 
                date = get_current_settlement_fday(),
                function = "export"):
        """
        Serbest Tüketici Uzlaştırmaya Esas Çekiş Miktarı Listeleme Servisi 
        ----------------------
        Serbest tüketici hakkını kullananların, bir uzlaştırma dönemi içinde saatlik olarak sistemden aldığı enerji miktarlarının toplam değerine ilişkin veri seti.
        ----------------------
        date = (2023,1,1) default: last settlement 
        function = list veya export
        """

        url = self._get_url("st_uecm", function)

        date = self._control_and_format_time(url, date)
        if date == False:
            return

        data = dict(period = date)
        self.final_result = self._request_data(url, data, function)
        return self.final_result


    def uecm(self, 
            startDate = get_current_settlement_fday(),
            endDate = get_current_settlement_lday(),
            function = "export"):
        """
        Uzlaştırmaya Esas Çekiş Miktarı (UEÇM) Listeleme Servisi 
        ----------------------
        Uzlaştırmaya esas çekiş birimlerinin, bir uzlaştırma dönemi içinde saatlik olarak sistemden aldığı enerji miktarlarının toplam değerine ilişkin veri seti
        ----------------------
        startDate = (2023,1,1) default: last settlement
        endDate = (2023,1,1) default: last settlement
        function = list veya export
        """

        url = self._get_url("uecm", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result


    def withdrawal_quantity_under_supply_liability(self, 
            startDate = get_year(),
            endDate = get_current_settlement_lday(),
                        function = "export"):
        """
        Tedarik Yükümlülüğü Kapsamındaki Uzlaştırmaya Esas Çekiş Miktarı (UEÇM) Listeleme Servisi 
        ----------------------
        Uzlaştırmaya esas çekiş birimlerinin, tedarik yükümlülüğü kapsamında sistemden aldığı enerji miktarlarının toplam değerine ilişkin veri seti. Bir fatura döneminde YEKDEM gelirinin YEK toplam bedelinden fazla olması durumunda, Yenilenebilir Enerji Kaynaklarının Belgelendirilmesi ve Desteklenmesine İlişkin Yönetmeliğin 13 üncü maddesinin dördüncü fıkrası uyarınca hesaplama yapılmakta olup, Görevli Tedarik Şirketlerinin K1 kapsamındaki satışları hariç tüm satışlar için tedarikçilere uygulanan birim fiyat 0 TL/MWh olmaktadır.
        ----------------------
        startDate = (2023,1,1) default: last settlement
        endDate = (2023,1,1) default: last settlement
        function = list veya export
        """

        url = self._get_url("withdrawal_quantity_under_supply_liability", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result


    def consumer_sector_list(self, 
                        function = "list"):
        """
        Profil Grubu Listeleme Servisi 
        ----------------------
        Tüketici bilgisi sayfalarının filtreleme alanları için Profil Grubu Listeleme servisidir.
        ----------------------
        function = list
        """

        url = self._get_url("consumer_sector_list", function)
        data = dict()
        self.final_result = self._request_data(url, data, function)
        return self.final_result


    def distribution_region(self, 
                        function = "list"):
        """
        Dağıtım Bölgesi Servisi 
        ----------------------
        Dağıtım Bölgesi Servisi
        ----------------------
        function = list
        """

        url = self._get_url("distribution_region", function)
        data = dict()
        self.final_result = self._request_data(url, data, function)
        return self.final_result

    def district_list(self,
                    provinceId,
                    function = "list"):
        """
        İlçe Listeleme Servisi 
        ----------------------
        Şehir bilgisine göre ilçe listelesini dönen servistir.
        ----------------------
        function = list
        """

        url = self._get_url("district_list", function)
        data = dict(provinceId=provinceId)
        self.final_result = self._request_data(url, data, function)
        return self.final_result

    def get_distribution_companies(self, 
                        function = "list"):
        """
        Dağıtım Şirketlerinin Alındığı Servis 
        ----------------------
        Dağıtım Şirketlerinin Alındığı Servis
        ----------------------
        function = list
        """

        url = self._get_url("get_distribution_companies", function)
        data = dict()
        self.final_result = self._request_data(url, data, function)
        return self.final_result

    def main_tariff_group_list(self, 
                        startDate = get_today(),
                        endDate = get_today(),
                        function = "list"):
        """
        Ana Tarife Grubu 
        ----------------------
        Ana Tarife gruplarını dönen servis.
        ----------------------
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self._get_url("main_tariff_group_list", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result



    def province_list(self, 
                        function = "list"):
        """
        Şehir Listeleme Servisi 
        ----------------------
        EPİAŞ Sisteminde kayıtlı Türkiye şehir listelemesini dönen servistir. İstanbul, Asya ve Avrupa olmak üzere ikiye ayrılmıştır.
        ----------------------
        function = list
        """

        url = self._get_url("province_list", function)
        data = dict()
        self.final_result = self._request_data(url, data, function)
        return self.final_result



    def profile_subscription_group_list(self, 
                        date = get_today(),
                        function = "list"):
        """
        Profil Abone Grubu Listeleme Servisi 
        ----------------------
        İl ilçe st adedi sayfası için profil abone grubu listesi döner
        ----------------------
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self._get_url("profile_subscription_group_list", function)

        date = self._control_and_format_time(url, date)
        if date == False:
            return

        data = dict(period = date)
        self.final_result = self._request_data(url, data, function)
        return self.final_result

