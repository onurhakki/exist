from pandas import ExcelFile
from timeformat.TimeFormat import TimeFormat
from timeformat.TimeFormatControl import TimeFormatControl


class MOF():
    def format_files_mof(self, function):
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

    
    def reconciliation_mof_organization(self, 
                                        period:tuple = None, 
                                        version:tuple = None, 
                                        function = "list"):
        """
        Dönemlik Organizasyon Piyasa İşletim Ücreti (PİÜ) Detayı
        ---------
        Organizasyonların dönemlik PİÜ'larını döner.

        Parametre 
        ---------
         - period : "2023-01-01T00:00:00+03:00" (Varsayılan: Güncel uzlaştırma periyotu)
         - version: "2023-01-01T00:00:00+03:00" (Varsayılan: Güncel uzlaştırma periyotu)
         - function : "list","export" (Varsayılan: "list" | list ile dict formatında, export ile dataframe veya dict olarak dönüş sağlar)
        
        Notlar
        ---------
         - Aylık periyotlar kullanılmıştır.
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
            path = "https://epys.epias.com.tr/reconciliation-mof/v1/reconciliation/mof/organization/list"
        elif function == "export":
            path = "https://epys.epias.com.tr/reconciliation-mof/v1/reconciliation/mof/organization/export"
        else:
            print("Function is not defined")
            return
        
        self.request_data(path, {"period": period, "version": version,
            "page": {'number': self.page, 'size': 10000}})

                                 
        if self.final_response != None:
            self.formatted_final_response = self.format_files_mof(function)
            return self.formatted_final_response




    def reconciliation_mof_organization_retrospective(self, 
                                        period:tuple = None, 
                                        version:tuple = None, function = "list"):
        """
        (GDDK) Dönemlik Organizasyon Piyasa İşletim Ücreti (PİÜ) Detayı
        ---------
        Organizasyonların GDDK kapsamında dönemlik PİÜ'larını döner.

        Parametre 
        ---------
         - period : "2023-01-01T00:00:00+03:00" (Varsayılan: Güncel uzlaştırma periyotu)
         - version: "2023-01-01T00:00:00+03:00" (Varsayılan: Güncel uzlaştırma periyotu)
         - function : "list","export" (Varsayılan: "list" | list ile dict formatında, export ile dataframe veya dict olarak dönüş sağlar)
        
        Notlar
        ---------
         - Aylık periyotlar kullanılmıştır.
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
            
        if TimeFormatControl.control_order_period_version_higher(period, version) == False:
            return False



        if function == "list":
            path = "https://epys.epias.com.tr/reconciliation-mof/v1/reconciliation/mof/organization/retrospective/list"
        elif function == "export":
            path = "https://epys.epias.com.tr/reconciliation-mof/v1/reconciliation/mof/organization/retrospective/export"
        else:
            print("Function is not defined")
            return
        
        self.request_data(path, {"period": period, "version": version,
            "page": {'number': self.page, 'size': 10000}})

        if self.final_response != None:
            self.formatted_final_response = self.format_files_mof(function)
            return self.formatted_final_response

            