from ..utils.get_time import get_today

class MMS():
    information = dict()
    information["data"] = dict({
"organization_list": {"list":"generation/data/organization-list"},
"power_plant_list_by_organization_id": {"list":"markets/data/power-plant-list-by-organization-id"},
"uevcb_list_by_power_plant_id": {"list":"markets/data/uevcb-list-by-power-plant-id"},
"market_message_system": {"list":"markets/data/market-message-system","export":"markets/export/market-message-system"},

    })

    information["details"] = {'organization_list': ['startDate', 'endDate', 'function'],
 'power_plant_list_by_organization_id': ['organizationId', 'date', 'function'],
 'uevcb_list_by_power_plant_id': ['powerPlantId', 'date', 'function'],
 'market_message_system': ['mesajTipId',
  'organizationId',
  'powerPlantId',
  'uevcbId',
  'startDate',
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
        self.region = "TR1"
        self.regionId = 1


    def organization_list(self, 
                        startDate = get_today(),
                        endDate = get_today(),
                        function = "list"):
        """
        Organizasyon Listesi Getirme Servisi ### Generation'daki servis ile aynıs
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

    def power_plant_list_by_organization_id(self, 
                        organizationId = None,
                        date = get_today(),
                        function = "list"):
        """
        Organizasyon Listesi Getirme Servisi 
        ----------------------
        İstekte verilen başlangıç ve bitiş tarihleri arasında tanımlı organizasyonların listesini döner.
        ----------------------
        organizationId = int default: None
        date = (2023,1,1) default: today
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "power_plant_list_by_organization_id", function)

        date = self.master.control_time(url, date)

        if date == False:
            return


        data = dict(startDate = date,
                    organizationId = organizationId)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result


    def uevcb_list_by_power_plant_id(self, 
                        powerPlantId,
                        date = get_today(),
                        function = "list"):
        """
        Piyasa Mesaj Sistemi Uevçb Listeleme Servisi 
        ----------------------
        Verilen santral id’ye ait UEVÇB’lerin listesini döner.
        ----------------------
        powerPlantId = int default: None
        date = (2023,1,1) default: today
        function = list veya export
        """


        url = self.master.get_url(self.main_url, self.information, "uevcb_list_by_power_plant_id", function)

        date = self.master.control_time(url, date)

        if date == False:
            return


        data = dict(startDate = date,
                    powerPlantId = powerPlantId)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result



    def market_message_system(self, 
                        mesajTipId = None,
                        organizationId = None,
                        powerPlantId = None,
                        uevcbId = None,
                        startDate = get_today(),
                        endDate = get_today(),
                        function = "export"):
        """
        Piyasa Mesaj Sistemi Listeleme Servisi
        ----------------------
        İlgili santralin arıza veya bakım bilgileridir.
        ----------------------
        mesajTipId = 0 [0: Arıza, 2: Bakım]
        organizationId = int default: None
        powerPlantId = int default: None
        uevcbId = int default: None
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "market_message_system", function)

        if mesajTipId not in [0,2, None]:
            print("mesajTipId should be 0 or 2. [0: Arıza, 2: Bakım]")
            return

        check = self.master.control_time_between(url, startDate, endDate)

        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(mesajTipId = mesajTipId,
                        organizationId = organizationId,
                        powerPlantId = powerPlantId,
                        uevcbId = uevcbId,
                        startDate = startDate,
                        endDate = endDate,
                        regionId = self.regionId)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result
