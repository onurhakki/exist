
from pandas import ExcelFile
from timeformat.TimeFormat import TimeFormat
from timeformat.TimeFormatControl import TimeFormatControl


class Precon():
    def format_files_precon(self, function):
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
    
    def format_files_meter_data_total(self):
        result = self.final_response.json()["body"]["content"]
        return result


    def meter_data_approved_meter_data(self,
                       period:tuple = None,
                       version:tuple = None, 
                       meterIds:list = [],
                       readStatus=True,
                       isRetrospective = False,
                       meterReadingCompany:int = None,
                       meterReadingType:str = None,
                       usageType:str = None,
                       region="TR1",
                       function = "list"):
        """
        Onaylı Sayaç Verisi
        ---------
        Onaylı sayaçların sayaç okunma durumlarına göre verilerini döner.

        Parametre 
        ---------
         - period              : "2023-01-01T00:00:00+03:00" (Varsayılan: Güncel uzlaştırma periyotu)
         - version             : "2023-01-01T00:00:00+03:00" (Varsayılan: Güncel uzlaştırma periyotu)
         - meterIds            : [] (Varsayılan: None - Hepsi Gelir)
         - readStatus          : True (Varsayılan: True - Okunmuşlar gelir)
         - isRetrospective     : False (Varsayılan: False - Hepsi Gelir)
         - meterReadingCompany : 650 (Varsayılan None - Hepsi Gelir)
            - meterReadingCompany => {650: 2. Bölge Müdürlüğü - İletim}
         - meterReadingType    : "HOURLY", "THREE_PHASE", "SINGLE_PHASE" (Varsayılan None - Hepsi Gelir)
         - usageType           : 3 (Varsayılan None - Hepsi Gelir)
            - usageType => {
                1: Trafo Merkezi,
                2: Serbest Tüketici (Normal)
                3: Serbest Tüketici (Talep Birleştirme)
                4: Üretim Şirketi,
                5: Otop. Üretim Tesisi,
                6: Otop. Tüketim Tesisi,
                8: Tüketim Sayacı,
                9: Teiaş İç İhtiyaç,
                10: İthalat-İhracat}
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
            
        if isRetrospective == False:
            if version == None:
                version= TimeFormat.current_settlement_date()
            else:
                version= TimeFormat.get_settlement_date(version)
                if version == False:
                    return

        if isRetrospective == False:
            if TimeFormatControl.control_order_period_version_equal(period, version) == False:
                return False


        if function == "list":
            path = "https://epys.epias.com.tr/pre-reconciliation/v1/meter-data/approved-meter-data/list"
        elif function == "export":
            path = "https://epys.epias.com.tr/pre-reconciliation/v1/meter-data/approved-meter-data/export"
        else:
            print("Function is not defined")
            return
                    
        self.request_data(path, {
            "period":period,
            "version":version,
            "organization": self.organizationId,
            "meterIds":meterIds,
            "readStatus":readStatus,
            "isRetrospective" : isRetrospective,
            "meterReadingCompany":meterReadingCompany,
            "meterReadingType":meterReadingType,
            "usageType":usageType,
            "region":region,
            "page": {'number': self.page, 'size': 10000}})

        
        if self.final_response != None:
            self.formatted_final_response = self.format_files_precon(function)
            return self.formatted_final_response



    def meter_data_approved_meter_data_period(self,
                                              meterId:int,
                                              period:tuple = None,
                                              version:tuple = None,
                                              function = "list"):
        """
        Saatlik Sayaç Verileri
        ---------
        Sisteme yüklenen saatlik sayaçların verilerini döner.

        Parametre 
        ---------
         - meterId             : (Zorunlu)
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
            path = "https://epys.epias.com.tr/pre-reconciliation/v1/meter-data/approved-meter-data/hourly/get"
        elif function == "export":
            path = "https://epys.epias.com.tr/pre-reconciliation/v1/meter-data/approved-meter-data/hourly/export"
        else:
            print("Function is not defined")
            return
                    
        self.request_data(path, {
            "period":period,
            "version":version,
            "organization": self.organizationId,
            "meterId":meterId,
            "page": {'number': self.page, 'size': 10000}})

        
        if self.final_response != None:
            self.formatted_final_response = self.format_files_precon(function)
            return self.formatted_final_response



    def meter_data_approved_meter_data_hourly(self,
                                              DateStart:tuple = None,
                                              DateEnd:tuple = None,
                                              function = "list"):
        """
        Saatlik Sayaç Verileri Detay
        ---------
        Sisteme yüklenen saatlik sayaçların verilerinin tamamını saatlik kırılımda döner.

        Parametre 
        ---------
         - DateStart           : "2023-01-01T00:00:00+03:00" (Varsayılan: Güncel uzlaştırma periyotu)
         - DateEnd             : "2023-01-31T23:00:00+03:00" (Varsayılan: Güncel uzlaştırma periyotu)
         - function : "list","export" (Varsayılan: "list" | list ile dict formatında dönüş sağlar)
                
        Notlar
        ---------
         - DateEnd >= DateStart olmalıdır.

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
            path = "https://epys.epias.com.tr/pre-reconciliation/v1/meter-data/approved-meter-data/hourly/list"
        else:
            print("Function is not defined")
            return
                    
        self.request_data(path, {
            "effectiveDateStart":DateStart,
            "effectiveDateEnd":DateEnd,
            "organization": self.organizationId,
            "page": {'number': self.page, 'size': 10000}})

        
        if self.final_response != None:
            self.formatted_final_response = self.format_files_precon(function)
            return self.formatted_final_response



    def meter_data_approved_meter_data_total(self,
                                             period:tuple = None,
                                              version:tuple = None,
                                              function = "list"):
        """
        !!!! - WARNING - !!!!!! Versiyon tutulmuyor olabilir / ORganizasyon bilgisine ihtiyaç duyulmuyor

        Toplam Onaylı Sayaç Verileri
        ---------
        Organizasyonun toplam aylık veriş, çekiş ve tenzil değerlerini döner.

        Parametre 
        ---------
         - period              : "2023-01-01T00:00:00+03:00" (Varsayılan: Güncel uzlaştırma periyotu)
         - version             : "2023-01-01T00:00:00+03:00" (Varsayılan: Güncel uzlaştırma periyotu)
         - function : "list","export" (Varsayılan: "list" | list ile dict formatında dönüş sağlar)
                
        Notlar
        ---------
         - version >= period olmalıdır.
         - Versiyon bulunmamaktadır.

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
            path = "https://epys.epias.com.tr/pre-reconciliation/v1/meter-data/approved-meter-data/total"
        else:
            print("Function is not defined")
            return
                    
        self.request_data(path, {
            "period":period,
            "version":version,
            "page": {'number': self.page, 'size': 10000}})

        
        if self.final_response != None:
            self.formatted_final_response = self.format_files_meter_data_total()
            return self.formatted_final_response



    def meter_data_approved_meter_data_profile_coefficient_get(self,
                                                               meterId:int,
                                                               period:tuple = None,
                                                               version:tuple = None,
                                                               function = "list"):
        """
        Profil Sayaç Katsayı Detayları
        ---------
        Sayaç katsayı detaylarını döner.

        Parametre 
        ---------
         - meterId             : (Zorunlu)
         - period              : "2023-01-01T00:00:00+03:00" (Varsayılan: Güncel uzlaştırma periyotu)
         - version             : "2023-01-01T00:00:00+03:00" (Varsayılan: Güncel uzlaştırma periyotu)
         - function : "list","export" (Varsayılan: "list" | list ile dict formatında, export ile dataframe veya dict olarak dönüş sağlar)
                
        Notlar
        ---------
         - version >= period olmalıdır.
         - Versiyon bulunmamaktadır.

        
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
            path = "https://epys.epias.com.tr/pre-reconciliation/v1/meter-data/approved-meter-data/profile-coefficient/get"
        elif function == "export":
            path = "https://epys.epias.com.tr/pre-reconciliation/v1/meter-data/approved-meter-data/profile/export"
        else:
            print("Function is not defined")
            return
                    
        self.request_data(path, {
            "meterId": meterId,
            "period":period,
            "version":version,
            "page": {'number': self.page, 'size': 10000}})

        
        if self.final_response != None:
            self.formatted_final_response = self.format_files_precon(function)
            return self.formatted_final_response



    def meter_data_approved_meter_data_profile_get(self,
                                                   meterId:int,
                                                   period:tuple = None,
                                                   version:tuple = None,
                                                   function = "list"):
        """
        Üç veya Tek Zamanlı Sayaç Veri Detayları
        ---------
        Üç veya Tek Zamanlı sayacın detay verilerini aylık kırlımda döner.

        Parametre 
        ---------
         - meterId             : (Zorunlu)
         - period              : "2023-01-01T00:00:00+03:00" (Varsayılan: Güncel uzlaştırma periyotu)
         - version             : "2023-01-01T00:00:00+03:00" (Varsayılan: Güncel uzlaştırma periyotu)
         - function : "list","export" (Varsayılan: "list" | list ile dict formatında dönüş sağlar)
                
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
            path = "https://epys.epias.com.tr/pre-reconciliation/v1/meter-data/approved-meter-data/profile/get"
        else:
            print("Function is not defined")
            return
                    
        self.request_data(path, {
            "meterId": meterId,
            "period":period,
            "version":version,
            "page": {'number': self.page, 'size': 10000}})

        
        if self.final_response != None:
            self.formatted_final_response = self.format_files_precon(function)
            return self.formatted_final_response



    def meter_data_approved_profile_meter_data(self,
                                               period:tuple = None,
                                               version:tuple = None,
                                               function = "list"):                                              
        """
        Üç veya Tek Zamanlı Sayaç Veri Detay
        ---------
        Üç veya Tek Zamanlı sayacın detay verilerini aylık kırılımda döner.

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
            path = "https://epys.epias.com.tr/pre-reconciliation/v1/meter-data/approved-profile-meter-data/list"
        elif function == "export":
            path = "https://epys.epias.com.tr/pre-reconciliation/v1/meter-data/approved-profile-meter-data/export"
        else:
            print("Function is not defined")
            return
                    
        self.request_data(path, {
            "period":period,
            "version":version,
            "organization": self.organizationId,
            "page": {'number': self.page, 'size': 10000}})

        
        if self.final_response != None:
            self.formatted_final_response = self.format_files_precon(function)
            return self.formatted_final_response



    def settlement_point_data(self,
                              settlementPointId:int = None,
                              period:tuple = None,
                              version:tuple = None,
                              DateStart:tuple = None,
                              DateEnd:tuple = None,
                              region = "TR1",
                              function = "list"):
        """
        UEVÇB Verileri Listeleme
        ---------
        UEVÇB verilerini döner.

        Parametre 
        ---------
         - settlementPointId   : None (Tamamı gelir)
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
            path = "https://epys.epias.com.tr/pre-reconciliation/v1/settlement-point/data"
        elif function == "export":
            path = "https://epys.epias.com.tr/pre-reconciliation/v1/settlement-point/data/export"
        else:
            print("Function is not defined")
            return
                    
        self.request_data(path, {
            "period":period,
            "version":version,
            "effectiveDateStart":DateStart,
            "effectiveDateEnd":DateEnd,
            "organization": self.organizationId,
            "settlementPointId":settlementPointId,
            "region": region, 
            "page": {'number': self.page, 'size': 10000}})

        
        if self.final_response != None:
            self.formatted_final_response = self.format_files_precon(function)
            return self.formatted_final_response




    def settlement_point_meter_data(self,
                                    settlementPointId= None,
                                    period:tuple = None,
                                    version:tuple = None,
                                    isDeduction = False,
                                    region = "TR1",
                                    function = "list"):                                              
        """
        UEVÇB'ye Bağlı Sayaçların Bilgileri
        ---------
        UEVÇB'ye Bağlı Sayaçların Veriş-Çekiş Değerlerini listesini döner.

        Parametre 
        ---------
         - meterId             : (Zorunlu)
         - period              : "2023-01-01T00:00:00+03:00" (Varsayılan: Güncel uzlaştırma periyotu)
         - version             : "2023-01-01T00:00:00+03:00" (Varsayılan: Güncel uzlaştırma periyotu)
         - isDeduction         : Tenzil durumu (False)
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
            path = "https://epys.epias.com.tr/pre-reconciliation/v1/settlement-point/meter-data/list"
        elif function == "export":
            path = "https://epys.epias.com.tr/pre-reconciliation/v1/settlement-point/meter-data/export"
        else:
            print("Function is not defined")
            return
                    
        self.request_data(path, {
            "settlementPointId": settlementPointId,
            "period":period,
            "version":version,
            "organization": self.organizationId,
            "isDeduction": isDeduction,
            "region": region,
            "page": {'number': self.page, 'size': 10000}})

        
        if self.final_response != None:
            self.formatted_final_response = self.format_files_precon(function)
            return self.formatted_final_response

