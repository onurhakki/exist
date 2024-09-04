
from pandas import ExcelFile
from ...epys.utils.get_time import get_current_settlement_days, get_last_day_of_month
from ...epys.utils.time_format import tuple_to_datetime, control_times
from json import dumps
from requests import request


class Reports():
    def request_reports_data(self, path, payload, octet = False):
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


    def format_files_reports(self, function):
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

    def settlement_point_data(self,
                              settlementPointId:int = None,
                              period:tuple = get_current_settlement_days(first_day = True, finalised = False),
                              version:tuple = get_current_settlement_days(first_day = True, finalised = False),
                              DateStart:tuple = None,
                              DateEnd:tuple = None,
                              region = "TR1",
                              function = "list"):
        """
        #Precon
        UEVÇB Verileri Listeleme
        ---------
        UEVÇB verilerini döner.

        İlgili Sayfa
        ---------
        https://epys.epias.com.tr/reconciliation-operations/reports/uevcb-data

        Parametre 
        ---------
         - settlementPointId   : None (Tamamı gelir)
         - period   : (2023,1) (Varsayılan: Güncel KESİNLEŞMEMİŞ (Ayın 6'sından sonra kesinleşmemiş Uzlaştırma çalışır) uzlaştırma dönemi kullanılmaktadır)
         - version  : (2023,1) (Varsayılan: Güncel KESİNLEŞMEMİŞ (Ayın 6'sından sonra kesinleşmemiş Uzlaştırma çalışır) uzlaştırma dönemi kullanılmaktadır)
         - DateStart: (2023,1) (Varsayılan: Güncel KESİNLEŞMEMİŞ (Ayın 6'sından sonra kesinleşmemiş Uzlaştırma çalışır) uzlaştırma dönemi kullanılmaktadır)
         - DateEnd  : (2023,1) (Varsayılan: Güncel KESİNLEŞMEMİŞ (Ayın 6'sından sonra kesinleşmemiş Uzlaştırma çalışır) uzlaştırma dönemi kullanılmaktadır)
         - function : "list","export" (Varsayılan: "list" | list ile dict formatında, export ile dataframe veya dict olarak dönüş sağlar)
                
        Notlar
        ---------
         - Eğer DateEnd veya DateStart parametre olarak giriliyorsa, period seçilmelidir. versiyon olarak en güncel dönem gelecektir.
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
            path = "https://epys{}.epias.com.tr/pre-reconciliation/v1/settlement-point/data".format(self.test_coef)
        elif function == "export":
            path = "https://epys{}.epias.com.tr/pre-reconciliation/v1/settlement-point/data/export".format(self.test_coef)
        else:
            print("Function is not defined")
            return
                    
        self.request_reports_data(path, {
            "period":period,
            "version":version,
            "effectiveDateStart":DateStart,
            "effectiveDateEnd":DateEnd,
            "organization": self.organizationId,
            "settlementPointId":settlementPointId,
            "region": region, 
            "page": {'number': self.page, 'size': 10000}})

        
        if self.final_response != None:
            self.formatted_final_response = self.format_files_reports(function)
            return self.formatted_final_response


    def settlement_point_meter_data(self,
                              settlementPointId:int = None,
                              period:tuple = get_current_settlement_days(first_day = True, finalised = False),
                              version:tuple = get_current_settlement_days(first_day = True, finalised = False),
                              isDeduction:bool = False,
                              region = "TR1",
                              function = "list"):
        """
        #Precon
        UEVÇB'ye Bağlı Sayaçların Bilgileri
        ---------
        UEVÇB'ye Bağlı Sayaçların Veriş-Çekiş Değerlerini listesini döner.

        İlgili Sayfa
        ---------
        https://epys.epias.com.tr/reconciliation-operations/reports/uevcb-meter-data

        Parametre 
        ---------
         - settlementPointId    : None (Tamamı gelir)
         - period               : (2023,1) (Varsayılan: Güncel KESİNLEŞMEMİŞ (Ayın 6'sından sonra kesinleşmemiş Uzlaştırma çalışır) uzlaştırma dönemi kullanılmaktadır)
         - version              : (2023,1) (Varsayılan: Güncel KESİNLEŞMEMİŞ (Ayın 6'sından sonra kesinleşmemiş Uzlaştırma çalışır) uzlaştırma dönemi kullanılmaktadır)
         - isDeduction          : Tenzil durumu (False)
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
            path = "https://epys{}.epias.com.tr/pre-reconciliation/v1/settlement-point/meter-data/list".format(self.test_coef)
        elif function == "export":
            path = "https://epys{}.epias.com.tr/pre-reconciliation/v1/settlement-point/meter-data/export".format(self.test_coef)
        else:
            print("Function is not defined")
            return
                    
        self.request_reports_data(path, {
            "period":period,
            "version":version,
            "isDeduction":isDeduction,
            "organization": self.organizationId,
            "settlementPointId":settlementPointId,
            "region": region, 
            "page": {'number': self.page, 'size': 10000}})

        
        if self.final_response != None:
            self.formatted_final_response = self.format_files_reports(function)
            return self.formatted_final_response


    def overproduction_data(self,
                              period:tuple = get_current_settlement_days(first_day = True, finalised = False),
                              version:tuple = get_current_settlement_days(first_day = True, finalised = False),
                              region = "TR1",
                              function = "list"):
        """
        #Precon
        Kırpma Miktarı
        ---------
        Fazla üretim nedeniyle kırpılan üretim verilerini döner.

        İlgili Sayfa
        ---------
        https://epys.epias.com.tr/reconciliation-operations/reports/overproduction-data

        Parametre 
        ---------
         - settlementPointId   : None (Tamamı gelir)
         - period   : (2023,1) (Varsayılan: Güncel KESİNLEŞMEMİŞ (Ayın 6'sından sonra kesinleşmemiş Uzlaştırma çalışır) uzlaştırma dönemi kullanılmaktadır)
         - version  : (2023,1) (Varsayılan: Güncel KESİNLEŞMEMİŞ (Ayın 6'sından sonra kesinleşmemiş Uzlaştırma çalışır) uzlaştırma dönemi kullanılmaktadır)
         - function : "list","export" (Varsayılan: "list" | list ile dict formatında, export ile dataframe veya dict olarak dönüş sağlar)
                
        Notlar
        ---------
         - Eğer DateEnd veya DateStart parametre olarak giriliyorsa, period seçilmelidir. versiyon olarak en güncel dönem gelecektir.
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

        if function == "list":
            path = "https://epys{}.epias.com.tr/pre-reconciliation/v1/settlement-point/overproduction-data/list".format(self.test_coef)
        elif function == "export":
            path = "https://epys{}.epias.com.tr/pre-reconciliation/v1/settlement-point/overproduction-data/export".format(self.test_coef)
        else:
            print("Function is not defined")
            return
                    
        self.request_reports_data(path, {
            "period":period,
            "version":version,
            "region": region, 
            "page": {'number': self.page, 'size': 10000}})

        
        if self.final_response != None:
            self.formatted_final_response = self.format_files_reports(function)
            return self.formatted_final_response

