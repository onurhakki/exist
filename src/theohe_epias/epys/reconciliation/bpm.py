
from pandas import ExcelFile
from ...epys.utils.get_time import get_current_settlement_days, get_last_day_of_month
from ...epys.utils.time_format import tuple_to_datetime, control_times
from json import dumps
from requests import request


class BPM():
    def request_data_bpm(self, path, payload, octet = False):
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


    def format_files_bpm(self, function):
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


    def sbfgp(self,
                             powerPlantId:int = None,
                            settlementPointId:int = None,
                period:tuple = get_current_settlement_days(first_day = True, finalised = False),
                version:tuple = get_current_settlement_days(first_day = True, finalised = False),
                DateStart:tuple = None,
                DateEnd:tuple = None,
                region = "TR1",
                function = "list"):
        """
        #BPM
        KÜPST (Kesinleşmiş Üretim Planından Sapma Tutarı)
        ---------
        KÜPST Detay detaylarını santral ve UEVÇB bazında saatlik kırılımda döner.
        
        İlgili Sayfa
        ---------
        https://epys.epias.com.tr/reconciliation-operations/dgp-operations/kupst-detail

        Parametre 
        ---------
         - powerPlantId        : None (Tamamı gelir)
         - settlementPointId   : None (Tamamı gelir)
         - period   : (2023,1) (Varsayılan: Güncel uzlaştırma periyotu)
         - version  : (2023,1) (Varsayılan: Güncel uzlaştırma periyotu)
         - DateStart: (2023,1,1,0) (Varsayılan: Güncel uzlaştırma periyotu)
         - DateEnd  : (2023,1,31,23) (Varsayılan: Güncel uzlaştırma periyotu)
         - function : "list","export" (Varsayılan: "list" | list ile dict formatında, export ile dataframe veya dict olarak dönüş sağlar)
                
        Notlar
        ---------
         - Aslında birden fazla versiyon beraber görüntülenebilir, fakat bu fonksiyonda elemine edilmiştir.
         - parametre olarak "versions" kullanıldığına dikkat edilmelidir, list kullanılır.
         - version >= period olmalıdır.
         - DateEnd >= DateStart olmalıdır.
         - DateStart >= period olmalıdır.
        """

        period= tuple_to_datetime(period)
        if period == False:
            return

        version= tuple_to_datetime(version)
        if version == False:
            return

        if control_times(period, version, equal = True, label = "period") == False:
            return



        if DateStart == None and DateEnd == None:
            DateStart, DateEnd= period, get_last_day_of_month(period) 

        elif DateStart == None and DateEnd != None:
            DateStart = period
            DateEnd = tuple_to_datetime(DateEnd)
            if DateEnd == False:
                return
        elif DateStart != None and DateEnd == None:
            DateEnd = get_last_day_of_month(period)
            DateStart = tuple_to_datetime(DateStart)
            if DateStart == False:
                return
        else:
            DateStart = tuple_to_datetime(DateStart)
            if DateStart == False:
                return
            DateEnd= tuple_to_datetime(DateEnd)
            if DateEnd == False:
                return


        if control_times(DateStart, DateEnd, equal = True, label = "date") == False:
            return

        if control_times(period, DateStart, equal = True, label = "period-date") == False:
            return


            
        if function == "list":
            path = "https://epys{}.epias.com.tr/reconciliation-bpm/v1/reconciliation/sbfgp".format(self.test_coef)
        elif function == "export":
            path = "https://epys{}.epias.com.tr/reconciliation-bpm/v1/reconciliation/sbfgp/export".format(self.test_coef)
        else:
            print("Function is not defined")
            return
                    
        self.request_data_bpm(path, {
            "powerPlantId": powerPlantId,
            "settlementPointId":settlementPointId,
            "period":period,
            "versions":[version],
            "effectiveDateStart":DateStart,
            "effectiveDateEnd":DateEnd,
            "region": region, 
            "page": {'number': self.page, 'size': 10000}})

        
        if self.final_response != None:
            self.formatted_final_response = self.format_files_bpm(function)
            return self.formatted_final_response


