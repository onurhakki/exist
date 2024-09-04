from ..utils.get_time import get_tomorrow

class AS():
    information = dict()
    information["data"] = dict({
"primary_frequency_capacity_amount": {"list":"markets/ancillary-services/data/primary-frequency-capacity-amount","export":"markets/ancillary-services/export/primary-frequency-capacity-amount"},
"primary_frequency_capacity_price": {"list":"markets/ancillary-services/data/primary-frequency-capacity-price","export":"markets/ancillary-services/export/primary-frequency-capacity-price"},
"secondary_frequency_capacity_amount": {"list":"markets/ancillary-services/data/secondary-frequency-capacity-amount","export":"markets/ancillary-services/export/secondary-frequency-capacity-amount"},
"secondary_frequency_capacity_price": {"list":"markets/ancillary-services/data/secondary-frequency-capacity-price","export":"markets/ancillary-services/export/secondary-frequency-capacity-price"},
    })

    information["details"] = {'primary_frequency_capacity_amount': ['startDate', 'endDate', 'function'],
 'primary_frequency_capacity_price': ['startDate', 'endDate', 'function'],
 'secondary_frequency_capacity_amount': ['startDate', 'endDate', 'function'],
 'secondary_frequency_capacity_price': ['startDate', 'endDate', 'function']}

    information["rename_columns"] = dict(
        PTF="PTF (TL/MWh)",
        SMF="SMF (TL/MWh)",
        )
    def __init__(self, root_url, master):
        self.main_url = root_url + "electricity-service/v1/"
        self.master = master
        self.headers = {"TGT":self.master.tgt_response, "Content-Type": "application/json"}

    def primary_frequency_capacity_amount(self, 
                        startDate = get_tomorrow(),
                        endDate = get_tomorrow(),
                        function = "export"):
        """
        Primer Frekans Rezerv Miktarı Listeleme Servisi 
        ----------------------
        Katılımcıların gerçek zamanlı frekans dengeleme için ayırması gereken saatlik toplam birincil frekans kapasite hacimleridir.
        ----------------------
        startDate = (2023,1,1) default: tomorrow
        endDate = (2023,1,1) default: tomorrow
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "primary_frequency_capacity_amount", function)

        check = self.master.control_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result
    
    def primary_frequency_capacity_price(self, 
                        startDate = get_tomorrow(),
                        endDate = get_tomorrow(),
                        function = "export"):
        """
        Primer Frekans Kontrolü (PFK) Fiyat Listeleme Servisi 
        ----------------------
        Saatlik bazda ihale ile belirlenen PFK kapasite bedelidir.
        ----------------------
        startDate = (2023,1,1) default: tomorrow
        endDate = (2023,1,1) default: tomorrow
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "primary_frequency_capacity_price", function)

        check = self.master.control_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result

    def secondary_frequency_capacity_amount(self, 
                        startDate = get_tomorrow(),
                        endDate = get_tomorrow(),
                        function = "export"):
        """
        Sekonder Frekans Rezerv Miktarı Listeleme Servisi 
        ----------------------
        Saatlik toplam belirlenen rezerv miktarlarıdır.
        ----------------------
        startDate = (2023,1,1) default: tomorrow
        endDate = (2023,1,1) default: tomorrow
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "secondary_frequency_capacity_amount", function)

        check = self.master.control_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result

    def secondary_frequency_capacity_price(self, 
                        startDate = get_tomorrow(),
                        endDate = get_tomorrow(),
                        function = "export"):
        """
        Sekonder Frekans Kontrolü (SFK) Fiyat Listeleme Servisi 
        ----------------------
        Saatlik bazda ihale ile belirlenen SFK kapasite bedelidir.
        ----------------------
        startDate = (2023,1,1) default: tomorrow
        endDate = (2023,1,1) default: tomorrow
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "secondary_frequency_capacity_price", function)

        check = self.master.control_time_between(url, startDate, endDate)
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result

