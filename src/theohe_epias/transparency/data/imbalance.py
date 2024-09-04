from ..utils.get_time import get_current_settlement_fday, get_current_settlement_lday, get_last_year

class IB():
    information = dict()
    information["data"] = dict({
"dsg_imbalance_quantity": {"list":"markets/imbalance/data/dsg-imbalance-quantity","export":"markets/imbalance/export/dsg-imbalance-quantity"},
"dsg_organization_list": {"list":"markets/imbalance/data/dsg-organization-list"},
"imbalance_amount": {"list":"markets/imbalance/data/imbalance-amount","export":"markets/imbalance/export/imbalance-amount"},
"imbalance_quantity": {"list":"markets/imbalance/data/imbalance-quantity","export":"markets/imbalance/export/imbalance-quantity"},

    })

    information["details"] = {'dsg_imbalance_quantity': ['dsg', 'startDate', 'endDate', 'function'],
 'dsg_organization_list': ['startDate', 'endDate', 'function'],
 'imbalance_amount': ['startDate', 'endDate', 'function'],
 'imbalance_quantity': ['startDate', 'endDate', 'function']}

    information["rename_columns"] = dict(
        PTF="PTF (TL/MWh)",
        SMF="SMF (TL/MWh)",
        )


    def __init__(self, root_url, master):
        self.main_url = root_url + "electricity-service/v1/"
        self.master = master
        self.headers = {"TGT":self.master.tgt_response, "Content-Type": "application/json"}


    def dsg_imbalance_quantity(self, 
                        dsg = None,
                        startDate = get_last_year(),
                        endDate = get_current_settlement_lday(),
                        function = "export"):
        """
        Dengeden Sorumlu Grup (DSG) Dengesizlik Miktarı Listeleme Servisi 
        ----------------------
        Dengeden sorumlu taraflar dengeleme yükümlülükleri kapsamında bir araya gelerek dengeden sorumlu grup oluşturabilirler. Dengeden sorumlu grup adına grup içinden bir dengeden sorumlu taraf, dengeden sorumlu grubun enerji dengesizliğine ilişkin Piyasa İşletmecisine karşı mali sorumluluğunu üstlenir. Dengeden sorumlu taraflarının portföyünde yer alan organizasyonların piyasa işlemleri neticesinde gerçekleşen üretim/tüketim değerlerinden ne kadar saptığını gösteren miktardır.
        ----------------------
        dsg = int default: None
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "dsg_imbalance_quantity", function)

        check = self.master.control_time_between(url, startDate, endDate)

        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(dsg = dsg,
                    startDate = startDate,
                    endDate = endDate)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result


    def dsg_organization_list(self,
                        startDate = get_current_settlement_fday(),
                        endDate = get_current_settlement_lday(),
                        function = "list"):
        """
        DSG Organizasyon Listesi Servisi 
        ----------------------
        Dengeden Sorumlu Grup servisinde kullanılan Organizasyon Listesi
        ----------------------
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "dsg_organization_list", function)

        check = self.master.control_time_between(url, startDate, endDate)

        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result


    def imbalance_amount(self, 
                        startDate = get_current_settlement_fday(),
                        endDate = get_current_settlement_lday(),
                        function = "export"):
        """
        Dengesizlik Tutarı Listeleme Servisi 
        ----------------------
        Piyasa katılımcılarının Gün Öncesi Piyasasındaki Gün İçi Piyasası, Dengeleme Güç Piyasası ve ikili Anlaşma işlemleri neticesinde gerçekleşen üretim/tüketim değerlerinden sapmaları durumunda alacaklı/borçlu olduğu tutardır.
        ----------------------
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "imbalance_amount", function)

        check = self.master.control_time_between(url, startDate, endDate)

        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result


    def imbalance_quantity(self, 
                        startDate = get_current_settlement_fday(),
                        endDate = get_current_settlement_lday(),
                        function = "export"):
        """
        Dengesizlik Miktarı Listeleme Servisi 
        ----------------------
        Piyasa katılımcılarının Gün Öncesi Piyasasındaki Gün İçi Piyasası, Dengeleme Güç Piyasası ve ikili Anlaşma işlemleri neticesinde gerçekleşen üretim/tüketim değerlerinden ne kadar saptığını gösteren miktardır.
        ----------------------
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "imbalance_quantity", function)

        check = self.master.control_time_between(url, startDate, endDate)

        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result
