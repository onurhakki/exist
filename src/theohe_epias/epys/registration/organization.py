
from pandas import ExcelFile
from ...epys.utils.get_time import get_current_settlement_days, get_last_day_of_month
from ...epys.utils.time_format import tuple_to_datetime, control_times
from json import dumps
from requests import request


class Organization():
    def request_organization(self, path, payload, octet = False):
        if octet == False:
            service_header ={
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                "TGT": self.tgt_response}
        else:
            service_header ={
                'Content-Type': 'application/json',
                'Accept': 'application/octet-stream',
                "TGT": self.tgt_response}

        if self.organizationId != None:
            if self.organizationId != 2:
                service_header["mockedOrganizationId"] = str(self.organizationId)
            payload = dumps(payload)
            final_response = request(
                "POST", path, headers=service_header, data=payload, 
            )
            
            if self.check_response(final_response):
                self.final_response = final_response
            else:
                self.final_response = None

        else:
            print("No valid Org ID")
            self.final_response = None


    def format_files_organization(self, function):
        if function == "export":
            res = ExcelFile(self.final_response.content)
            sheet_names = res.sheet_names
            if len(sheet_names) == 0:
                print("There are no sheets.")
                return 
            elif len(sheet_names) == 1:
                return res.parse(sheet_names[0])
            elif len(sheet_names) > 1:
                print("There are more then one sheet.")
                result = dict()
                for sheet in res.sheet_names:
                    print(sheet)
                    result[sheet] = res.parse(sheet)
            return result
        
        elif function == "list":
            result = self.final_response.json()["body"]["content"]
            return result


    def registration_organization(self,
                        name:str = None,
                        effectiveDate:tuple = None,
                        # effectiveDateStart:tuple = None,
                        # effectiveDateEnd:tuple = None,
                        statusIds:int = [2], #Durum: 2 Aktif, 3 Pasif
                        licenseTypeIds:list = [],
                        isCategory:int = None,
                        typeIds:list = [],
                        mainOrganizationId:int = None,
                        recordStatusIds:list = [],
                        subTypeIds:list = [],
                        taxNo:str = None, 
                        function = "list"
                        

):
        """
        #Registration
        Organizasyon Listeleme
        ---------
        Organizasyonların kayıt detaylarını döner.

        İlgili Sayfa
        ---------
        https://epys.epias.com.tr/registration-operations/organization-operations/organization-list

        Parametre 
        ---------
         - Eklenmedi. 
        """

        if effectiveDate != None:
            effectiveDate= tuple_to_datetime(effectiveDate)
            if effectiveDate == False:
                return

        # if effectiveDateStart != None:
        #     effectiveDateStart= tuple_to_datetime(effectiveDateStart)
        #     if effectiveDateStart == False:
        #         return

        # if effectiveDateEnd != None:
        #     effectiveDateEnd= tuple_to_datetime(effectiveDateEnd)
        #     if effectiveDateEnd == False:
        #         return

            
        if function == "list":
            path = "https://epys{}.epias.com.tr/registration/v1/organization/query".format(self.test_coef)
        else:
            print("Function is not defined")
            return
                    
        self.request_organization(path, {
                        "name":name,
                        "effectiveDate":effectiveDate,
                        # "effectiveDateStart":effectiveDateStart,
                        # "effectiveDateEnd":effectiveDateEnd,
                        "statusIds":statusIds,
                        "licenseTypeIds":licenseTypeIds,
                        "isCategory":isCategory,
                        "typeIds":typeIds,
                        "mainOrganizationId":mainOrganizationId,
                        "recordStatusIds":recordStatusIds,
                        "subTypeIds":subTypeIds,
                        "taxNo": taxNo,
            "page": {'number': self.page, 'size': 10000}})

        
        if self.final_response != None:
            self.formatted_final_response = self.format_files_organization(function)
            return self.formatted_final_response



    def registration_brp_organization(self,
                        period:tuple = None,
                        brgParticipant:int = None,
                        brgOwner:int = None,
                        statusIds:int = [0], #Durum: 0 Aktif, 1 Gruptan Çıkmış, 2 Gruptan çıkarılmış
                        function = "list"

):
        """
        #Registration
        BRP Listeleme
        ---------
        Organizasyonların kayıt detaylarını döner.

        İlgili Sayfa
        ---------
        https://epys.epias.com.tr/registration-operations/brg-operations/brg-operations

        Parametre 
        ---------
         - Eklenmedi. 
        """

        if period != None:
            period= tuple_to_datetime(period)
            if period == False:
                return
            
        if function == "list":
            path = "https://epys{}.epias.com.tr/balancing-group/v1/brg/query".format(self.test_coef)
        else:
            print("Function is not defined")
            return
                    
        self.request_organization(path, {
                        "period":period,
                        "brgParticipant":brgParticipant,
                        "brgOwner":brgOwner,
                        "statusIds":statusIds,
            "page": {'number': self.page, 'size': 10000}})

        
        if self.final_response != None:
            self.formatted_final_response = self.format_files_organization(function)
            return self.formatted_final_response



