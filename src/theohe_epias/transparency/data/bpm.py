from ..utils.get_time import get_today, get_yesterday

class BPM():
    information = dict()
    information["data"] = dict({
"order_summary_down": {"list":"markets/bpm/data/order-summary-down","export":"markets/bpm/export/order-summary-down"},
"order_summary_up": {"list":"markets/bpm/data/order-summary-up","export":"markets/bpm/export/order-summary-up"},
"system_direction": {"list":"markets/bpm/data/system-direction","export":"markets/bpm/export/system-direction"},
"smp": {"list":"markets/bpm/data/system-marginal-price","export":"markets/bpm/export/system-marginal-price"},
    })

    information["details"] = {'order_summary_down': ['startDate', 'endDate', 'function'],
 'order_summary_up': ['startDate', 'endDate', 'function'],
 'system_direction': ['startDate', 'endDate', 'function'],
 'smp': ['startDate', 'endDate', 'function']}
    
    information["rename_columns"] = dict(
        PTF="PTF (TL/MWh)",
        SMF="SMF (TL/MWh)",
        )


    def __init__(self, root_url, master):
        self.main_url = root_url + "electricity-service/v1/"
        self.master = master
        self.headers = {"TGT":self.master.tgt_response, "Content-Type": "application/json"}


    def order_summary_down(self, 
                        startDate = get_yesterday(),
                        endDate = get_today(),
                        function = "export"):
        """
        Yük Atma (YAT) Talimat Miktarı Listeleme Servisi 
        ----------------------
        0, 1, 2 kodlu Alma Talimat Miktarı (YAT), sistem yönünde elektrik fazlası durumlarda sistemi dengelemek için verilen talimat miktarıdır. Veriler 4 saat önceki talimatları yansıtmaktadır.
        ----------------------
        startDate = (2023,1,1) default: yesterday
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "order_summary_down", function)

        check = self.master.control_time_between(url, startDate, endDate)

        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result


    def order_summary_up(self, 
                        startDate = get_yesterday(),
                        endDate = get_today(),
                        function = "export"):
        """
        Yük Alma (YAL) Talimat Miktarları Listeleme Servisi 
        ----------------------
        0, 1, 2 kodlu Alma Talimat Miktarı (YAL), sistem yönünde elektrik açığı durumlarda sistemi dengelemek için verilen talimat miktarıdır. Veriler 4 saat önceki talimatları yansıtmaktadır.
        ----------------------
        startDate = (2023,1,1) default: yesterday
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "order_summary_up", function)

        check = self.master.control_time_between(url, startDate, endDate)

        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result


    def system_direction(self, 
                        startDate = get_yesterday(),
                        endDate = get_today(),
                        function = "export"):
        """
        Sistem Yönü Listeleme Servisi 
        ----------------------
        Sistemde elektrik fazlası veya elektrik açığı olduğunu gösterir. Veriler 4 saat önceki talimatları yansıtmaktadır.
        ----------------------
        startDate = (2023,1,1) default: yesterday
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "system_direction", function)

        check = self.master.control_time_between(url, startDate, endDate)
        
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result


    def smp(self, 
                        startDate = get_yesterday(),
                        endDate = get_today(),
                        function = "export"):
        """
        Sistem Marjinal Fiyatı Listeleme Servisi 
        ----------------------
        Sistem Marjinal Fiyatı, Dengeleme Güç Piyasasında net talimat hacmine karşılık gelen teklifin fiyatıdır. Veriler 4 saat önceki talimatları yansıtmaktadır.
        ----------------------
        startDate = (2023,1,1) default: yesterday
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "smp", function)

        check = self.master.control_time_between(url, startDate, endDate)
        
        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result
