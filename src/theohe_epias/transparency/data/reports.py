import requests
import pandas as pd

from theohe_epias.transparency.utils.get_time import get_today, get_yesterday
from theohe_epias.transparency.utils.time_format import tuple_to_datetime

class Reports():
    def __init__(self):
        self.information = dict()
        self.information["data"] = dict({
            "mcp_smp_imbalance": {"list":"data/ptf-smf-sdf", "export":"export/ptf-smf-sdf"},
            "daily_report": {"list":"data/daily-report", "export":"export/daily-report"},
            "periodic_price_averages": {"list":"data/periodic-price-averages", "export":"export/periodic-price-averages"},
            "periodic_price_volume": {"list":"data/periodic-price-volume", "export":"export/periodic-price-volume"},
            "eligible_consumer_and_meter_increases": {"list":"data/eligible-consumer-and-meter-increases", "export":"export/eligible-consumer-and-meter-increases"},
            "mcp_smp_averages": {"list":"data/mcp-smp-averages", "export":"export/mcp-smp-averages"},
            "smp_mcp_multiple_daytime_avg": {"list":"data/smp-mcp-multiple-daytime-avg", "export":"export/smp-mcp-multiple-daytime-avg"},
            "daily_prices": {"list":"data/daily-prices", "export":"export/daily-prices"},
            "bpm_instructions_avg": {"list":"data/dgp-talimat-agr-ort", "export":"export/dgp-talimat-agr-ort"},
            "bpm_instructions": {"list":"data/dgp-talimat", "export":"export/dgp-talimat"},
            "electricity_market_volume_physically":{"list":"data/electricity-market-volume-physically", "export":"export/electricity-market-volume-physically"},
            "idm_contract_summary": {"list":"data/idm-contract-summary", "export":"export/idm-contract-summary"},
            "idm_contract": {"list":"data/gip-kontrat"},
            "idm_order_list": {"list":"data/idm-order-list", "export":"export/idm-order-list"},    
        })

        self.information["details"] = dict({
            "mcp_smp_imbalance": ["startDate", "endDate", "function"],
            "daily_report": ["startDate", "endDate", "function"],
            "periodic_price_averages": ["function"],
            "periodic_price_volume": ["function"],
            "eligible_consumer_and_meter_increases": ["function"],
            "mcp_smp_averages": ["startDate", "endDate", "function"],
            "smp_mcp_multiple_daytime_avg": ["function"],
            "daily_prices": ["date", "function"],
            "bpm_instructions_avg": ["date", "function"],
            "bpm_instructions": ["date", "function"],
            "electricity_market_volume_physically": ["startDate", "endDate", "function"],
            "idm_contract_summary": ["startDate", "endDate", "function"],
            "idm_contract": ["startDate", "endDate", "function"],
            "idm_order_list": ["startDate", "endDate", "function"],            
        })

        self.information["rename_columns"] = dict(
            PTF="PTF (TL/MWh)",
            SMF="SMF (TL/MWh)",
            )

        self.main_url = "https://seffaflik.epias.com.tr/reporting-service/v1/"


    def _get_url(self, attr, function):
        if function in ["export","list"]:
            url = self.main_url + self.information["data"][attr][function]
            return url
        else:
            print("Not Defined Function.")
            return None
        

    def _request_data(self, url, data, function):
        if function == "list":

            if url in ["https://seffaflik.epias.com.tr/reporting-service/v1/data/eligible-consumer-and-meter-increases"]:
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


    def _control_and_format_time(self, url, date):
        date = tuple_to_datetime(date)
        if url == None or date == False:
            return False
        else:
            return date



    def mcp_smp_imbalance(self, 
                          startDate = get_today(),
                          endDate = get_today(),
                          function = "export"):
        """
        PTF, SMF ve SDF Listeleme
        ----------------------
        Saatlik kırlımda PTF, SMF, Pozitif Dengesizlik Fiyatı (TL/MWh), Negatif Dengesizlik Fiyatı (TL/MWh) ve SMF Yönü getirir.
        ----------------------
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self._get_url("mcp_smp_imbalance", function)
        
        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check
        
        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result

    def daily_report(self, 
                          startDate = get_today(),
                          endDate = get_today(),
                          function = "export"):
        """
        Günlük Rapor
        ----------------------
        Saatlik kırlımda Yük Tahmin Planı (MWh), İkili Anlaşma (MWh), PTF (TL/MWh), SAM (MWh), SSM (MWh), KGÜP (MWh), SMF (TL/MWh) ve TEİAŞ talimatlarını getirir.
        ----------------------
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self._get_url("daily_report", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result

    def periodic_price_averages(self, function = "export"):
        """
        Dönemlik Fiyat Ortalamaları
        ----------------------
        2021-01-01 Sonrasındaki PTF SMF'nin Ağırlıklı Ortalama ve Aritmetik Ortalamlarını getirir.
        ----------------------
        function = list veya export
        """
        url = self._get_url("periodic_price_averages", function)
        if url == None:
            return
        data = dict()
        self.final_result = self._request_data(url, data, function)
        return self.final_result

    def periodic_price_volume(self, function = "export"):
        """
        Dönemlik Piyasa Hacimleri
        ----------------------
        2021-01-01 Sonrasındaki SBDT'yi, İkili Anlaşma (İA) miktarlarını, UEVM, UEÇM ve piyasa oranlarını getirir.
        ----------------------
        function = list veya export
        """
        url = self._get_url("periodic_price_volume", function)
        if url == None:
            return
        data = dict()
        self.final_result = self._request_data(url, data, function)
        return self.final_result

    def eligible_consumer_and_meter_increases(self, function = "export"):
        """
        Serbest Tüketici ve Sayaç Artışları
        ----------------------
        2009-12-01 Sonrasındaki serbest tüketici Sayaç Adedi ve Sayaç Artış Oranını getirir.
        ----------------------
        function = list veya export
        """
        url = self._get_url("eligible_consumer_and_meter_increases", function)
        if url == None:
            return
        data = dict()
        self.final_result = self._request_data(url, data, function)
        return self.final_result

    def mcp_smp_averages(self, 
                          startDate = get_today(),
                          endDate = get_today(),
                          function = "export"):
        """
        SMF ve PTF Fiyat Ortalamaları
        ----------------------
        Günlük kırlımda PTF Ağırlıklı Ortalama, SMF Ağırlıklı Ortalama, PTF Aritmetik Ortalama ve SMF Aritmetik Ortalama getirir.
        ----------------------
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self._get_url("mcp_smp_averages", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result


    def smp_mcp_multiple_daytime_avg(self, function = "export"):
        """
        SMF ve PTF 3 Zamanlı Fiyat Ortalamaları
        ----------------------
        2021-01-01 Sonrasındaki dönemlik PTF Gündüz Ortalama, SMF Gündüz Ortalama, PTF Puant Ortalama, SMF Puant Ortalama, PTF Gece Ortalama ve SMF Gece Ortalama getirir.
        ----------------------
        function = list veya export
        """

        url = self._get_url("smp_mcp_multiple_daytime_avg", function)
        if url == None:
            return
        data = dict()
        self.final_result = self._request_data(url, data, function)
        return self.final_result
        
    def daily_prices(self, 
                          date = get_today(),
                          function = "export"):
        """
        Günlük Fiyatlar
        ----------------------
        Saatlik PTF, 1 Ay Önceki PTF, SMF, 1 Ay Önceki SMF ve SMF Yön getirir.
        ----------------------
        date = (2023,1,1) default: yesterday
        function = list veya export
        """

        url = self._get_url("daily_prices", function)

        date = self._control_and_format_time(url, date)
        if date == False:
            return

        data = dict(date = date)
        self.final_result = self._request_data(url, data, function)
        return self.final_result


    def bpm_instructions_avg(self, 
                          date = get_today(),
                          function = "export"):
        """
        DGP Talimatları (Ağırlıklı Ortalama)
        ----------------------
        Saatlik Net Talimat, YAL 0 Miktar, YAL 0 Ağırlıklı Ort., YAL 1 Miktar, YAL 1 Ağırlıklı Ort., YAL 2 Miktar, YAL 2 Ağırlıklı Ort., YAT 0 Miktar, 
        YAT 0 Ağırlıklı Ort., YAT 1 Miktar, YAT 1 Ağırlıklı Ort., YAT 2 Miktar, YAT 2 Ağırlıklı Ort., Yerine Getirilen YAL, Yerine Getirilen YAT, SMF ve PTF getirir.
        ----------------------
        date = (2023,1,1) default: today
        function = list veya export
        """

        url = self._get_url("bpm_instructions_avg", function)

        date = self._control_and_format_time(url, date)
        if date == False:
            return

        data = dict(date = date)
        self.final_result = self._request_data(url, data, function)
        return self.final_result

    def bpm_instructions(self, 
                          date = get_today(),
                          function = "export"):
        """
        DGP Talimatları
        ----------------------
        Saatlik Net Talimat, YAL 0 Miktar,YAL 0 Fiyat,YAL 1 Miktar,YAL 1 Fiyat, YAL 2 Miktar,YAL 2 Fiyat,YAT 0 Miktar,YAT 0 Fiyat,
        YAT 1 Miktar,YAT 1 Fiyat,YAT 2 Miktar,YAT 2 Fiyat Yerine Getirilen YAL, Yerine Getirilen YAT, SMF ve PTF getirir.
        ----------------------
        date = (2023,1,1) default: today
        function = list veya export
        """

        url = self._get_url("bpm_instructions", function)

        date = self._control_and_format_time(url, date)
        if date == False:
            return

        data = dict(date = date)
        self.final_result = self._request_data(url, data, function)
        return self.final_result


    def electricity_market_volume_physically(self, 
                          startDate = get_today(),
                          endDate = get_today(),
                          function = "export"):
        """
        Elektrik Piyasa Hacimleri Fiziksel
        ----------------------
        Saatlik kırlımda İ.A. Hacmi, Kamu İ.A. Hacmi, Özel Sektör İ.A. Hacmi, GÖP Hacmi, DGP Hacmi ve Toplam Piyasa Hacmini getirir.
        ----------------------
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self._get_url("electricity_market_volume_physically", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result

    def idm_contract_summary(self, 
                          startDate = get_today(),
                          endDate = get_today(),
                          function = "export"):
        """
        GİP Kontrat Özeti
        ----------------------
        Kontrat Türü kırlımında kontrat istatistiklerini getirir.
        ----------------------
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self._get_url("idm_contract_summary", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result

    def idm_contract(self, 
                          startDate = get_today(),
                          endDate = get_today(),
                          function = "list"):
        """
        GİP Kontrat
        ----------------------
        GİP Kontratlarını getirir.
        ----------------------
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list
        """

        url = self._get_url("idm_contract", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result

    def idm_order_list(self, 
                          startDate = get_today(),
                          endDate = get_today(),
                          function = "export"):
        """
        GİP Teklif Listesi
        ----------------------
        Kontrat Türü kırlımında Kontrat Türü, Teklif Yönü, Fiyat (TL/MWh), Miktar (Lot), Kalan Miktar (Lot), Teklif Durumu, OEYE ve TEYE getirir.
        ----------------------
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self._get_url("idm_order_list", function)

        check = self._control_and_format_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.final_result = self._request_data(url, data, function)
        return self.final_result

