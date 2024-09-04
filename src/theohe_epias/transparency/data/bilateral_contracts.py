from ..utils.get_time import get_this_month, get_time_dam, get_today, get_year


class BC(): 
    information = dict()
    information["data"] = dict({
"amount_of_bilateral_contracts": {"list":"markets/bilateral-contracts/data/amount-of-bilateral-contracts","export":"markets/bilateral-contracts/export/amount-of-bilateral-contracts"},
"bilateral_contracts_bid_quantity": {"list":"markets/bilateral-contracts/data/bilateral-contracts-bid-quantity","export":"markets/bilateral-contracts/export/bilateral-contracts-bid-quantity"},
"bilateral_contracts_offer_quantity": {"list":"markets/bilateral-contracts/data/bilateral-contracts-offer-quantity","export":"markets/bilateral-contracts/export/bilateral-contracts-offer-quantity"},
"clearing_quantity_organization_list": {"list":"markets/dam/data/clearing-quantity-organization-list"},
    })

    information["details"] = {'amount_of_bilateral_contracts': ['startDate', 'endDate', 'function'],
 'bilateral_contracts_bid_quantity': ['organizationId','startDate', 'endDate', 'function'],
 'bilateral_contracts_offer_quantity': ['organizationId', 'startDate', 'endDate', 'function'],
 'clearing_quantity_organization_list': ['period', 'function']}

    information["rename_columns"] = dict(
        PTF="PTF (TL/MWh)",
        SMF="SMF (TL/MWh)",
        )

    
    def __init__(self, root_url, master):
        self.main_url = root_url + "electricity-service/v1/"
        self.master = master
        self.headers = {"TGT":self.master.tgt_response, "Content-Type": "application/json"}


    def amount_of_bilateral_contracts(self, 
                        startDate = get_year(),
                        endDate = get_today(),
                        function = "export"):
        """
        EÜAŞ - GTŞ İkili Anlaşmalar Listeleme Servisi 
        ----------------------
        Düzenlemeye tabi tarife kapsamına göre EÜAŞ ile GTŞ’lerin arasında yapılan ikili anlaşmaların aylık toplamlarını göstermektedir.
        ----------------------
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "amount_of_bilateral_contracts", function)

        check = self.master.control_time_between(url, startDate, endDate)

        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(startDate = startDate,
                    endDate = endDate)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result

    def bilateral_contracts_bid_quantity(self,
                        organizationId,
                        startDate = get_today(),
                        endDate = get_today(),
                        function = "export"):
        """
        İkili Anlaşma (İA) Alış Miktarı Listeleme Servisi 
        ----------------------
        İkili anlaşmalara ait alış miktarları verisidir.
        ----------------------
        organizationId = int
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "bilateral_contracts_bid_quantity", function)

        check = self.master.control_time_between(url, startDate, endDate)

        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(
            organizationId = organizationId,
            startDate = startDate,
            endDate = endDate)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result

    def bilateral_contracts_offer_quantity(self, 
                        organizationId,
                        startDate = get_today(),
                        endDate = get_today(),
                        function = "export"):
        """
        İkili Anlaşma (İA) Satış Miktarı Listeleme Servisi 
        ----------------------
        İkili anlaşmalara ait satış miktarı verisidir.
        ----------------------
        organizationId = int
        startDate = (2023,1,1) default: today
        endDate = (2023,1,1) default: today
        function = list veya export
        """

        url = self.master.get_url(self.main_url, self.information, "bilateral_contracts_offer_quantity", function)

        check = self.master.control_time_between(url, startDate, endDate)

        if check == False:
            return
        else:
            startDate, endDate = check

        data = dict(
            organizationId = organizationId,
            startDate = startDate,
            endDate = endDate)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result

    def clearing_quantity_organization_list(self, 
                        period = get_this_month(),
                        function = "list"):
        """
        İkili Anlaşma Eşleşme Miktarı Organizasyon Listeleme Servisi 
        ----------------------
        İkili Anlaşma Eşleşme Miktarı için organizasyonları listeler.
        ----------------------
        period = (2023,1, 1) default: this month
        function = list
        """


        url = self.master.get_url(self.main_url, self.information, "clearing_quantity_organization_list", function)

        period = self.master.control_time(url, period)

        if period == False:
            return

        data = dict(period = period)
        self.result = self.master.request_data(url, data, function, self.headers, self.information)
        return self.result

