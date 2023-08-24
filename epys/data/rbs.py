from pandas import ExcelFile
from timeformat.TimeFormat import TimeFormat
from timeformat.TimeFormatControl import TimeFormatControl


class RBS():
    def format_files_rbs(self, function):
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

    
    def auf(self, 
                DateStart:tuple = None,
                DateEnd:tuple = None, 
                sourceTypeId:int = None,
                function = "list"):
                          
        """
        #RBS
        Azami Uzlaştırma Fiyatı (AUF)
        ---------
        ...

        İlgili Sayfa
        ---------
        https://epys.epias.com.tr/reconciliation-operations/resource-based-support-operations/maximum-settlement-price-msp

        Parametre
        ---------
         - sourceTypeId            : (None iken tamamı gelir)
            - 0: Rüzgar
            - 1: Linyit
            - 2: Taş Kömürü
            - 3: İthal Kömür
            - 4: Fuel Oil
            - 5: Nafta
            - 6: Motorin
            - 7: Doğalgaz
            - 8: Jeotermal
            - 9: LPG
            - 10: Biogaz
            - 33: Kanal Tipi
            - 41: Güneş
            - 43: Biokütle
            - 44: Biokütleden Elde Edilen Gaz(LFG-Çöp Gazı)
            - 48: Nehir Tipi
            - 49: Rezervuarlı
            - 50: Prolitik Oil & Prolitik Gaz
            - 53: Proses Atık Isısı
            - 54: Asfaltit
            - 141: Rezervuarli + Kanal Tipi
         - DateStart: (2023,1,1) (Varsayılan: Güncel uzlaştırma periyotu)
         - DateEnd  : (2023,1,31) (Varsayılan: Güncel uzlaştırma periyotu)
         - function : "list","export" (Varsayılan: "list" | list ile dict formatında, export ile dataframe veya dict olarak dönüş sağlar)
        
        Notlar
        ---------
         - Maksimum bir senelik veri çekilebilmektedir.
        """

        if DateStart == None:
            DateStart= TimeFormat.current_settlement_date_start()
        else:
            DateStart= TimeFormat.get_settlement_date_day(DateStart)
            if DateStart == False:
                return
            
        if DateEnd == None:
            DateEnd= TimeFormat.current_settlement_date_end()
        else:
            DateEnd= TimeFormat.get_settlement_date_day(DateEnd)
            if DateEnd == False:
                return
            
        if TimeFormatControl.control_order_dates_equal(DateStart, DateEnd) == False:
            return False


        if function == "list":
            path = "https://epys.epias.com.tr/reconciliation-rbs/v1/min-recon-price/list"
        elif function == "export":
            path = "https://epys.epias.com.tr/reconciliation-rbs/v1/min-recon-price/export"
        else:
            print("Function is not defined")
            return
                    
        self.request_data(path, {
            "effectiveDateStart": DateStart,
            "effectiveDateEnd": DateEnd,
            "sourceTypeId":sourceTypeId,
            "page": {'number': self.page, 'size': 10000}})

        
        if self.final_response != None:
            self.formatted_final_response = self.format_files_market(function)
            return self.formatted_final_response



    def rbs_settlement(self, 
                       powerPlantId: int = None,
                       period:tuple = None,
                       version:tuple = None,
                       function = "list"):
        """
        #RBS
        Kaynak Bazında Destekleme Uzlaştırma
        ---------
        Organizasyonların Kaynak Bazında Destekleme Uzlaştırma alacak ve ödeme tutarlarını döner.

        Export fonksiyonu ile saatlik kırılım detayı da gelmektedir.

        İlgili Sayfa
        ---------
        https://epys.epias.com.tr/reconciliation-operations/resource-based-support-operations/resource-based-support-settlement

        Parametre
        ---------
         - powerPlantId        : None (Tamamı gelir)
         - period   : (2023,1) (Varsayılan: Güncel uzlaştırma periyotu)
         - version  : (2023,1) (Varsayılan: Güncel uzlaştırma periyotu)
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
            path = "https://epys.epias.com.tr/reconciliation-rbs/v1/reconciliation-rbs/power-plant/list"
        elif function == "export":
            path = "https://epys.epias.com.tr/reconciliation-rbs/v1/reconciliation-rbs/power-plant/export"
        else:
            print("Function is not defined")
            return
        
        self.request_data(path, {
            "period": period, 
            "version": version,
            "powerPlantId": powerPlantId, 
            "page": {'number': self.page, 'size': 10000}})

                                 
        if self.final_response != None:
            self.formatted_final_response = self.format_files_res(function)
            return self.formatted_final_response


    def rbs_settlement_organization(self,
                                    period:tuple = None,
                                    version:tuple = None,
                                    function = "list"):
        """
        #RBS
        Kaynak Bazında Destekleme Uzlaştırma - GTŞ
        ---------
        Organizasyonların Kaynak Bazında Destekleme Uzlaştırma alacak ve ödeme tutarlarını döner.

        İlgili Sayfa
        ---------
        https://epys.epias.com.tr/reconciliation-operations/resource-based-support-operations/resource-based-support-settlementars

        Parametre
        ---------
         - period   : (2023,1) (Varsayılan: Güncel uzlaştırma periyotu)
         - version  : (2023,1) (Varsayılan: Güncel uzlaştırma periyotu)
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
            path = "https://epys.epias.com.tr/reconciliation-rbs/v1/reconciliation-rbs/organization/list"
        elif function == "export":
            path = "https://epys.epias.com.tr/reconciliation-rbs/v1/reconciliation-rbs/organization/export"
        else:
            print("Function is not defined")
            return
        
        self.request_data(path, {
            "period": period, 
            "version": version,
            "page": {'number': self.page, 'size': 10000}})

                                 
        if self.final_response != None:
            self.formatted_final_response = self.format_files_res(function)
            return self.formatted_final_response








    def rbs_retrospective(self,
                          powerPlantId: int = None,
                          period:tuple = None,
                          version:tuple = None,
                          function = "list"):
        """
        #RBS
        #GDDK
        Kaynak Bazında Destekleme Uzlaştırma GDDK
        ---------
        Kaynak Bazında Destekleme Uzlaştırma GDDK döner.

        İlgili Sayfa
        ---------
        https://epys.epias.com.tr/reconciliation-operations/retro-operations/resource-based-support-settlement-retro

        Parametre
        ---------
         - powerPlantId        : None (Tamamı gelir)
         - period   : (2023,1) (Varsayılan: Güncel uzlaştırma periyotu)
         - version  : (2023,2) (Varsayılan: Güncel uzlaştırma periyotu)
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
            path = "https://epys.epias.com.tr/reconciliation-rbs/v1/reconciliation-rbs/power-plant/retro/list"
        elif function == "export":
            path = "https://epys.epias.com.tr/reconciliation-rbs/v1/reconciliation-rbs/power-plant/retro/export"
        else:
            print("Function is not defined")
            return
        
        self.request_data(path, {
            "period": period, 
            "version": version,
            "powerPlantId": powerPlantId, 
            "page": {'number': self.page, 'size': 10000}})

                                 
        if self.final_response != None:
            self.formatted_final_response = self.format_files_res(function)
            return self.formatted_final_response




    def rbs_retrospective_organization(self,
                                       period:tuple = None,
                                       version:tuple = None,
                                       function = "list"):
        """
        #RBS
        #GDDK
        Kaynak Bazında Destekleme Uzlaştırma - GTŞ GDDK
        ---------
        Kaynak Bazında Destekleme Uzlaştırma - GTŞ GDDK döner.

        İlgili Sayfa
        ---------
        https://epys.epias.com.tr/reconciliation-operations/retro-operations/resource-based-support-ars-retro

        Parametre
        ---------
         - period   : (2023,1) (Varsayılan: Güncel uzlaştırma periyotu)
         - version  : (2023,2) (Varsayılan: Güncel uzlaştırma periyotu)
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
            path = "https://epys.epias.com.tr/reconciliation-rbs/v1/reconciliation-rbs/organization/retro/list"
        elif function == "export":
            path = "https://epys.epias.com.tr/reconciliation-rbs/v1/reconciliation-rbs/organization/retro/export"
        else:
            print("Function is not defined")
            return
        
        self.request_data(path, {
            "period": period, 
            "version": version,
            "page": {'number': self.page, 'size': 10000}})

                                 
        if self.final_response != None:
            self.formatted_final_response = self.format_files_res(function)
            return self.formatted_final_response


