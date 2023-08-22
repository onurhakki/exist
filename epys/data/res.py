from pandas import ExcelFile
from timeformat.TimeFormat import TimeFormat
from timeformat.TimeFormatControl import TimeFormatControl


class RES():
    def format_files_res(self, function):
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

    
    def rescostsettlement(self, 
                          powerPlantId:int = None,
                          settlementPointId:int = None,
                          period:tuple = None,
                          version:tuple = None,
                          category:list = [],
                          region = "TR1",
                          function = "list"):
        """

        !!!

        Export fonksiyonunda bir hata var
        
        !!!
        YEK UEVM
        ---------
        Organizasyonların YEKDEM kapsamındaki UEVM'!lerinin Kırpma, kapasite oranı ve YAT talimatına göre verilerini döner.

        Parametre
        ---------
         - powerPlantId        : None (Tamamı gelir)
         - settlementPointId   : None (Tamamı gelir)
         - category            : [] (Boş iken tamamı gelir)
            - "TRIMMED_GENERATION"
            - "CAPACITY_RATIO"
            - "DOWN_REGULATION" 
         - period : "2023-01-01T00:00:00+03:00" (Varsayılan: Güncel uzlaştırma periyotu)
         - version: "2023-01-01T00:00:00+03:00" (Varsayılan: Güncel uzlaştırma periyotu)
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
            path = "https://epys.epias.com.tr/reconciliation-res/v1/rescostsettlement/list"
        elif function == "export":
            path = "https://epys.epias.com.tr/reconciliation-res/v1/rescostsettlement/export"
        else:
            print("Function is not defined")
            return
        
        self.request_data(path, {
            "period": period, 
            "version": version,
            "powerPlantId": powerPlantId,
            "settlementPointId":settlementPointId,
            "category": category,
            "region": region, 

            "page": {'number': self.page, 'size': 10000}})

                                 
        if self.final_response != None:
            self.formatted_final_response = self.format_files_res(function)
            return self.formatted_final_response




    def res_unit_price(self,
                       DateStart:tuple = None,
                       DateEnd:tuple = None,
                       powerPlantTypes:list = [],
                       function = "list"):
        """
        YEK TL Birim Fiyatları
        ---------
        YEK TL Birim Fiyatları döner.

        Parametre 
        ---------
         - DateStart: "2023-01-01T00:00:00+03:00" (Varsayılan: Güncel uzlaştırma periyotu)
         - DateEnd: "2023-01-31T23:00:00+03:00" (Varsayılan: Güncel uzlaştırma periyotu)
         - powerPlantTypes: [] (Boş iken tamamı gelir)
            - "BIOMASS_BIOMETHANATION"
            - "BIOMASS_LANDFILL_GAS"
            - "WAVE_OR_TIDAL"
            - "WIND_OFFSHORE"
            - "SOLAR"
            - "GEOTHERMAL"
            - "WIND_ONSHORE"
            - "HYDRO_RIVER"
            - "HYDRO_PUMPED_STORAGE"
            - "HYDRO_RESERVOIR"
            - "WIND_OR_SOLAR_INTEGRATED_STORAGE"
            - "BIOMASS_THERMAL_TREATMENT"
         - function : "list","export" (Varsayılan: "list" | list ile dict formatında, export ile dataframe veya dict olarak dönüş sağlar)
        
        Notlar
        ---------
         - YEKDEM TL Hesaplama Verileri dışarı aktarıldığında (export) aynı sonucu verir.
         - Gerçekleşme tarihleri kullanılmıştır.
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
            path = "https://epys.epias.com.tr/reconciliation-res/v1/res/unit-price/list"
        elif function == "export":
            path = "https://epys.epias.com.tr/reconciliation-res/v1/res/unit-price/export"
        else:
            print("Function is not defined")
            return
                    
        self.request_data(path, {
            "effectiveDateStart": DateStart,
            "effectiveDateEnd": DateEnd,
            "powerPlantTypes": powerPlantTypes,
            "page": {'number': self.page, 'size': 10000}})

        
        if self.final_response != None:
            self.formatted_final_response = self.format_files_res(function)
            return self.formatted_final_response
        



    def res_coefficient_detail(self,
                       DateStart:tuple = None,
                       DateEnd:tuple = None,
                       function = "list"):
        """
        YEKDEM TL Hesaplama Verileri
        ---------
        YEKDEM TL Hesaplama Verileri döner.

        Parametre 
        ---------
         - DateStart: "2023-01-01T00:00:00+03:00" (Varsayılan: Güncel uzlaştırma periyotu)
         - DateEnd: "2023-01-31T23:00:00+03:00" (Varsayılan: Güncel uzlaştırma periyotu)
         - function : "list","export" (Varsayılan: "list" | list ile dict formatında, export ile dataframe veya dict olarak dönüş sağlar)
        
        Notlar
        ---------
         - YEK TL Birim Fiyatları dışarı aktarıldığında (export) aynı sonucu verir.
         - Gerçekleşme tarihleri kullanılmıştır.
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
            path = "https://epys.epias.com.tr/reconciliation-res/v1/res/unit-price/coefficient-detail/list"
        elif function == "export":
            path = "https://epys.epias.com.tr/reconciliation-res/v1/res/unit-price/export"
        else:
            print("Function is not defined")
            return
                    
        self.request_data(path, {
            "effectiveDateStart": DateStart,
            "effectiveDateEnd": DateEnd,
            "page": {'number': self.page, 'size': 10000}})

        
        if self.final_response != None:
            self.formatted_final_response = self.format_files_res(function)
            return self.formatted_final_response
        

    def luy_invoice_invoice(self,
                            settlementPointId:int = None,
                            period:tuple = None,
                            region = "TR1",
                            function = "list"):
        """
        LÜY Fatura
        ---------
        Lisanssız üretim yapan UEVCB'lere ait faturaları listeler.

        Parametre 
        ---------
         - period: "2023-01-01T00:00:00+03:00" (Varsayılan: Güncel uzlaştırma periyotu)
         - settlementPointId   : None (Tamamı gelir)       
         - function : "list","export" (Varsayılan: "list" | list ile dict formatında, export ile dataframe veya dict olarak dönüş sağlar)
        
        Notlar
        ---------
         - Yok.
        """

        if period == None:
            period= TimeFormat.current_settlement_date()
        else:
            period= TimeFormat.get_settlement_date(period)
            if period == False:
                return

        if function == "list":
            path = "https://epys.epias.com.tr/reconciliation-res/v1/luy-invoice/invoice/list"
        elif function == "export":
            path = "https://epys.epias.com.tr/reconciliation-res/v1/luy-invoice/invoice/export"
        else:
            print("Function is not defined")
            return
        
        self.request_data(path, {"period": period,
                                 "settlementPointId": settlementPointId,
                                 "region": region,
                                 "page": {'number': self.page, 'size': 10000}})

                                 
        if self.final_response != None:
            self.formatted_final_response = self.format_files_res(function)
            return self.formatted_final_response                    




    def payment_obligation(self, 
                          period:tuple = None,
                          version:tuple = None,
                          region = "TR1",
                          function = "list"):
        """

        YEK Uzlaştırma
        ---------
        Organizasyonların YEK kapsamındaki alacak ve ödeme tutarlarını döner.

        Parametre
        ---------
         - period : "2023-01-01T00:00:00+03:00" (Varsayılan: Güncel uzlaştırma periyotu)
         - versions: "2023-01-01T00:00:00+03:00" (Varsayılan: Güncel uzlaştırma periyotu)
         - function : "list","export" (Varsayılan: "list" | list ile dict formatında, export ile dataframe veya dict olarak dönüş sağlar)
        
        Notlar
        ---------
         - period yerine "effectiveDate" ile request oluşturulmaktadır. (period mantığında parametre kullanılmaktadır.) 
         - version yerine "versions" ile request oluşturulmaktadır.
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
            path = "https://epys.epias.com.tr/reconciliation-res/v1/payment-obligation/list"
        elif function == "export":
            path = "https://epys.epias.com.tr/reconciliation-res/v1/payment-obligation/export"
        else:
            print("Function is not defined")
            return
        
        self.request_data(path, {
            "effectiveDate": period, 
            "versions": [version],
            "region": region, 
            "page": {'number': self.page, 'size': 10000}})

                                 
        if self.final_response != None:
            self.formatted_final_response = self.format_files_res(function)
            return self.formatted_final_response


    def payment_obligation_detail(self,
                                  powerPlantId:int = None,
                                  settlementPointId:int = None,
                                  period:tuple = None,
                                  version:tuple = None,
                                  region = "TR1",
                                  function = "list"):
        """

        YEK UEVM Uzlaştırma
        ---------
        Organizasyonların YEKDEM kapsamındaki UEVM'lerinin detay kırılımını döner.

        Parametre
        ---------
         - powerPlantId        : None (Tamamı gelir)
         - settlementPointId   : None (Tamamı gelir)
         - period : "2023-01-01T00:00:00+03:00" (Varsayılan: Güncel uzlaştırma periyotu)
         - version: "2023-01-01T00:00:00+03:00" (Varsayılan: Güncel uzlaştırma periyotu)
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
            path = "https://epys.epias.com.tr/reconciliation-res/v1/payment-obligation/details/list"
        elif function == "export":
            path = "https://epys.epias.com.tr/reconciliation-res/v1/payment-obligation/details/export"
        else:
            print("Function is not defined")
            return
        
        self.request_data(path, {
            "effectiveDate": period, 
            "version": version,
            "powerPlantId": powerPlantId,
            "settlementPointId":settlementPointId,
            "region": region, 
            "page": {'number': self.page, 'size': 10000}})

                                 
        if self.final_response != None:
            self.formatted_final_response = self.format_files_res(function)
            return self.formatted_final_response



    def res_retrospective(self, 
                          period:tuple = None,
                          version:tuple = None,
                          function = "list"):
        """

        YEKDEM GDDK
        ---------
        YEKDEM GDDK döner.

        Parametre
        ---------
         - periodList : "2023-01-01T00:00:00+03:00" (Varsayılan: Güncel uzlaştırma periyotu)
         - version: "2023-01-01T00:00:00+03:00" (Varsayılan: Güncel uzlaştırma periyotu)
         - function : "list","export" (Varsayılan: "list" | list ile dict formatında, export ile dataframe veya dict olarak dönüş sağlar)
        
        Notlar
        ---------
         - period yerine "periodList" ile request oluşturulmaktadır. (period mantığında parametre kullanılmaktadır.) 
         - version > period olmalıdır.
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
            path = "https://epys.epias.com.tr/reconciliation-res/v1/res/retrospective/list"
        elif function == "export":
            path = "https://epys.epias.com.tr/reconciliation-res/v1/res/retrospective/export"
        else:
            print("Function is not defined")
            return
        
        self.request_data(path, {
            "periodList": [period], 
            "version": version,
            "page": {'number': self.page, 'size': 10000}})

                                 
        if self.final_response != None:
            self.formatted_final_response = self.format_files_res(function)
            return self.formatted_final_response



    def payment_obligation_detail(self,
                                  powerPlantId:int = None,
                                  settlementPointId:int = None,
                                  period:tuple = None,
                                  version:tuple = None,
                                  region = "TR1",
                                  function = "list"):
        """

        YEKDEM GDDK
        ---------
        YEKDEM GDDK döner.

        Parametre
        ---------
         - powerPlantId        : None (Tamamı gelir)
         - settlementPointId   : None (Tamamı gelir)
         - period : "2023-01-01T00:00:00+03:00" (Varsayılan: Güncel uzlaştırma periyotu)
         - version: "2023-01-01T00:00:00+03:00" (Varsayılan: Güncel uzlaştırma periyotu)
         - function : "list","export" (Varsayılan: "list" | list ile dict formatında, export ile dataframe veya dict olarak dönüş sağlar)
        
        Notlar
        ---------
         - version > period olmalıdır.
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
            path = "https://epys.epias.com.tr/reconciliation-res/v1/res/retrospective/detail-list"
        elif function == "export":
            path = "https://epys.epias.com.tr/reconciliation-res/v1/res/retrospective/detail-export"
        else:
            print("Function is not defined")
            return
        
        self.request_data(path, {
            "period": period, 
            "version": version,
            "powerPlantId": powerPlantId,
            "settlementPointId":settlementPointId,
            "region": region, 
            "page": {'number': self.page, 'size': 10000}})

                                 
        if self.final_response != None:
            self.formatted_final_response = self.format_files_res(function)
            return self.formatted_final_response


