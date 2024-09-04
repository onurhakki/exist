
# from ...transparency.utils.time_format import tuple_to_datetime
# from ..utils.get_time import get_this_month, get_time_dam

class Dams():
    information = dict()
    information["data"] = dict({
"active_fullness": {"list":"dams/data/active-fullness","export":"dams/export/active-fullness"},
"active_volume": {"list":"dams/data/active-volume","export":"dams/export/active-volume"},
"basin_list": {"list":"dams/data/basin-list"},
"daily_kot": {"list":"dams/data/daily-kot","export":"dams/export/daily-kot"},
"daily_volume": {"list":"dams/data/daily-volume","export":"dams/export/daily-volume"},
"dam_kot": {"list":"dams/data/dam-kot","export":"dams/export/dam-kot"},
"dam_list": {"list":"dams/data/dam-list"},
"dam_volume": {"list":"dams/data/dam-volume","export":"dams/export/dam-volume"},
"flow_rate_and_installed_power": {"list":"dams/data/flow-rate-and-installed-power","export":"dams/export/flow-rate-and-installed-power"},
"water_energy_provision": {"list":"dams/data/water-energy-provision","export":"dams/export/water-energy-provision"},

    })

    information["details"] = {'active_fullness': ['basinName', 'damName', 'function'],
 'active_volume': ['basinName', 'damName', 'function'],
 'basin_list': ['function'],
 'daily_kot': ['basinName', 'damName', 'function'],
 'daily_volume': ['basinName', 'damName', 'function'],
 'dam_kot': ['basinName', 'damName', 'function'],
 'dam_list': ['basinName', 'function'],
 'dam_volume': ['basinName', 'damName', 'function'],
 'flow_rate_and_installed_power': ['basinName', 'damName', 'function'],
 'water_energy_provision': ['basinName', 'damName', 'function']}
    
    information["rename_columns"] = dict(
        PTF="PTF (TL/MWh)",
        SMF="SMF (TL/MWh)",
        )

    def __init__(self, root_url, master):
        self.main_url = root_url + "electricity-service/v1/"
        self.master = master
        self.headers = {"TGT":self.master.tgt_response, "Content-Type": "application/json"}

    def active_fullness(self, 
                        basinName = None,
                        damName = None,
                        function = "export"):
        """
        Aktif Doluluk Listeleme Servisi 
        ----------------------
        Bir barajın maksimum ve minimum işletme seviyeleri arasındaki hacimin yüzdesidir. Formül: Aktif Doluluk= [( İlgili Tarihteki Seviyeye Karşılık Gelen Hacim – Minimum Hacim ) / ( Maksimum Hacim – Minimum Hacim )] * 100. Veriler saat 17:00 itibariyle nihai halini almaktadır. Baraj verileri günlük olarak verilmektedir. Geriye dönük veri bulunmamaktadır.
        ----------------------
        basinName = str default: None
        damName = str default: None
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "active_fullness", function)

        if basinName != None:
            vals = self.basin_list()
            if basinName not in vals:
                print("basinName is not in vals. check",vals)
                return

        if damName != None:
            vals = self.dam_list()["damList"]
            if damName not in vals:
                print("basinName is not in vals. check",vals)
                return

        data = dict(basinName = basinName,damName=damName)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result

    def active_volume(self, 
                        basinName = None,
                        damName = None,
                        function = "export"):
        """
        Aktif Hacim Listeleme Servisi 
        ----------------------
        Bir barajın ilgili tarihteki seviyeye karşılık gelen hacmi ve minimum işletme seviyeleri arasındaki hacimdir. Veriler saat 17:00 itibariyle nihai halini almaktadır. Baraj verileri günlük olarak verilmektedir. Geriye dönük veri verilmemektedir.
        ----------------------
        basinName = str default: None
        damName = str default: None
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "active_volume", function)

        if basinName != None:
            vals = self.basin_list()
            if basinName not in vals:
                print("basinName is not in vals. check",vals)
                return

        if damName != None:
            vals = self.dam_list()["damList"]
            if damName not in vals:
                print("basinName is not in vals. check",vals)
                return

        data = dict(basinName = basinName,damName=damName)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result
        
    def basin_list(self, function = "list"):
        """
        Havza listesini dönen servisir. 
        ----------------------
        Havza listesini dönen servisir.
        ----------------------
        function = list
        """

        url = self.master.get_url(self.main_url, self.information, "basin_list", function)

        data = dict()
        self.result = self.master.request_data_get(url, data, function, self.headers, self.information)
        return self.result

    def daily_kot(self, 
                        basinName = None,
                        damName = None,
                        function = "export"):
        """
        Günlük Kot Listeleme Servisi 
        ----------------------
        Barajın ilgili gündeki su yüksekliğini belirtir. Veriler saat 17:00 itibariyle nihai halini almaktadır. Baraj verileri günlük olarak verilmektedir. Geriye dönük veri bulunmamaktadır.
        ----------------------
        basinName = str default: None
        damName = str default: None
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "daily_kot", function)

        if basinName != None:
            vals = self.basin_list()
            if basinName not in vals:
                print("basinName is not in vals. check",vals)
                return

        if damName != None:
            vals = self.dam_list()["damList"]
            if damName not in vals:
                print("basinName is not in vals. check",vals)
                return

        data = dict(basinName = basinName,damName=damName)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result

    def daily_volume(self, 
                        basinName = None,
                        damName = None,
                        function = "export"):
        """
        Günlük Hacim Listeleme Servisi 
        ----------------------
        Bir barajın ilgili tarihteki seviyesine karşılık gelen hacimdir. Veriler saat 17:00 itibariyle nihai halini almaktadır. Baraj verileri günlük olarak verilmektedir. Geriye dönük veri verilmemektedir.
        ----------------------
        basinName = str default: None
        damName = str default: None
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "daily_volume", function)

        if basinName != None:
            vals = self.basin_list()
            if basinName not in vals:
                print("basinName is not in vals. check",vals)
                return

        if damName != None:
            vals = self.dam_list()["damList"]
            if damName not in vals:
                print("basinName is not in vals. check",vals)
                return

        data = dict(basinName = basinName,damName=damName)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result

    def dam_kot(self, 
                        basinName = None,
                        damName = None,
                        function = "export"):
        """
        Kot Listeleme Servisi 
        ----------------------
        İlgili barajın maximum ve minumum seviyesini gösterir.
        ----------------------
        basinName = str default: None
        damName = str default: None
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "dam_kot", function)

        if basinName != None:
            vals = self.basin_list()
            if basinName not in vals:
                print("basinName is not in vals. check",vals)
                return

        if damName != None:
            vals = self.dam_list()["damList"]
            if damName not in vals:
                print("basinName is not in vals. check",vals)
                return

        data = dict(basinName = basinName,damName=damName)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result


    def dam_list(self, 
                        basinName = None,
                        function = "list"):
        """
        Havza ismi ile Barajlar listesini dönen servisir. 
        ----------------------
        Havza ismi ile Barajlar listesini dönen servisir.
        ----------------------
        basinName = str default: None
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "dam_list", function)
        if basinName != None:
            vals = self.basin_list()
            print(vals)


        data = dict(basinName = basinName)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result

    def dam_volume(self, 
                        basinName = None,
                        damName = None,
                        function = "export"):
        """
        Hacim Listeleme Servisi 
        ----------------------
        İlgili barajın maksimum ve minumum hacim seviyesini gösterir.
        ----------------------
        basinName = str default: None
        damName = str default: None
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "dam_volume", function)

        if basinName != None:
            vals = self.basin_list()
            if basinName not in vals:
                print("basinName is not in vals. check",vals)
                return

        if damName != None:
            vals = self.dam_list()["damList"]
            if damName not in vals:
                print("basinName is not in vals. check",vals)
                return

        data = dict(basinName = basinName,damName=damName)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result

    def flow_rate_and_installed_power(self, 
                        basinName = None,
                        damName = None,
                        function = "export"):
        """
        Debi ve Kurulu Güç Listeleme Servisi 
        ----------------------
        İlgili barajda üniteden geçen suyun miktarını ve barajın kurulu gücünü gösterir.
        ----------------------
        basinName = str default: None
        damName = str default: None
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "flow_rate_and_installed_power", function)

        if basinName != None:
            vals = self.basin_list()
            if basinName not in vals:
                print("basinName is not in vals. check",vals)
                return

        if damName != None:
            vals = self.dam_list()["damList"]
            if damName not in vals:
                print("basinName is not in vals. check",vals)
                return

        data = dict(basinName = basinName,damName=damName)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result

    def water_energy_provision(self, 
                        basinName = None,
                        damName = None,
                        function = "export"):
        """
        Suyun Enerji Karşılığı Listeleme Servisi 
        ----------------------
        Barajda yer alan suyun hesaplanan MWh cinsinden enerji karşılığıdır. Veriler saat 17:00 itibariyle nihai halini almaktadır. Baraj verileri günlük olarak verilmektedir. Geriye dönük veri verilmemektedir.
        ----------------------
        basinName = str default: None
        damName = str default: None
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "water_energy_provision", function)

        if basinName != None:
            vals = self.basin_list()
            if basinName not in vals:
                print("basinName is not in vals. check",vals)
                return

        if damName != None:
            vals = self.dam_list()["damList"]
            if damName not in vals:
                print("basinName is not in vals. check",vals)
                return

        data = dict(basinName = basinName,damName=damName)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result

