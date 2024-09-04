from ..utils.get_time import get_today

class GD():
    information = dict()
    information["data"] = dict({
"market_participants": {"list":"markets/general-data/data/market-participants","export":"markets/general-data/export/market-participants"},
"market_participants_organization_filter_list": {"list":"markets/general-data/data/market-participants-organization-filter-list"},
"participant_count_based_upon_license_type": {"list":"markets/general-data/data/participant-count-based-upon-license-type","export":"markets/general-data/export/participant-count-based-upon-license-type"},

    })

    information["details"] = {'market_participants': ['organizationId', 'function'],
 'market_participants_organization_filter_list': ['function'],
 'participant_count_based_upon_license_type': ['date', 'function']}


    information["rename_columns"] = dict(
        PTF="PTF (TL/MWh)",
        SMF="SMF (TL/MWh)",
        )

    def __init__(self, root_url, master):
        self.main_url = root_url + "electricity-service/v1/"
        self.master = master
        self.headers = {"TGT":self.master.tgt_response, "Content-Type": "application/json"}

    def market_participants(self, 
                        organizationId = None,
                        function = "export"):
        """
        Piyasa Katılımcıları Listeleme Servisi 
        ----------------------
        Piyasa Katılımcıları’nın GÖP, GİP, VEP, YEK-G piyasalarına katılım durumunu belirtir. Ayrıca Tüzel kişilik olarak firmanın aktiflik/pasiflik durumunu bildirir.
        ----------------------
        organizationId = int default: None
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "market_participants", function)

        data = dict(organizationId = organizationId)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result


    def market_participants_organization_filter_list(self, 
                        function = "list"):
        """
        Piyasa Katılımcıları Organizasyon Filtre Listesi Servisi 
        ----------------------
        Piyasa Katılımcıları Organizasyon Filtre Listesi
        ----------------------
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "market_participants_organization_filter_list", function)

        data = dict()
        self.result = self.master.request_data_get(url, data, function, self.headers, self.information)
        return self.result


    def participant_count_based_upon_license_type(self, 
                        date = get_today(),
                        function = "export"):
        """
        Lisans Türüne Göre Katılımcı Sayısı Listeleme Servisi 
        ----------------------
        Kamu ve Özel Sektör piyasa katılımcılarının Üretim, Tedarik, Dağıtım, OSB Üretim, İletim ve Görevli Tedaril lisansları türlerine göre toplam sayılarını gösterir. Görevli tedarik şirketleri tüketici grupları için K1 (21), K2 (21) ve K3 (21) olacak şekilde kategorize edilmiştir.
        ----------------------
        date = (2023,1,1) default: today
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "participant_count_based_upon_license_type", function)

        date = self.master.control_time(url, date)

        if date == False:
            return

        data = dict(startDate = date)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result
