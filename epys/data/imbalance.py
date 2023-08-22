
from pandas import ExcelFile
from timeformat.TimeFormat import TimeFormat
from timeformat.TimeFormatControl import TimeFormatControl


class Imbalance():
    def format_files_imbalance(self, function):
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
    
    def imbalance(self,
                              period:tuple = None,
                              version:tuple = None,
                              DateStart:tuple = None,
                              DateEnd:tuple = None,
                              region = "TR1",
                              function = "list"):
        """
        Organizasyon Enerji Dengesizlik
        ---------
        Organizasyonların saatlik detayda dengesizlik detaylarını döner. (EPYS ekranlarındaki "Dengesizlik Uzlaştırma" sayfasını döner)

        Parametre 
        ---------
         - period              : "2023-01-01T00:00:00+03:00" (Varsayılan: Güncel uzlaştırma periyotu)
         - version             : "2023-01-01T00:00:00+03:00" (Varsayılan: Güncel uzlaştırma periyotu)
         - DateStart           : "2023-01-01T00:00:00+03:00" (Varsayılan: Güncel uzlaştırma periyotu)
         - DateEnd             : "2023-01-31T23:00:00+03:00" (Varsayılan: Güncel uzlaştırma periyotu)
         - function : "list","export" (Varsayılan: "list" | list ile dict formatında, export ile dataframe veya dict olarak dönüş sağlar)
                
        Notlar
        ---------
         - version >= period olmalıdır.
         - DateEnd >= DateStart olmalıdır.
         - DateStart >= period olmalıdır.

        """

        if period == None:
            period= TimeFormat.current_settlement_date()
        else:
            period= TimeFormat.get_settlement_date(period)
            if period == False:
                return
            
        if version == None:
            version= TimeFormat.current_settlement_date()
        else:
            version= TimeFormat.get_settlement_date(version)
            if version == False:
                return
            
        if TimeFormatControl.control_order_period_version_equal(period, version) == False:
            return False
        
        
        
        if DateStart == None and DateEnd == None:
            DateStart, DateEnd= TimeFormat.get_settlement_date_in_period_hour(period)
        elif DateStart == None and DateEnd != None:
            DateStart, _= TimeFormat.get_settlement_date_in_period_hour(period)
            DateEnd= TimeFormat.get_settlement_date_hour(DateEnd)
            if DateEnd == False:
                return
        elif DateStart != None and DateEnd == None:
            _, DateEnd = TimeFormat.get_settlement_date_in_period_hour(period)
            DateStart = TimeFormat.get_settlement_date_hour(DateStart)
            if DateStart == False:
                return
        else:
            DateStart = TimeFormat.get_settlement_date_hour(DateStart)
            if DateStart == False:
                return
            DateEnd= TimeFormat.get_settlement_date_hour(DateEnd)
            if DateEnd == False:
                return
            
            
        if TimeFormatControl.control_order_dates_equal(DateStart, DateEnd) == False:
            return False

        if TimeFormatControl.control_order_dates_equal_period_date(period, DateStart) == False:
            return False


        if function == "list":
            path = "https://epys.epias.com.tr/reconciliation-imbalance/v1/imbalance/list"
        elif function == "export":
            path = "https://epys.epias.com.tr/reconciliation-imbalance/v1/imbalance/export"
        else:
            print("Function is not defined")
            return
                    
        self.request_data(path, {
            "period":period,
            "version":version,
            "effectiveDateStart":DateStart,
            "effectiveDateEnd":DateEnd,
            "region": region, 
            "page": {'number': self.page, 'size': 10000}})

        
        if self.final_response != None:
            self.formatted_final_response = self.format_files_imbalance(function)
            return self.formatted_final_response


    def imbalance_balance_group_organization_detail(self,
                              period:tuple = None,
                              version:tuple = None,
                              DateStart:tuple = None,
                              DateEnd:tuple = None,
                              region = "TR1",
                              function = "list"):
        """
        DSG Enerji Dengesizlik Detay
        ---------
        Dengeden sorumlu grup üyelerinin enerji dengesizlik bilgilerinin detaylarını döner. (EPYS ekranlarındaki "Dengesizlik Uzlaştırma Detay" sayfasını dışarı aktarıldığında elde edilen excel sayfasındaki verileri döner.)

        Parametre 
        ---------
         - period              : "2023-01-01T00:00:00+03:00" (Varsayılan: Güncel uzlaştırma periyotu)
         - version             : "2023-01-01T00:00:00+03:00" (Varsayılan: Güncel uzlaştırma periyotu)
         - DateStart           : "2023-01-01T00:00:00+03:00" (Varsayılan: Güncel uzlaştırma periyotu)
         - DateEnd             : "2023-01-31T23:00:00+03:00" (Varsayılan: Güncel uzlaştırma periyotu)
         - function : "list","export" (Varsayılan: "list" | list ile dict formatında, export ile dataframe veya dict olarak dönüş sağlar)
                
        Notlar
        ---------
         - version >= period olmalıdır.
         - DateEnd >= DateStart olmalıdır.
         - DateStart >= period olmalıdır.

        """

        if period == None:
            period= TimeFormat.current_settlement_date()
        else:
            period= TimeFormat.get_settlement_date(period)
            if period == False:
                return
            
        if version == None:
            version= TimeFormat.current_settlement_date()
        else:
            version= TimeFormat.get_settlement_date(version)
            if version == False:
                return
            
        if TimeFormatControl.control_order_period_version_equal(period, version) == False:
            return False
        
        
        if DateStart == None and DateEnd == None:
            DateStart, DateEnd= TimeFormat.get_settlement_date_in_period_hour(period)
        elif DateStart == None and DateEnd != None:
            DateStart, _= TimeFormat.get_settlement_date_in_period_hour(period)
            DateEnd= TimeFormat.get_settlement_date_hour(DateEnd)
            if DateEnd == False:
                return
        elif DateStart != None and DateEnd == None:
            _, DateEnd = TimeFormat.get_settlement_date_in_period_hour(period)
            DateStart = TimeFormat.get_settlement_date_hour(DateStart)
            if DateStart == False:
                return
        else:
            DateStart = TimeFormat.get_settlement_date_hour(DateStart)
            if DateStart == False:
                return
            DateEnd= TimeFormat.get_settlement_date_hour(DateEnd)
            if DateEnd == False:
                return
            
        if TimeFormatControl.control_order_dates_equal(DateStart, DateEnd) == False:
            return False

        if TimeFormatControl.control_order_dates_equal_period_date(period, DateStart) == False:
            return False


        if function == "list":
            path = "https://epys.epias.com.tr/reconciliation-imbalance/v1/imbalance/balance-group-organization/detail/list"
        elif function == "export":
            path = "https://epys.epias.com.tr/reconciliation-imbalance/v1/imbalance/balance-group-organization/detail/export"
        else:
            print("Function is not defined")
            return
                    
        self.request_data(path, {
            "period":period,
            "version":version,
            "effectiveDateStart":DateStart,
            "effectiveDateEnd":DateEnd,
            "region": region, 
            "page": {'number': self.page, 'size': 10000}})

        
        if self.final_response != None:
            self.formatted_final_response = self.format_files_imbalance(function)
            return self.formatted_final_response



    def imbalance_balance_group_organization_detail_monthly(self,
                                                            period:tuple = None,
                                                            version:tuple = None,
                                                            region = "TR1",
                                                            function = "list"):
        """
        DSG Enerji Dengesizlik Aylık Detay
        ---------
        Dengeden sorumlu grup üyelerinin aylık enerji dengesizlik bilgilerinin detaylarını döner. 
        (
            list: EPYS ekranlarındaki "Dengesizlik Uzlaştırma Detay" sayfasınındaki verileri döner.
            export: EPYS ekranlarındaki "Dengesizlik Uzlaştırma Detay" sayfasını dışarı aktarıldığında elde edilen excel sayfasındaki verileri döner.
        )

        Parametre 
        ---------
         - period              : "2023-01-01T00:00:00+03:00" (Varsayılan: Güncel uzlaştırma periyotu)
         - version             : "2023-01-01T00:00:00+03:00" (Varsayılan: Güncel uzlaştırma periyotu)
         - function : "list","export" (Varsayılan: "list" | list ile dict formatında, export ile dataframe veya dict olarak dönüş sağlar)
                
        Notlar
        ---------
         - version >= period olmalıdır.

        """

        if period == None:
            period= TimeFormat.current_settlement_date()
        else:
            period= TimeFormat.get_settlement_date(period)
            if period == False:
                return
            
        if version == None:
            version= TimeFormat.current_settlement_date()
        else:
            version= TimeFormat.get_settlement_date(version)
            if version == False:
                return
            
        if TimeFormatControl.control_order_period_version_equal(period, version) == False:
            return False
        
        
        if function == "list":
            path = "https://epys.epias.com.tr/reconciliation-imbalance/v1/imbalance/balance-group-organization/detail/monthly/list"
        elif function == "export":
            path = "https://epys.epias.com.tr/reconciliation-imbalance/v1/imbalance/balance-group-organization/detail/monthly/export"
        else:
            print("Function is not defined")
            return
                    
        self.request_data(path, {
            "period":period,
            "version":version,
            "region": region, 
            "page": {'number': self.page, 'size': 10000}})

        
        if self.final_response != None:
            self.formatted_final_response = self.format_files_imbalance(function)
            return self.formatted_final_response


    def retrospective_imbalance_balance_group_organization_detail(self,
                              period:tuple = None,
                              version:tuple = None,
                              DateStart:tuple = None,
                              DateEnd:tuple = None,
                              region = "TR1",
                              function = "list"):
        """
        DSG GDDK Enerji Dengesizlik Detay
        ---------
        DSG üyelerinin aylık GDDK değişimlerine ait dengesizlik bilgilerinin detaylarını döner.

        Parametre 
        ---------
         - period              : "2023-01-01T00:00:00+03:00" (Varsayılan: Güncel uzlaştırma periyotu)
         - version             : "2023-01-01T00:00:00+03:00" (Varsayılan: Güncel uzlaştırma periyotu)
         - DateStart           : "2023-01-01T00:00:00+03:00" (Varsayılan: Güncel uzlaştırma periyotu)
         - DateEnd             : "2023-01-31T23:00:00+03:00" (Varsayılan: Güncel uzlaştırma periyotu)
         - function : "list","export" (Varsayılan: "list" | list ile dict formatında, export ile dataframe veya dict olarak dönüş sağlar)
                
        Notlar
        ---------
         - version >= period olmalıdır.
         - DateEnd >= DateStart olmalıdır.
         - DateStart >= period olmalıdır.

        """

        if period == None:
            period= TimeFormat.current_settlement_date()
        else:
            period= TimeFormat.get_settlement_date(period)
            if period == False:
                return
            
        if version == None:
            version= TimeFormat.current_settlement_date()
        else:
            version= TimeFormat.get_settlement_date(version)
            if version == False:
                return
            
        if TimeFormatControl.control_order_period_version_higher(period, version) == False:
            return False
        
        
        if DateStart == None and DateEnd == None:
            DateStart, DateEnd= TimeFormat.get_settlement_date_in_period_hour(period)
        elif DateStart == None and DateEnd != None:
            DateStart, _= TimeFormat.get_settlement_date_in_period_hour(period)
            DateEnd= TimeFormat.get_settlement_date_hour(DateEnd)
            if DateEnd == False:
                return
        elif DateStart != None and DateEnd == None:
            _, DateEnd = TimeFormat.get_settlement_date_in_period_hour(period)
            DateStart = TimeFormat.get_settlement_date_hour(DateStart)
            if DateStart == False:
                return
        else:
            DateStart = TimeFormat.get_settlement_date_hour(DateStart)
            if DateStart == False:
                return
            DateEnd= TimeFormat.get_settlement_date_hour(DateEnd)
            if DateEnd == False:
                return
            
        if TimeFormatControl.control_order_dates_equal(DateStart, DateEnd) == False:
            return False

        if TimeFormatControl.control_order_dates_equal_period_date(period, DateStart) == False:
            return False


        if function == "list":
            path = "https://epys.epias.com.tr/reconciliation-imbalance/v1/retrospective-imbalance/list-balance-group-detail"
        elif function == "export":
            path = "https://epys.epias.com.tr/reconciliation-imbalance/v1/retrospective-imbalance/list-balance-group-detail/export"
        else:
            print("Function is not defined")
            return
                    
        self.request_data(path, {
            "period":period,
            "version":version,
            "effectiveDateStart":DateStart,
            "effectiveDateEnd":DateEnd,
            "region": region, 
            "page": {'number': self.page, 'size': 10000}})

        
        if self.final_response != None:
            self.formatted_final_response = self.format_files_imbalance(function)
            return self.formatted_final_response
