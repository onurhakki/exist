import requests
import pandas as pd

from theohe_epias.transparency.utils.get_time import get_today, get_year, get_tomorrow, get_current_settlement_fday, get_current_settlement_lday, get_last_year
from theohe_epias.transparency.utils.time_format import tuple_to_datetime

class Production():
    def __init__(self):
        self.information = dict()
        self.information["data"] = dict({
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
            if url in ["https://seffaflik.epias.com.tr/electricity-service/v1/generation/data/injection-quantity-powerplant-list",
            "https://seffaflik.epias.com.tr/electricity-service/v1/generation/data/powerplant-list",
            "https://seffaflik.epias.com.tr/electricity-service/v1/generation/data/region-list",

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

        url = self._get_url("aic", function)
        if organizationId == None:
            uevcbId = None
        else:
            for d in [startDate, endDate]:
                uevcbs = [k["id"] for k in self.uevcb_list(organizationId, date = d)["items"]]
                if uevcbId not in uevcbs:
                    print("UEVCB ID is not in Organization port in between given dates.")
                    print("Possible UEVCB IDs: {}".format(uevcbs))
                    return self.uevcb_list(organizationId, date = startDate)


        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(
            uevcbId = uevcbId,
            organizationId = organizationId,
            startDate = startDate,
                    endDate = endDate,
                    region = self.region
                    )
        self.final_result = self._request_data(url, data, function)
        return self.final_result


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

        url = self._get_url("dpp", function)

        if organizationId == None:
            uevcbId = None
        else:
            for d in [startDate, endDate]:
                uevcbs = [k["id"] for k in self.uevcb_list(organizationId, date = d)["items"]]
                if uevcbId not in uevcbs:
                    print("UEVCB ID is not in Organization port in between given dates.")
                    print("Possible UEVCB IDs: {}".format(uevcbs))
                    return self.uevcb_list(organizationId, date = startDate)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(
            uevcbId = uevcbId,
            organizationId = organizationId,
            startDate = startDate,
                    endDate = endDate,
                    region = self.region
                    )
        self.final_result = self._request_data(url, data, function)
        return self.final_result


    def injection_quantity(self,
                    powerplantId = None,
                        startDate = get_current_settlement_fday(),
                        endDate = get_current_settlement_lday(),
                        function = "export"):
        """
        Uzlaştırma Esas Veriş Miktarı (UEVM) Listeleme Servisi 
        ----------------------
        Uzlaştırmaya esas veriş birimlerinin, bir uzlaştırma dönemi içinde saatlik olarak sisteme verdiği elektrik miktarının toplam değeridir.
        ----------------------
        powerplantId = int default: None
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self._get_url("injection_quantity", function)

        if powerplantId != None:
            pp_list = self.injection_quantity_powerplant_list()
            pp_ids = [k["id"] for k in pp_list["items"]]
            if powerplantId not in pp_ids:
                print("powerplantId is not found.")
                return pp_list

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(
            powerplantId = powerplantId,
            startDate = startDate,
                    endDate = endDate,
                    )
        try:
            self.final_result = self._request_data(url, data, function)
            return self.final_result
        except:
            print("Not valid powerplantID, check these.")
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

        url = self._get_url("licensed_powerplant_investment_list", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result



    def realtime_generation(self, 
                    powerplantId = None,
                        startDate = get_today(),
                        endDate = get_today(),
                        function = "export"):
        """
        Gerçek Zamanlı Üretim Listeleme Servisi 
        ----------------------
        Elektrik üretiminin kaynak bazında saatlik gösterimidir.
        ----------------------
        powerplantId = int default: None
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self._get_url("realtime_generation", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(
            powerPlantId = powerplantId,
            startDate = startDate,
                    endDate = endDate,
                    )

        try:
            self.final_result = self._request_data(url, data, function)
            return self.final_result
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

        url = self._get_url("sbfgp", function)

        if organizationId == None:
            uevcbId = None
        else:
            for d in [startDate, endDate]:
                uevcbs = [k["id"] for k in self.uevcb_list(organizationId, date = d)["items"]]
                if uevcbId not in uevcbs:
                    print("UEVCB ID is not in Organization port in between given dates.")
                    print("Possible UEVCB IDs: {}".format(uevcbs))
                    return self.uevcb_list(organizationId, date = startDate)


        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(
            uevcbId = uevcbId,
            organizationId = organizationId,
            startDate = startDate,
                    endDate = endDate,
                    region = self.region
                    )
        self.final_result = self._request_data(url, data, function)
        return self.final_result



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

        url = self._get_url("uevcb_list", function)

        date = self._control_and_format_time(url, date)
        if date == False:
            return

        data = dict(organizationId = organizationId, startDate = date)
        self.final_result = self._request_data(url, data, function)
        return self.final_result



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

        url = self._get_url("organization_list", function)


        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result


    def injection_quantity_powerplant_list(self, 
                        function = "list"):
        """
        Uzlaştırma Esas Veriş Miktarı (UEVM) Santral Listesi Servisi 
        ----------------------
        Uzlaştırma Esas Veriş Miktarı (UEVM) Santral Listesi Servisi
        ----------------------
        function = list veya export
        """

        url = self._get_url("injection_quantity_powerplant_list", function)
        data = dict()
        self.final_result = self._request_data(url, data, function)
        return self.final_result


    def powerplant_list(self, 
                    powerplantId = None,
                        function = "list"):
        """
        Santral Listeleme Servisi 
        ----------------------
        Santral Listeleme Servisi
        ----------------------
        function = list veya export
        """

        url = self._get_url("powerplant_list", function)
        data = dict()
        self.final_result = self._request_data(url, data, function)
        return self.final_result

    def region_list(self, 
                        function = "list"):
        """
        Bölge Listesi Getirme Servisi 
        ----------------------
        Bölge Listesi Getirme Servisi
        ----------------------
        function = list veya export
        """

        url = self._get_url("region_list", function)
        data = dict()
        self.final_result = self._request_data(url, data, function)
        return self.final_result


