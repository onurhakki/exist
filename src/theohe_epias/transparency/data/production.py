from ..utils.get_time import get_today, get_year, get_tomorrow, get_current_settlement_fday, get_current_settlement_lday, get_last_year

class Production():
    information = dict()
    information["data"] = dict({
"aic": {"list":"generation/data/aic","export":"generation/export/aic"},
"dpp": {"list":"generation/data/dpp","export":"generation/export/dpp"},
"injection_quantity": {"list":"generation/data/injection-quantity","export":"generation/export/injection-quantity"},
"injection_quantity_powerplant_list": {"list":"generation/data/injection-quantity-powerplant-list"},
"licensed_powerplant_investment_list": {"list":"generation/data/licensed-powerplant-investment-list","export":"generation/export/licensed-powerplant-investment-list"},
"organization_list": {"list":"generation/data/organization-list"},
"powerplant_list": {"list":"generation/data/powerplant-list"},
"realtime_generation": {"list":"generation/data/realtime-generation","export":"generation/export/realtime-generation"},
"region_list": {"list":"generation/data/region-list"},
"sbfgp": {"list":"generation/data/sbfgp","export":"generation/export/sbfgp"},
"uevcb_list": {"list":"generation/data/uevcb-list"},
    })

    information["details"] = {'aic': ['uevcbId', 'organizationId', 'startDate', 'endDate', 'function'],
 'dpp': ['uevcbId', 'organizationId', 'startDate', 'endDate', 'function'],
 'injection_quantity': ['powerPlantId', 'startDate', 'endDate', 'function'],
 'injection_quantity_powerplant_list': ['function'],
 'licensed_powerplant_investment_list': ['startDate', 'endDate', 'function'],
 'organization_list': ['startDate', 'endDate', 'function'],
 'powerplant_list': ['function'],
 'realtime_generation': ['powerPlantId', 'startDate', 'endDate', 'function'],
 'region_list': ['function'],
 'sbfgp': ['uevcbId', 'organizationId', 'startDate', 'endDate', 'function'],
 'uevcb_list': ['organizationId', 'startDate', 'function']}


    information["rename_columns"] = dict(
        PTF="PTF (TL/MWh)",
        SMF="SMF (TL/MWh)",
        )

    def __init__(self, root_url, master):
        self.main_url = root_url + "electricity-service/v1/"
        self.master = master
        self.headers = {"TGT":self.master.tgt_response, "Content-Type": "application/json"}

    def aic(self,
            uevcbId = None,
            organizationId = None,
            startDate = get_today(),
            endDate = get_tomorrow(),
            function = "export"):
        """
        Emre Amade Kapasite (EAK) Listeleme Servisi 
        ----------------------
        Emre Amade Kapasite: Bir üretim biriminin sisteme sağlayabileceği aktif güç kapasitesidir.
        ----------------------
        uevcbId = int default: None
        organizationId = int default: None
        startDate = (2023,1,1) default: tomorrow
        endDate = (2023,1,1) default: tomorrow
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "aic", function)

        if organizationId == None:
            uevcbId = None
        else:
            for d in [startDate, endDate]:
                uevcbs = [k["id"] for k in self.uevcb_list(organizationId, date = d)["items"]]
                if uevcbId not in uevcbs:
                    print("UEVCB ID is not in Organization port in between given dates.")
                    print("Possible UEVCB IDs: {}".format(uevcbs))
                    return self.uevcb_list(organizationId, date = startDate)


        check = self.master.control_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(
            uevcbId = uevcbId,
            organizationId = organizationId,
            startDate = startDate,
                    endDate = endDate,
                    region = self.master.region
                    )
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result


    def dpp(self, 
            uevcbId = None,
            organizationId = None,
                        startDate = get_today(),
                        endDate = get_tomorrow(),
                        function = "export"):
        """
        Kesinleşmiş Günlük Üretim Planı (KGÜP) Listeleme Servisi 
        ----------------------
        Kesinleşmiş Gün Öncesi Üretim Programı, katılımcının bir sonraki güne ilişkin gerçekleştirmeyi öngördüğü ve sistem işletmecisine dengeleme güç piyasasının başlangıcında bildirdiği üretim değeridir.
        ----------------------
        uevcbId = int default: None
        organizationId = int default: None
        startDate = (2023,1,1) default: tomorrow
        endDate = (2023,1,1) default: tomorrow
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "dpp", function)

        if organizationId == None:
            uevcbId = None
        else:
            for d in [startDate, endDate]:
                uevcbs = [k["id"] for k in self.uevcb_list(organizationId, date = d)["items"]]
                if uevcbId not in uevcbs:
                    print("UEVCB ID is not in Organization port in between given dates.")
                    print("Possible UEVCB IDs: {}".format(uevcbs))
                    return self.uevcb_list(organizationId, date = startDate)

        check = self.master.control_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(
            uevcbId = uevcbId,
            organizationId = organizationId,
            startDate = startDate,
                    endDate = endDate,
                    region = self.master.region
                    )
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result


    def injection_quantity(self,
                    powerPlantId = None,
                        startDate = get_current_settlement_fday(),
                        endDate = get_current_settlement_lday(),
                        function = "export"):
        """
        Uzlaştırma Esas Veriş Miktarı (UEVM) Listeleme Servisi 
        ----------------------
        Uzlaştırmaya esas veriş birimlerinin, bir uzlaştırma dönemi içinde saatlik olarak sisteme verdiği elektrik miktarının toplam değeridir.
        ----------------------
        powerPlantId = int default: None
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "injection_quantity", function)

        if powerPlantId != None:
            pp_list = self.injection_quantity_powerplant_list()
            pp_ids = [k["id"] for k in pp_list["items"]]
            if powerPlantId not in pp_ids:
                print("powerPlantId is not found.")
                return pp_list

        check = self.master.control_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(
            powerplantId = powerPlantId,
            startDate = startDate,
                    endDate = endDate,
                    )
        try:
            self.result = self.master.request_data(url, data, function, self.headers, self.information)
            return self.result
        except:
            print("Not valid powerPlantId, check these.")
            return self.injection_quantity_powerplant_list()["items"]



    def licensed_powerplant_investment_list(self, 
                        startDate = get_last_year(),
                        endDate = get_today(),
                        function = "export"):
        """
        Lisanslı Santral Yatırımları Listeleme Servisi 
        ----------------------
        Enerji İşleri Genel Müdürlüğü tarafından ön kabulü tamamlanmış ve devreye alınmış elektrik üretim tesislerinin aylık listesidir. Elektrik üretim tesislerinin aylık listesidir.
        ----------------------
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "licensed_powerplant_investment_list", function)

        check = self.master.control_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result



    def realtime_generation(self, 
                    powerPlantId = None,
                        startDate = get_today(),
                        endDate = get_today(),
                        function = "export"):
        """
        Gerçek Zamanlı Üretim Listeleme Servisi 
        ----------------------
        Elektrik üretiminin kaynak bazında saatlik gösterimidir.
        ----------------------
        powerPlantId = int default: None
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "realtime_generation", function)

        check = self.master.control_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(
            powerPlantId = powerPlantId,
            startDate = startDate,
                    endDate = endDate,
                    )

        try:
            self.result = self.master.request_data(url, data, function, self.headers, self.information)
            return self.result
        except:
            print("Not valid powerplantID, check these.")
            return self.powerplant_list()["items"]



    def sbfgp(self, 
            uevcbId = None,
            organizationId = None,
                        startDate = get_today(),
                        endDate = get_today(),
                        function = "export"):
        """
        Kesinleştirilmiş Uzlaştırma Dönemi Üretim Planı (KUDÜP) Listeleme Servisi 
        ----------------------
        Gün öncesinde bildirilen UEVÇB bazında kaynaklara göre kesinleşmiş günlük üretim planlarının gün içi piyasasının kapanışından sonra DUY 69. madde kapsamında güncellenmesiyle oluşan kesinleşmiş günlük üretim planları.
        ----------------------
        uevcbId = int default: None
        organizationId = int default: None
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "sbfgp", function)


        if organizationId == None:
            uevcbId = None
        else:
            for d in [startDate, endDate]:
                uevcbs = [k["id"] for k in self.uevcb_list(organizationId, date = d)["items"]]
                if uevcbId not in uevcbs:
                    print("UEVCB ID is not in Organization port in between given dates.")
                    print("Possible UEVCB IDs: {}".format(uevcbs))
                    return self.uevcb_list(organizationId, date = startDate)


        check = self.master.control_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(
            uevcbId = uevcbId,
            organizationId = organizationId,
            startDate = startDate,
                    endDate = endDate,
                    region = self.master.region
                    )
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result



    def uevcb_list(self, 
                    organizationId,
                    date = get_today(),
                    function = "list"):
        """
        Uevçb Listeleme Servisi 
        ----------------------
        Verilen organizasyon id'ye ait UEVÇB'lerin listesini döner.
        ----------------------
        organizationId = int 
        startDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "uevcb_list", function)

        date = self.master.control_time(url, date)

        if date == False:
            return

        data = dict(organizationId = organizationId, startDate = date)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result



    def organization_list(self, 
                        startDate = get_today(),
                        endDate = get_today(),
                        function = "list"):
        """
        Organizasyon Listesi Getirme Servisi 
        ----------------------
        İstekte verilen başlangıç ve bitiş tarihleri arasında tanımlı organizasyonların listesini döner.
        ----------------------
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "organization_list", function)


        check = self.master.control_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result

    def injection_quantity_powerplant_list(self, 
                        function = "list"):
        """
        Uzlaştırma Esas Veriş Miktarı (UEVM) Santral Listesi Servisi 
        ----------------------
        Uzlaştırma Esas Veriş Miktarı (UEVM) Santral Listesi Servisi
        ----------------------
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "injection_quantity_powerplant_list", function)

        data = dict()
        self.result = self.master.request_data_get(url, data, function, self.headers, self.information)
        return self.result


    def powerplant_list(self, 
                        function = "list"):
        """
        Santral Listeleme Servisi 
        ----------------------
        Santral Listeleme Servisi
        ----------------------
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "powerplant_list", function)

        data = dict()
        self.result = self.master.request_data_get(url, data, function, self.headers, self.information)
        return self.result

    def region_list(self, 
                        function = "list"):
        """
        Bölge Listesi Getirme Servisi 
        ----------------------
        Bölge Listesi Getirme Servisi
        ----------------------
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "region_list", function)

        data = dict()
        self.result = self.master.request_data_get(url, data, function, self.headers, self.information)
        return self.result


