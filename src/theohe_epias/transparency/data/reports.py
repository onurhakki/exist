
from ..utils.get_time import get_today, get_yesterday

class Reports():
    information = dict()
    information["data"] = dict({
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

    information["details"] = {'mcp_smp_imbalance': ['startDate', 'endDate', 'function'],
 'daily_report': ['startDate', 'endDate', 'function'],
 'periodic_price_averages': ['function'],
 'periodic_price_volume': ['function'],
 'eligible_consumer_and_meter_increases': ['function'],
 'mcp_smp_averages': ['startDate', 'endDate', 'function'],
 'smp_mcp_multiple_daytime_avg': ['function'],
 'daily_prices': ['date', 'function'],
 'bpm_instructions_avg': ['date', 'function'],
 'bpm_instructions': ['date', 'function'],
 'electricity_market_volume_physically': ['startDate', 'endDate', 'function'],
 'idm_contract_summary': ['startDate', 'endDate', 'function'],
 'idm_contract': ['startDate', 'endDate', 'function'],
 'idm_order_list': ['contractId', 'startDate', 'endDate', 'function']}


    information["rename_columns"] = dict(
        PTF="PTF (TL/MWh)",
        SMF="SMF (TL/MWh)",
        )

    def __init__(self, root_url, master):
        self.main_url = root_url + "reporting-service/v1/"
        self.master = master
        self.headers = {"TGT":self.master.tgt_response, "Content-Type": "application/json"}

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

        url = self.master.get_url(self.main_url, self.information, "mcp_smp_imbalance", function)

        check = self.master.control_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check
        
        data = dict(startDate = startDate,
                    endDate = endDate)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result

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

        url = self.master.get_url(self.main_url, self.information, "daily_report", function)

        check = self.master.control_time_between(url, startDate, endDate)

        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result

    def periodic_price_averages(self, function = "export"):
        """
        Dönemlik Fiyat Ortalamaları
        ----------------------
        2021-01-01 Sonrasındaki PTF SMF'nin Ağırlıklı Ortalama ve Aritmetik Ortalamlarını getirir.
        ----------------------
        function = list veya export
        """
        url = self.master.get_url(self.main_url, self.information, "periodic_price_averages", function)

        if url == None:
            return
        data = dict()
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result

    def periodic_price_volume(self, function = "export"):
        """
        Dönemlik Piyasa Hacimleri
        ----------------------
        2021-01-01 Sonrasındaki SBDT'yi, İkili Anlaşma (İA) miktarlarını, UEVM, UEÇM ve piyasa oranlarını getirir.
        ----------------------
        function = list veya export
        """
        url = self.master.get_url(self.main_url, self.information, "periodic_price_volume", function)

        if url == None:
            return
        data = dict()
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result

    def eligible_consumer_and_meter_increases(self, function = "export"):
        """
        Serbest Tüketici ve Sayaç Artışları
        ----------------------
        2009-12-01 Sonrasındaki serbest tüketici Sayaç Adedi ve Sayaç Artış Oranını getirir.
        ----------------------
        function = list veya export
        """
        url = self.master.get_url(self.main_url, self.information, "eligible_consumer_and_meter_increases", function)

        if url == None:
            return
        data = dict()
        self.result = self.master.request_data_get(url, data, function, self.headers, self.information)
        return self.result

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

        url = self.master.get_url(self.main_url, self.information, "mcp_smp_averages", function)

        check = self.master.control_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result


    def smp_mcp_multiple_daytime_avg(self, function = "export"):
        """
        SMF ve PTF 3 Zamanlı Fiyat Ortalamaları
        ----------------------
        2021-01-01 Sonrasındaki dönemlik PTF Gündüz Ortalama, SMF Gündüz Ortalama, PTF Puant Ortalama, SMF Puant Ortalama, PTF Gece Ortalama ve SMF Gece Ortalama getirir.
        ----------------------
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "smp_mcp_multiple_daytime_avg", function)

        if url == None:
            return
        data = dict()
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result
        
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

        url = self.master.get_url(self.main_url, self.information, "daily_prices", function)

        date = self.master.control_time(url, date)

        if date == False:
            return

        data = dict(date = date)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result


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

        url = self.master.get_url(self.main_url, self.information, "bpm_instructions_avg", function)

        date = self.master.control_time(url, date)

        if date == False:
            return
        data = dict(date = date)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result

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

        url = self.master.get_url(self.main_url, self.information, "bpm_instructions", function)

        date = self.master.control_time(url, date)

        if date == False:
            return

        data = dict(date = date)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result


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

        url = self.master.get_url(self.main_url, self.information, "electricity_market_volume_physically", function)

        check = self.master.control_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result

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

        url = self.master.get_url(self.main_url, self.information, "idm_contract_summary", function)

        check = self.master.control_time_between(url, startDate, endDate)

        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result

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
        url = self.master.get_url(self.main_url, self.information, "idm_contract", function)

        check = self.master.control_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result

    def idm_order_list(self, 
                       contractId,
                          startDate = get_today(),
                          endDate = get_today(),
                          function = "export"):
        """
        GİP Teklif Listesi
        ----------------------
        Kontrat Türü kırlımında Kontrat Türü, Teklif Yönü, Fiyat (TL/MWh), Miktar (Lot), Kalan Miktar (Lot), Teklif Durumu, OEYE ve TEYE getirir.
        ----------------------
        contractId = int
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "idm_order_list", function)

        check = self.master.control_time_between(url, startDate, endDate)

        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(
            contractId = contractId,
            startDate = startDate,
                    endDate = endDate)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result

