from ..utils.get_time import get_today, get_year, get_yesterday, get_tomorrow, get_current_settlement_fday, get_current_settlement_lday

class Consumption():
    information = dict()
    information["data"] = dict({
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
# "monthly_index": {"list":"consumption/data/monthly-index","export":"consumption/export/monthly-index"},

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

    information["details"] = {'consumer_quantity': ['provinceId', 'profileGroupId', 'date', 'function'],
 'consumer_sector_list': ['function'],
 'consumption_quantity': ['provinceId', 'profileGroupId', 'date', 'function'],
 'demand_forecast': ['distrubutionOrganization', 'function'],
 'distribution_region': ['function'],
 'district_list': ['provinceId', 'function'],
 'eligible_consumer_count': ['provinceId',
  'districtName',
  'profileGroupName',
  'date',
  'function'],
 'eligible_consumer_quantity': ['startDate', 'endDate', 'function'],
 'get_distribution_companies': ['function'],
 'load_estimation_plan': ['startDate', 'endDate', 'function'],
 'main_tariff_group_list': ['startDate', 'endDate', 'function'],
 'meter_count': ['function'],
 'multiple_factor': ['distributionId',
  'meterReadingType',
  'subscriberProfileGroup',
  'date',
  'function'],
 'multiple_factor_distribution': ['date', 'function'],
 'multiple_factor_meter_reading_type': ['function'],
 'multiple_factor_profile_group': ['distributionId', 'date', 'function'],
 'percentage_consumption_info': ['provinceId', 'date', 'function'],
 'planned_power_outage_info': ['distributionCompanyId',
  'provinceId',
  'date',
  'function'],
 'profile_subscription_group_list': ['date', 'function'],
 'province_list': ['function'],
 'realtime_consumption': ['startDate', 'endDate', 'function'],
 'st_adedi': ['startDate', 'endDate', 'function'],
 'st_uecm': ['date', 'function'],
 'uecm': ['startDate', 'endDate', 'function'],
 'unplanned_power_outage_info': ['distributionCompanyId',
  'provinceId',
  'date',
  'function'],
 'withdrawal_quantity_under_supply_liability': ['startDate',
  'endDate',
  'function']}

    information["rename_columns"] = dict(
        PTF="PTF (TL/MWh)",
        SMF="SMF (TL/MWh)",
        )

    
    def __init__(self, root_url, master):
        self.main_url = root_url + "electricity-service/v1/"
        self.master = master
        self.headers = {"TGT":self.master.tgt_response, "Content-Type": "application/json"}


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
        date = (2023,1,1) default: last settlement period
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "consumer_quantity", function)

        date = self.master.control_time(url, date)

        if date == False:
            return

        data = dict(provinceId=provinceId,
                        profileGroupId=profileGroupId,
                        period = date)
        try:
            self.result = self.master.request_data(url, data, function, self.headers, self.information)
            return self.result
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
        date = (2023,1,1) default: last settlement period
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "consumption_quantity", function)

        date = self.master.control_time(url, date)
        if date == False:
            return

        data = dict(provinceId=provinceId,
                        profileGroupId=profileGroupId,
                        period = date)
        try:
            self.result = self.master.request_data(url, data, function, self.headers, self.information)
            return self.result
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
        distrubutionOrganization = int default: None
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "demand_forecast", function)

        data = dict(distrubutionOrganization = distrubutionOrganization)
        try:
            self.result = self.master.request_data(url, data, function, self.headers, self.information)
            return self.result
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
        date = (2023,1,1) default: last settlement
        function = list veya export
        """
        
        url = self.master.get_url(self.main_url, self.information, "eligible_consumer_count", function)

        date = self.master.control_time(url, date)

        if date == False:
            return

        data = dict(districtName = districtName,
                        provinceId = provinceId,
                        profileGroupName = profileGroupName,
                        period = date)
        try:
            self.result = self.master.request_data(url, data, function, self.headers, self.information)
            return self.result

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


        url = self.master.get_url(self.main_url, self.information, "eligible_consumer_quantity", function)

        check = self.master.control_time_between(url, startDate, endDate)

        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result


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

        url = self.master.get_url(self.main_url, self.information, "st_adedi", function)

        check = self.master.control_time_between(url, startDate, endDate)

        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result



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

        url = self.master.get_url(self.main_url, self.information, "load_estimation_plan", function)

        check = self.master.control_time_between(url, startDate, endDate)

        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result



    def meter_count(self, 
                        function = "export"):
        """
        Sayaç Adedi Listeleme Servisi 
        ----------------------
        İçerisinde bulunana dönemden bir sonraki dönem için açıklanan sayaç adedi verisidir.
        ----------------------
        function = list veya export
        """
        url = self.master.get_url(self.main_url, self.information, "meter_count", function)

        data = dict()
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result



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

        url = self.master.get_url(self.main_url, self.information, "multiple_factor_distribution", function)

        date = self.master.control_time(url, date)

        if date == False:
            return
        data = dict(period = date)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result



    def multiple_factor_meter_reading_type(self, 
                        function = "list"):
        """
        Sayaç Okuma Tipi Listeleme Servisi 
        ----------------------
        Sayaç Okuma Tipi Listeleme Servisi
        ----------------------
        function = list
        """

        url = self.master.get_url(self.main_url, self.information, "multiple_factor_meter_reading_type", function)

        data = dict()
        self.result = self.master.request_data_get(url, data, function, self.headers, self.information)
        return self.result


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

        url = self.master.get_url(self.main_url, self.information, "multiple_factor_profile_group", function)

        date_new = self.master.control_time(url, date)

        if date_new == False:
            return

        disco_list = self.multiple_factor_distribution(date)
        discos = [k["id"] for k in disco_list]
        if distributionId not in discos:
            print("Select from distribution ids.")
            return disco_list

        data = dict(distributionId = distributionId, period = date_new)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result


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
        meterReadingType = 1,3 default:1,
        subscriberProfileGroup = int
        date = (2023,1,1) default: last settlement
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "multiple_factor", function)
        date_new = self.master.control_time(url, date)

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

        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result

        
        

    def percentage_consumption_info(self, 
                        provinceId = None,
                        date = get_current_settlement_fday(),
                        function = "export"):
        """
        Yüzdesel Tüketim Bilgileri Listeleme Servisi 
        ----------------------
        Fiili tüketimin il bazında ve profil abone grubu bazında yüzdesel kırılımına ilişkin veri seti.
        ----------------------
        provinceId = int default: None
        date = (2023,1,1) default: today
        function = list veya export
        """
        url = self.master.get_url(self.main_url, self.information, "percentage_consumption_info", function)

        date = self.master.control_time(url, date)

        if date == False:
            return

        data = dict(provinceId = provinceId, period = date)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result




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
        url = self.master.get_url(self.main_url, self.information, "planned_power_outage_info", function)

        date = self.master.control_time(url, date)

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
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result



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

        url = self.master.get_url(self.main_url, self.information, "unplanned_power_outage_info", function)

        date = self.master.control_time(url, date)

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
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result





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

        url = self.master.get_url(self.main_url, self.information, "realtime_consumption", function)

        check = self.master.control_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result


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

        url = self.master.get_url(self.main_url, self.information, "st_uecm", function)

        date = self.master.control_time(url, date)

        if date == False:
            return
        data = dict(period = date)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result



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

        url = self.master.get_url(self.main_url, self.information, "uecm", function)

        check = self.master.control_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result



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

        url = self.master.get_url(self.main_url, self.information, "withdrawal_quantity_under_supply_liability", function)

        check = self.master.control_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result



    def consumer_sector_list(self, 
                        function = "list"):
        """
        Profil Grubu Listeleme Servisi 
        ----------------------
        Tüketici bilgisi sayfalarının filtreleme alanları için Profil Grubu Listeleme servisidir.
        ----------------------
        function = list
        """

        url = self.master.get_url(self.main_url, self.information, "consumer_sector_list", function)

        data = dict()
        self.result = self.master.request_data_get(url, data, function, self.headers, self.information)
        return self.result



    def distribution_region(self, 
                        function = "list"):
        """
        Dağıtım Bölgesi Servisi 
        ----------------------
        Dağıtım Bölgesi Servisi
        ----------------------
        function = list
        """

        url = self.master.get_url(self.main_url, self.information, "distribution_region", function)
        data = dict()
        self.result = self.master.request_data_get(url, data, function, self.headers, self.information)
        return self.result


    def district_list(self,
                    provinceId,
                    function = "list"):
        """
        İlçe Listeleme Servisi 
        ----------------------
        Şehir bilgisine göre ilçe listelesini dönen servistir.
        ----------------------
        provinceId = int default: None
        function = list
        """

        url = self.master.get_url(self.main_url, self.information, "district_list", function)

        data = dict(provinceId=provinceId)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result


    def get_distribution_companies(self, 
                        function = "list"):
        """
        Dağıtım Şirketlerinin Alındığı Servis 
        ----------------------
        Dağıtım Şirketlerinin Alındığı Servis
        ----------------------
        function = list
        """

        url = self.master.get_url(self.main_url, self.information, "get_distribution_companies", function)

        data = dict()
        self.result = self.master.request_data_get(url, data, function, self.headers, self.information)
        return self.result


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

        url = self.master.get_url(self.main_url, self.information, "main_tariff_group_list", function)

        check = self.master.control_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.result = self.master.request_data_get(url, data, function, self.headers, self.information)
        return self.result




    def province_list(self, function = "list"):
        """
        Şehir Listeleme Servisi 
        ----------------------
        EPİAŞ Sisteminde kayıtlı Türkiye şehir listelemesini dönen servistir. İstanbul, Asya ve Avrupa olmak üzere ikiye ayrılmıştır.
        ----------------------
        function = list
        """

        url = self.master.get_url(self.main_url, self.information, "province_list", function)

        data = dict()
        self.result = self.master.request_data_get(url, data, function, self.headers, self.information)
        return self.result




    def profile_subscription_group_list(self, 
                        date = get_today(),
                        function = "list"):
        """
        Profil Abone Grubu Listeleme Servisi 
        ----------------------
        İl ilçe st adedi sayfası için profil abone grubu listesi döner
        ----------------------
        date = (2023,1,1) default: today
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "profile_subscription_group_list", function)

        date = self.master.control_time(url, date)

        if date == False:
            return
        data = dict(period = date)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result

