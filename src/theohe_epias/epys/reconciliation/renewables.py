
from pandas import ExcelFile
from ...epys.utils.get_time import get_current_settlement_days, get_last_day_of_month
from ...epys.utils.time_format import tuple_to_datetime, control_times
from json import dumps
from requests import request


class Renewables():
    def request_renewables_data(self, path, payload, octet = False):
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


    def format_files_renewables(self, function):
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



    def luy_invoice(self,
                              settlementPointId:int = None,
                              period:tuple = get_current_settlement_days(first_day = True, finalised = False),
                              version:tuple = get_current_settlement_days(first_day = True, finalised = False),
                              statuses:list = None,
                              region = "TR1",
                              function = "list"):
        """
        #Renewables
        LÜY Fatura İşlemleri
        ---------

        İlgili Sayfa
        ---------
        https://epys.epias.com.tr/reconciliation-operations/resm-operations/upr-amount-operations

        Parametre 
        ---------
         - settlementPointId    : None (Tamamı gelir)
         - period               : (2023,1) (Varsayılan: Güncel KESİNLEŞMEMİŞ (Ayın 6'sından sonra kesinleşmemiş Uzlaştırma çalışır) uzlaştırma dönemi kullanılmaktadır)
         - version              : (2023,1) (Varsayılan: Güncel KESİNLEŞMEMİŞ (Ayın 6'sından sonra kesinleşmemiş Uzlaştırma çalışır) uzlaştırma dönemi kullanılmaktadır)
         - statuses          : None (Tamamı gelir)
         "1": Açık
         "51": Onay Bekleyen
         "101": Onaylı
         "151": GDDK Onay Bekleyen
         "201": GDDK Onaylı
         "251": İptal
         - function             : "list","export" (Varsayılan: "list" | list ile dict formatında, export ile dataframe veya dict olarak dönüş sağlar)
                
        Notlar
        ---------
         - version >= period olmalıdır.
        """

        period= tuple_to_datetime(period)
        if period == False:
            return

        version= tuple_to_datetime(version)
        if version == False:
            return

        if control_times(period, version, equal = True, label = "period") == False:
            return
                    
        if function == "list":
            path = "https://epys{}.epias.com.tr/reconciliation-res/v1/luy-invoice/invoice/list".format(self.test_coef)
        elif function == "export":
            path = "https://epys{}.epias.com.tr/reconciliation-res/v1/luy-invoice/invoice/export".format(self.test_coef)
        else:
            print("Function is not defined")
            return
                    
        self.request_renewables_data(path, {
            "period":period,
            "version":version,
            "statuses":statuses,
            "organization": self.organizationId,
            "settlementPointId":settlementPointId,
            "region": region, 
            "page": {'number': self.page, 'size': 10000}})

        
        if self.final_response != None:
            self.formatted_final_response = self.format_files_renewables(function)
            return self.formatted_final_response


