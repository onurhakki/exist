
from pandas import ExcelFile
from timeformat.TimeFormat import TimeFormat
from timeformat.TimeFormatControl import TimeFormatControl


class Bpm():
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
            result = self.final_response.json()["body"]["content"]["items"]
            return result
    
    def format_files_smp(self):
        result = self.final_response.json()["body"]["content"]
        return result

    def aic(self,
            powerPlantId:int = None,
            settlementPointId:int = None,
            DateStart:tuple = None,
            DateEnd:tuple = None,
            region = "TR1",
            function = "list"):
        """
        #BPM
        EAK (Emre Amade Kapasite)
        ---------
        Saatlik kırılımda EAK listesini döner.

        İlgili Sayfa
        ---------
        https://epys.epias.com.tr/reconciliation-operations/dgp-operations/ac-list

        Parametre 
        ---------
         - powerPlantId        : None (Tamamı gelir)
         - settlementPointId   : None (Tamamı gelir)
         - DateStart: (2023,1,1,0) (Varsayılan: Güncel uzlaştırma periyotu)
         - DateEnd  : (2023,1,31,23) (Varsayılan: Güncel uzlaştırma periyotu)
         - function : "list","export" (Varsayılan: "list" | list ile dict formatında, export ile dataframe veya dict olarak dönüş sağlar)
                
        Notlar
        ---------
         - DateEnd >= DateStart olmalıdır.
         - powerPlantId None ise settlementPointId None kabul edilir.

        """        
        
        if DateStart == None:
            DateStart= TimeFormat.current_settlement_date_start()
        else:
            DateStart= TimeFormat.get_settlement_date_hour(DateStart)
            if DateStart == False:
                return
            
        if DateEnd == None:
            DateEnd= TimeFormat.current_settlement_date_end()
        else:
            DateEnd= TimeFormat.get_settlement_date_hour(DateEnd)
            if DateEnd == False:
                return
            
        if TimeFormatControl.control_order_dates_equal(DateStart, DateEnd) == False:
            return False
            
        
        if powerPlantId == None:
            settlementPointId == None
        

        if function == "list":
            path = "https://epys.epias.com.tr/reconciliation-bpm/v1/aic/list"
        elif function == "export":
            path = "https://epys.epias.com.tr/reconciliation-bpm/v1/aic/export"
        else:
            print("Function is not defined")
            return
                    
        self.request_data(path, {
            "effectiveDateStart":DateStart,
            "effectiveDateEnd":DateEnd,
            "powerPlantId": powerPlantId,
            "settlementPointId":settlementPointId,
            "region": region, 
            "page": {'number': self.page, 'size': 10000}})

        
        if self.final_response != None:
            self.formatted_final_response = self.format_files_bpm(function)
            return self.formatted_final_response


    def fddp(self,
            powerPlantId:int = None,
            settlementPointId:int = None,
            DateStart:tuple = None,
            DateEnd:tuple = None,
            region = "TR1",
            function = "list"):
        """
        #BPM
        KGÜP (Kesinleşmiş Gün Öncesi Üretim/Tüketim Programı)
        ---------
        Saatlik kırılımda KGÜP listesini döner.

        İlgili Sayfa
        ---------
        https://epys.epias.com.tr/reconciliation-operations/dgp-operations/fdgs-list

        Parametre 
        ---------
         - powerPlantId        : None (Tamamı gelir)
         - settlementPointId   : None (Tamamı gelir)
         - DateStart: (2023,1,1,0) (Varsayılan: Güncel uzlaştırma periyotu)
         - DateEnd  : (2023,1,31,23) (Varsayılan: Güncel uzlaştırma periyotu)
         - function : "list","export" (Varsayılan: "list" | list ile dict formatında, export ile dataframe veya dict olarak dönüş sağlar)
                
        Notlar
        ---------
         - DateEnd >= DateStart olmalıdır.
         - powerPlantId None ise settlementPointId None kabul edilir.

        """        
        
        if DateStart == None:
            DateStart= TimeFormat.current_settlement_date_start()
        else:
            DateStart= TimeFormat.get_settlement_date_hour(DateStart)
            if DateStart == False:
                return
            
        if DateEnd == None:
            DateEnd= TimeFormat.current_settlement_date_end()
        else:
            DateEnd= TimeFormat.get_settlement_date_hour(DateEnd)
            if DateEnd == False:
                return
            
        if TimeFormatControl.control_order_dates_equal(DateStart, DateEnd) == False:
            return False
            
            
        if powerPlantId == None:
            settlementPointId == None
        

        if function == "list":
            path = "https://epys.epias.com.tr/reconciliation-bpm/v1/fddp/list"
        elif function == "export":
            path = "https://epys.epias.com.tr/reconciliation-bpm/v1/fddp/export"
        else:
            print("Function is not defined")
            return
                    
        self.request_data(path, {
            "effectiveDateStart":DateStart,
            "effectiveDateEnd":DateEnd,
            "powerPlantId": powerPlantId,
            "settlementPointId":settlementPointId,
            "region": region, 
            "page": {'number': self.page, 'size': 10000}})

        
        if self.final_response != None:
            self.formatted_final_response = self.format_files_bpm(function)
            return self.formatted_final_response



    def instruction(self,
            powerPlantId:int = None,
            settlementPointId:int = None,
            DateStart:tuple = None,
            DateEnd:tuple = None,
            region = "TR1",
            function = "list"):
        """
        #BPM
        DGP Talimatları
        ---------
        Saatlik kırılımda DGP Talimatlarının listesini döner.
        
        İlgili Sayfa
        ---------
        https://epys.epias.com.tr/reconciliation-operations/dgp-operations/instruction-list


        Parametre 
        ---------
         - powerPlantId        : None (Tamamı gelir)
         - settlementPointId   : None (Tamamı gelir)
         - DateStart: (2023,1,1,0) (Varsayılan: Güncel uzlaştırma periyotu)
         - DateEnd  : (2023,1,31,23) (Varsayılan: Güncel uzlaştırma periyotu)
         - function : "list","export" (Varsayılan: "list" | list ile dict formatında, export ile dataframe veya dict olarak dönüş sağlar)
                
        Notlar
        ---------
         - DateEnd >= DateStart olmalıdır.
         - powerPlantId None ise settlementPointId None kabul edilir.

        """        
        
        if DateStart == None:
            DateStart= TimeFormat.current_settlement_date_start()
        else:
            DateStart= TimeFormat.get_settlement_date_hour(DateStart)
            if DateStart == False:
                return
            
        if DateEnd == None:
            DateEnd= TimeFormat.current_settlement_date_end()
        else:
            DateEnd= TimeFormat.get_settlement_date_hour(DateEnd)
            if DateEnd == False:
                return
            
        if TimeFormatControl.control_order_dates_equal(DateStart, DateEnd) == False:
            return False
            
            
        if powerPlantId == None:
            settlementPointId == None
        

        if function == "list":
            path = "https://epys.epias.com.tr/reconciliation-bpm/v1/instruction/list"
        elif function == "export":
            path = "https://epys.epias.com.tr/reconciliation-bpm/v1/instruction/list/export"
        else:
            print("Function is not defined")
            return
                    
        self.request_data(path, {
            "effectiveDateStart":DateStart,
            "effectiveDateEnd":DateEnd,
            "powerPlantId": powerPlantId,
            "settlementPointId":settlementPointId,
            "region": region, 
            "page": {'number': self.page, 'size': 10000}})

        
        if self.final_response != None:
            self.formatted_final_response = self.format_files_bpm(function)
            return self.formatted_final_response





    def reconciliation_detail(self,
                                powerPlantId:int = None,
                                settlementPointId:int = None,
                                period:tuple = None,
                                version:tuple = None,
                                DateStart:tuple = None,
                                DateEnd:tuple = None,
                                region = "TR1",
                                function = "list"):
        
        """
        #BPM
        DGP Uzlaştırma Detay
        ---------
        DGP Uzlaştırma detaylarını santral ve UEVÇB bazında saatlik kırılımda döner.
        (DGP Uzlaştırma Detay Sayfası)

        İlgili Sayfa
        ---------
        https://epys.epias.com.tr/reconciliation-operations/dgp-operations/bpm-settlement-detail

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
            path = "https://epys.epias.com.tr/reconciliation-bpm/v1/reconciliation/detail/list"
        elif function == "export":
            path = "https://epys.epias.com.tr/reconciliation-bpm/v1/reconciliation/detail/export"
        else:
            print("Function is not defined")
            return
                    
        self.request_data(path, {
            "period":period,
            "versions":[version],
            "effectiveDateStart":DateStart,
            "effectiveDateEnd":DateEnd,
            "powerPlantId": powerPlantId,
            "settlementPointId":settlementPointId,
            "region": region, 
            "page": {'number': self.page, 'size': 10000}})

        
        if self.final_response != None:
            self.formatted_final_response = self.format_files_precon(function)
            return self.formatted_final_response


    def reconciliation_instruction_undeliverable(self,
                                                powerPlantId:int = None,
                                                settlementPointId:int = None,
                                                period:tuple = None,
                                                version:tuple = None,
                                                DateStart:tuple = None,
                                                DateEnd:tuple = None,
                                                region = "TR1",
                                                function = "list"):
        
        """
        #BPM
        Yerine Getirilmeyen Talimat Detay
        ---------
        Yerine Getirilmeyen Talimat detaylarını saatlik kırılımda döner.

        İlgili Sayfa
        ---------
        https://epys.epias.com.tr/reconciliation-operations/dgp-operations/unfulfilled-instruction-list

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
            path = "https://epys.epias.com.tr/reconciliation-bpm/v1/reconciliation/instruction/undeliverable"
        elif function == "export":
            path = "https://epys.epias.com.tr/reconciliation-bpm/v1/reconciliation/instruction/undeliverable/export"
        else:
            print("Function is not defined")
            return
                    
        self.request_data(path, {
            "period":period,
            "versions":[version],
            "effectiveDateStart":DateStart,
            "effectiveDateEnd":DateEnd,
            "powerPlantId": powerPlantId,
            "settlementPointId":settlementPointId,
            "region": region, 
            "page": {'number': self.page, 'size': 10000}})

        
        if self.final_response != None:
            self.formatted_final_response = self.format_files_precon(function)
            return self.formatted_final_response




    def reconciliation_organization(self,
                                    period:tuple = None,
                                    version:tuple = None,
                                    DateStart:tuple = None,
                                    DateEnd:tuple = None,
                                    region = "TR1",
                                    function = "list"):
        
        """
        #BPM
        DGP Uzlaştırma
        ---------
        Organizasyona ait DGP Uzlaştırmasını saatlik kırılımda döner.

        İlgili Sayfa
        ---------
        https://epys.epias.com.tr/reconciliation-operations/dgp-operations/bpm-settlement

        Parametre 
        ---------
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
            path = "https://epys.epias.com.tr/reconciliation-bpm/v1/reconciliation/organization/list"
        elif function == "export":
            path = "https://epys.epias.com.tr/reconciliation-bpm/v1/reconciliation/organization/export"
        else:
            print("Function is not defined")
            return
                    
        self.request_data(path, {
            "period":period,
            "versions":[version],
            "effectiveDateStart":DateStart,
            "effectiveDateEnd":DateEnd,
            "region": region, 
            "page": {'number': self.page, 'size': 10000}})

        
        if self.final_response != None:
            self.formatted_final_response = self.format_files_precon(function)
            return self.formatted_final_response





    def reconciliation_sbfgp(self,
                             powerPlantId:int = None,
                            settlementPointId:int = None,
                            period:tuple = None,
                            version:tuple = None,
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
            path = "https://epys.epias.com.tr/reconciliation-bpm/v1/reconciliation/sbfgp"
        elif function == "export":
            path = "https://epys.epias.com.tr/reconciliation-bpm/v1/reconciliation/sbfgp/export"
        else:
            print("Function is not defined")
            return
                    
        self.request_data(path, {
            "period":period,
            "versions":[version],
            "effectiveDateStart":DateStart,
            "effectiveDateEnd":DateEnd,
            "powerPlantId": powerPlantId,
            "settlementPointId":settlementPointId,
            "region": region, 
            "page": {'number': self.page, 'size': 10000}})

        
        if self.final_response != None:
            self.formatted_final_response = self.format_files_precon(function)
            return self.formatted_final_response


    def reconciliation_retrospective_bpm(self,
                                         powerPlantId:int = None,
                                        settlementPointId:int = None,
                                        period:tuple = None,
                                        version:tuple = None,
                                        DateStart:tuple = None,
                                        DateEnd:tuple = None,
                                        region = "TR1",
                                        function = "list"):
        
        """
        #BPM
        #GDDK
        DGP GDDK
        ---------
        DGP GDDK detaylarının listesini döner.

        İlgili Sayfa
        ---------
        https://epys.epias.com.tr/reconciliation-operations/retro-operations/bpm-retro

        Parametre 
        ---------
         - powerPlantId        : None (Tamamı gelir)
         - settlementPointId   : None (Tamamı gelir)
         - period   : (2023,1) (Varsayılan: Güncel uzlaştırma periyotu)
         - version  : (2023,2) (Varsayılan: Güncel uzlaştırma periyotu)
         - DateStart: (2023,1,1,0) (Varsayılan: Güncel uzlaştırma periyotu)
         - DateEnd  : (2023,1,31,23) (Varsayılan: Güncel uzlaştırma periyotu)
         - function : "list","export" (Varsayılan: "list" | list ile dict formatında, export ile dataframe veya dict olarak dönüş sağlar)
                
        Notlar
        ---------
         - version > period olmalıdır.
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
            path = "https://epys.epias.com.tr/reconciliation-bpm/v1/reconciliation/retrospective/bpm/list"
        elif function == "export":
            path = "https://epys.epias.com.tr/reconciliation-bpm/v1/reconciliation/retrospective/bpm/list/export"
        else:
            print("Function is not defined")
            return
                    
        self.request_data(path, {
            "period":period,
            "version":version,
            "effectiveDateStart":DateStart,
            "effectiveDateEnd":DateEnd,
            "powerPlantId": powerPlantId,
            "settlementPointId":settlementPointId,
            "region": region, 
            "page": {'number': self.page, 'size': 10000}})

        
        if self.final_response != None:
            self.formatted_final_response = self.format_files_precon(function)
            return self.formatted_final_response


    def reconciliation_retrospective_sbfgp(self,
                                           powerPlantId:int = None,
                                            settlementPointId:int = None,
                                            period:tuple = None,
                                            version:tuple = None,
                                            DateStart:tuple = None,
                                            DateEnd:tuple = None,
                                            region = "TR1",
                                            function = "list"):
        
        """
        #BPM
        #GDDK
        KUPST GDDK
        ---------
        KUPST GDDK detaylarının listesini döner.

        İlgili Sayfa
        ---------
        https://epys.epias.com.tr/reconciliation-operations/retro-operations/kupst-retro

        Parametre 
        ---------
         - powerPlantId        : None (Tamamı gelir)
         - settlementPointId   : None (Tamamı gelir)
         - period   : (2023,1) (Varsayılan: Güncel uzlaştırma periyotu)
         - version  : (2023,2) (Varsayılan: Güncel uzlaştırma periyotu)
         - DateStart: (2023,1,1,0) (Varsayılan: Güncel uzlaştırma periyotu)
         - DateEnd  : (2023,1,31,23) (Varsayılan: Güncel uzlaştırma periyotu)
         - function : "list","export" (Varsayılan: "list" | list ile dict formatında, export ile dataframe veya dict olarak dönüş sağlar)
                
        Notlar
        ---------
         - version > period olmalıdır.
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
            path = "https://epys.epias.com.tr/reconciliation-bpm/v1/reconciliation/retrospective/sbfgp"
        elif function == "export":
            path = "https://epys.epias.com.tr/reconciliation-bpm/v1/reconciliation/retrospective/sbfgp/export"
        else:
            print("Function is not defined")
            return
                    
        self.request_data(path, {
            "period":period,
            "version":version,
            "effectiveDateStart":DateStart,
            "effectiveDateEnd":DateEnd,
            "powerPlantId": powerPlantId,
            "settlementPointId":settlementPointId,
            "region": region, 
            "page": {'number': self.page, 'size': 10000}})

        
        if self.final_response != None:
            self.formatted_final_response = self.format_files_precon(function)
            return self.formatted_final_response





    def smp(self,
            DateStart:tuple = None,
            DateEnd:tuple = None, 
            function = "list"):
        """
        #BPM
        SMF (Sistem Marjinal Fiyatı)
        ---------
        Saatlik kırılımda SMF bilgilerini döner.

        İlgili Sayfa
        ---------
        Yok.

        Parametre 
        ---------
         - DateStart: (2023,1,1,0) (Varsayılan: Güncel uzlaştırma periyotu)
         - DateEnd  : (2023,1,31,23) (Varsayılan: Güncel uzlaştırma periyotu)
         - function: "list" (Varsayılan: "list" | list ile dict formatında dönüş sağlar)
        
        Notlar
        ---------
         - Enerjinin teslim edilme tarihleri kullanılmıştır.
         - DateEnd > DateStart olmalıdır.
         - Maksimum bir senelik veri çekilebilmektedir.
        """

        if DateStart == None:
            DateStart= TimeFormat.current_settlement_date_start()
        else:
            DateStart= TimeFormat.get_settlement_date_hour(DateStart)
            if DateStart == False:
                return
            
        if DateEnd == None:
            DateEnd= TimeFormat.current_settlement_date_end()
        else:
            DateEnd= TimeFormat.get_settlement_date_hour(DateEnd)
            if DateEnd == False:
                return
            
        if TimeFormatControl.control_order_dates_equal(DateStart, DateEnd) == False:
            return False


        if function == "list":
            path = "https://epys.epias.com.tr/reconciliation-bpm/v1/smp/list"
        else:
            print("Function is not defined")
            return
                                        
        self.request_data(path, {
            "effectiveDateStart": DateStart,
            "effectiveDateEnd": DateEnd,
            "page": {'number': self.page, 'size': 10000}})

        
        if self.final_response != None:
            self.formatted_final_response = self.format_files_smp()
            return self.formatted_final_response


