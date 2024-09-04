
from pandas import ExcelFile
from ...epys.utils.get_time import get_current_settlement_days, get_last_day_of_month, get_current_month
from ...epys.utils.time_format import tuple_to_datetime, control_times
from json import dumps
from requests import request


class Advance():
    def request_advance_data(self, path, payload, octet = False):
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


    def format_files_advance(self, function):
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
            result = self.final_response.json()["body"]["content"]["items"]
            return result


    def advance(self,
                DateStart:tuple = get_current_month(first_day = True),
                DateEnd:tuple = get_current_month(first_day = False),
                function = "list"):
        """
        #Market
        Avans Bildirim Detayları
        ---------
        Organizasyonların avans alacak borç detaylarını günlük kırlımda döner.
        
        İlgili Sayfa
        ---------
        https://epys.epias.com.tr/reconciliation-operations/advance-detail

        Parametre 
        ---------
         - DateStart: (2023,1) (Varsayılan: Güncel ay),
         - DateEnd  : (2023,1) (Varsayılan: Güncel ay),
         - function : "list","export" (Varsayılan: "list" | list ile dict formatında, export ile dataframe veya dict olarak dönüş sağlar)
                
        Notlar
        ---------
         - DateEnd > DateStart olmalıdır.
         - Maksimum bir senelik veri çekilebilmektedir.
        """

        DateStart= tuple_to_datetime(DateStart)
        if DateStart == False:
            return

        DateEnd= tuple_to_datetime(DateEnd)
        if DateEnd == False:
            return

        if control_times(DateStart, DateEnd, equal = True, label = "date") == False:
            return
            
        if function == "list":
            path = "https://epys{}.epias.com.tr/reconciliation-market/v1/advance/list".format(self.test_coef)
        elif function == "export":
            path = "https://epys{}.epias.com.tr/reconciliation-market/v1/advance/export".format(self.test_coef)
        else:
            print("Function is not defined")
            return
                    
        self.request_advance_data(path, {
            "paymentDateStart":DateStart,
            "paymentDateEnd":DateEnd,
            "page": {'number': self.page, 'size': 10000}})

        
        if self.final_response != None:
            self.formatted_final_response = self.format_files_advance(function)
            return self.formatted_final_response




