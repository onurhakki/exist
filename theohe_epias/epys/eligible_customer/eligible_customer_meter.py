
from pandas import ExcelFile
from ...epys.utils.get_time import get_current_settlement_days, get_last_day_of_month
from ...epys.utils.time_format import tuple_to_datetime, control_times
from json import dumps
from requests import request


class EligibleCustomerMeter():
    def request_eligiblecustomermeter_data(self, path, payload, octet = False):
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


    def format_files_eligiblecustomermeter(self, function):
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


    def eligible_customer_meter_data(self,

                        id:int = None,
                        period:tuple = get_current_settlement_days(first_day = True, finalised = False),
                        eic:str = None,
                        mainMeterId:int = None,
                        oizOrganizationId:int = None,
                        portfolioTypeId:int = 3, # None, 1: Portföy, 2: Tenzil, 3: Portföy + Tenzil
                        readingOrganizationId:int = None,
                        reconciliationPeriodDate:int = None,
                        reconciliationVersionTypeId:int = 2, # None, 1: İlk versiyon, 2: Son versiyon
                        serial:str = None,
                        statusId:int = 2, #Durum: 2 Aktif, 3 Pasif
                        uniqueCode:str = None,
                        usageTypeIds:list = [],

                        function = "list"
):
        """
        #Eligible-Customer
        Serbest Tüketici Sayaç Listeleme
        ---------
        Serbest Tüketici sayaçların kayıt detaylarını döner.

        İlgili Sayfa
        ---------
        https://epys.epias.com.tr/eligible-customer-operations/meter-operations

        Parametre 
        ---------
         - id: int = None,
         - period: (2023,1) (Varsayılan: Güncel KESİNLEŞMEMİŞ (Ayın 6'sından sonra kesinleşmemiş Uzlaştırma çalışır) uzlaştırma dönemi kullanılmaktadır)
         - eic:str = None,
         - mainMeterId:int = None,
         - oizOrganizationId:int = None,
         - portfolioTypeId:int = 3, # None, 1: Portföy, 2: Tenzil, 3: Portföy + Tenzil
         - readingOrganizationId:int = None,
         - reconciliationPeriodDate:int = None,
         - reconciliationVersionTypeId:int = 2, # None, 1: İlk versiyon, 2: Son versiyon
         - serial:str = None,
         - statusId:int = 2, #Durum: 2 Aktif, 3 Pasif
         - uniqueCode:str = None,
         - usageTypeIds:list = None
            - usageType => {
                2: Serbest Tüketici (Normal)
                5: Otop. Üretim Tesisi,
                12: Serbest Tüketici (OSB Ana Sayacı),
                14: Ölçüm Noktası,
                }
                
        Notlar
        ---------
         - Girilmedi.
        """


        period= tuple_to_datetime(period)
        if period == False:
            return
        else:
            periodDateStart = period
            periodDateEnd = get_last_day_of_month(period)

        if function == "list":
            path = "https://epys{}.epias.com.tr/grid/v1/meter/query".format(self.test_coef)
        else:
            print("Function is not defined")
            return
                    
        self.request_eligiblecustomermeter_data(path, {

                        "id":id,
                        "eic":eic,
                        "mainMeterId":mainMeterId,
                        "organizationId":self.organizationId,
                        "oizOrganizationId":oizOrganizationId,
                        "periodDateStart": periodDateStart,
                        "periodDateEnd": periodDateEnd,
                        "portfolioTypeId":portfolioTypeId,
                        "readingOrganizationId":readingOrganizationId,
                        "reconciliationPeriodDate":reconciliationPeriodDate,
                        "reconciliationVersionTypeId":reconciliationVersionTypeId,
                        "serial":serial,
                        "statusId":statusId, #Durum: 2 Aktif, 3 Pasif
                        "uniqueCode":uniqueCode,
                        "usageTypeIds":usageTypeIds,



            "page": {'number': self.page, 'size': 10000}})

        
        if self.final_response != None:
            self.formatted_final_response = self.format_files_eligiblecustomermeter(function)
            return self.formatted_final_response


