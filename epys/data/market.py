
from pandas import ExcelFile
from timeformat.TimeFormat import TimeFormat
from timeformat.TimeFormatControl import TimeFormatControl


class Market():
    def format_files_market(self, function):
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

    def format_files_mcp(self):
        result = self.final_response.json()["body"]["content"]['marketClearingPrices']
        return result


    def advance(self,
                DateStart:tuple = None,
                DateEnd:tuple = None, function = "list"):
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
         - DateStart: (2023,1,1) (Varsayılan: Güncel uzlaştırma periyotu)         
         - DateEnd  : (2023,1,31) (Varsayılan: Güncel uzlaştırma periyotu)
         - function : "list","export" (Varsayılan: "list" | list ile dict formatında, export ile dataframe veya dict olarak dönüş sağlar)
        
        Notlar
        ---------
         - Ödeme tarihleri kullanılmıştır.
         - DateEnd > DateStart olmalıdır.
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
            path = "https://epys.epias.com.tr/reconciliation-market/v1/advance/list"
        elif function == "export":
            path = "https://epys.epias.com.tr/reconciliation-market/v1/advance/export"
        else:
            print("Function is not defined")
            return
                    
        self.request_data(path, {
            "paymentDateStart": DateStart,
            "paymentDateEnd": DateEnd,
            "page": {'number': self.page, 'size': 10000}})

        
        if self.final_response != None:
            self.formatted_final_response = self.format_files_market(function)
            return self.formatted_final_response


    def bilateral_contract(self,
                           DateStart:tuple = None,
                           DateEnd:tuple = None,
                           function = "list"):
        """
        #Market
        İkili Anlaşma
        ---------
        Uzlaştırma dönemi bazında günlük toplam ikili anlaşma alış-satış miktarlarını saatlik kırılımda döner.

        İlgili Sayfa
        ---------
        https://epys.epias.com.tr/reconciliation-operations/bilateral-agreement-operations/bilateral-contract

        Parametre 
        ---------
         - DateStart: (2023,1,1,0) (Varsayılan: Güncel uzlaştırma periyotu)
         - DateEnd  : (2023,1,31,23) (Varsayılan: Güncel uzlaştırma periyotu)
         - function : "list","export" (Varsayılan: "list" | list ile dict formatında, export ile dataframe veya dict olarak dönüş sağlar)
        
        Notlar
        ---------
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
            path = "https://epys.epias.com.tr/reconciliation-market/v1/bilateral-contract/list"
        elif function == "export":
            path = "https://epys.epias.com.tr/reconciliation-market/v1/bilateral-contract/export"
        else:
            print("Function is not defined")
            return
                    
        self.request_data(path, {
            "effectiveDateStart": DateStart,
            "effectiveDateEnd": DateEnd,
            "page": {'number': self.page, 'size': 10000}})

        
        if self.final_response != None:
            self.formatted_final_response = self.format_files_market(function)
            return self.formatted_final_response


    def bilateral_contract_detail(self,
                                  DateStart:tuple = None,
                                  DateEnd:tuple = None, 
                                  targetOrganizationId:int = None, 
                                  function = "list"):
        """
        #Market
        İkili Anlaşma Detayları
        ---------
        Uzlaştırma dönemi bazında günlük toplam ikili anlaşma alış-satış miktarlarını seçilen organizasyon detaylarını saatlik kırılımda döner.

        İlgili Sayfa
        ---------
        https://epys.epias.com.tr/reconciliation-operations/bilateral-agreement-operations/bilateral-contract-detail

        Parametre 
        ---------
         - DateStart: (2023,1,1,0) (Varsayılan: Güncel uzlaştırma periyotu)
         - DateEnd: (2023,1,31,23) (Varsayılan: Güncel uzlaştırma periyotu)
         - targetOrganizationId: None (Varsayılan: None | ikili anlaşma yapılan organizasyonları id'si girelebilir)
         - function: "list","export" (Varsayılan: "list" | list ile dict formatında, export ile dataframe veya dict olarak dönüş sağlar)
        
        Notlar
        ---------
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
            path = "https://epys.epias.com.tr/reconciliation-market/v1/bilateral-contract/detail/list"
        elif function == "export":
            path = "https://epys.epias.com.tr/reconciliation-market/v1/bilateral-contract/detail/export"
        else:
            print("Function is not defined")
            return
                    
        self.request_data(path, {
            "effectiveDateStart": DateStart,
            "effectiveDateEnd": DateEnd,
            "targetOrganizationId" : targetOrganizationId,
            "page": {'number': self.page, 'size': 10000}})

        
        if self.final_response != None:
            self.formatted_final_response = self.format_files_market(function)
            return self.formatted_final_response


    def market_day_ahead_market_daily(self,
                           DateStart:tuple = None,
                           DateEnd:tuple = None, 
                           region = "TR1",
                           function = "list"):
        """
        #Market
        Gün Öncesi Piyasası(GÖP) Uzlaştırma Detay Bildirimi
        ---------
        Organizasyonların GÖP'de yapmış oldukları eşleşme detaylarını saatlik kırılımda döner.

        İlgili Sayfa
        ---------
        https://epys.epias.com.tr/reconciliation-operations/dam-operations/dam-settlement-detail

        Parametre 
        ---------
         - DateStart: (2023,1,1,0) (Varsayılan: Güncel uzlaştırma periyotu)
         - DateEnd: (2023,1,31,23) (Varsayılan: Güncel uzlaştırma periyotu)
         - function: "list","export" (Varsayılan: "list" | list ile dict formatında, export ile dataframe veya dict olarak dönüş sağlar)
        
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
            path = "https://epys.epias.com.tr/reconciliation-market/v1/market/day-ahead-market/daily/list"
        elif function == "export":
            path = "https://epys.epias.com.tr/reconciliation-market/v1/market/day-ahead-market/daily/export"
        else:
            print("Function is not defined")
            return
                    
        self.request_data(path, {
            "deliveryDayStart": DateStart,
            "deliveryDayEnd": DateEnd,
            "region": region,
            "page": {'number': self.page, 'size': 10000}})

        
        if self.final_response != None:
            self.formatted_final_response = self.format_files_market(function)
            return self.formatted_final_response


    def market_day_ahead_market(self,
                           DateStart:tuple = None,
                           DateEnd:tuple = None, 
                           region = "TR1",
                           function = "list"):
        """
        #Market
        Gün Öncesi Piyasası(GÖP) Uzlaştırma Bildirimi
        ---------
        Organizasyonların GÖP'de yapmış oldukları eşleşme detaylarını günlük kırılımda döner.

        İlgili Sayfa
        ---------
        https://epys.epias.com.tr/reconciliation-operations/dam-operations/dam-settlement

        Parametre 
        ---------
         - DateStart: (2023,1,1) (Varsayılan: Güncel uzlaştırma periyotu)
         - DateEnd: (2023,1,31) (Varsayılan: Güncel uzlaştırma periyotu)
         - function: "list","export" (Varsayılan: "list" | list ile dict formatında, export ile dataframe veya dict olarak dönüş sağlar)
        
        Notlar
        ---------
         - Enerjinin teslim edilme tarihleri kullanılmıştır.
         - DateEnd > DateStart olmalıdır.
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
            path = "https://epys.epias.com.tr/reconciliation-market/v1/market/day-ahead-market/list"
        elif function == "export":
            path = "https://epys.epias.com.tr/reconciliation-market/v1/market/day-ahead-market/export"
        else:
            print("Function is not defined")
            return
                    
        self.request_data(path, {
            "deliveryDayStart": DateStart,
            "deliveryDayEnd": DateEnd,
            "region": region,
            "page": {'number': self.page, 'size': 10000}})

        
        if self.final_response != None:
            self.formatted_final_response = self.format_files_market(function)
            return self.formatted_final_response



    def market_day_ahead_market_gap_amount(self,
                           DateStart:tuple = None,
                           DateEnd:tuple = None, 
                           region = "TR1",
                           function = "list"):
        """
        #Market
        Gün Öncesi Piyasası(GÖP) Fark Tutarı
        ---------
        Organizasyonun gün öncesi piyasasında fark fonu bilgilerini günlük kırılımda döner.

        İlgili Sayfa
        ---------
        https://epys.epias.com.tr/reconciliation-operations/dam-operations/dam-settlement-detail

        Parametre 
        ---------
         - DateStart: (2023,1,1) (Varsayılan: Güncel uzlaştırma periyotu)
         - DateEnd: (2023,1,31) (Varsayılan: Güncel uzlaştırma periyotu)
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
            path = "https://epys.epias.com.tr/reconciliation-market/v1/market/day-ahead-market/gap-amount/list"
        else:
            print("Function is not defined")
            return
                                        
        self.request_data(path, {
            "deliveryDayStart": DateStart,
            "deliveryDayEnd": DateEnd,
            "region": region,
            "page": {'number': self.page, 'size': 10000}})

        
        if self.final_response != None:
            self.formatted_final_response = self.format_files_market(function)
            return self.formatted_final_response



    def market_day_ahead_market_mcp(self,
                           DateStart:tuple = None,
                           DateEnd:tuple = None, 
                           function = "list"):
        """
        #Market
        Gün Öncesi Piyasası(GÖP) Piyasa Takas Fiyatı (PTF)
        ---------
        Saatlik kırılımda Piyasa Takas Fiyatı (PTF) bilgilerini saatlik kırılımda döner.

        İlgili Sayfa
        ---------
        Yok.

        Parametre 
        ---------
         - DateStart: (2023,1,1,0) (Varsayılan: Güncel uzlaştırma periyotu)
         - DateEnd: (2023,1,31,23) (Varsayılan: Güncel uzlaştırma periyotu)
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
            path = "https://epys.epias.com.tr/reconciliation-market/v1/market/day-ahead-market/mcp/list"
        else:
            print("Function is not defined")
            return
                                        
        self.request_data(path, {
            "effectiveDateStart": DateStart,
            "effectiveDateEnd": DateEnd,
            "page": {'number': self.page, 'size': 10000}})

        
        if self.final_response != None:
            self.formatted_final_response = self.format_files_mcp()
            return self.formatted_final_response



    def market_intraday_market(self,
                           DateStart:tuple = None,
                           DateEnd:tuple = None, 
                           region = "TR1",
                           function = "list"):
        """
        #Market
        Gün İçi Piyasası(GİP) Uzlaştırma Bildirimi
        ---------
        Organizasyonun gün içi piyasasındaki eşleşme sonuçlarını günlük kırılımda döner.

        İlgili Sayfa
        ---------
        https://epys.epias.com.tr/reconciliation-operations/idm-operations/idm-settlement

        Parametre 
        ---------
         - DateStart: (2023,1,1) (Varsayılan: Güncel uzlaştırma periyotu)
         - DateEnd: (2023,1,31) (Varsayılan: Güncel uzlaştırma periyotu)
         - function : "list","export" (Varsayılan: "list" | list ile dict formatında, export ile dataframe veya dict olarak dönüş sağlar)
        
        Notlar
        ---------
         - Enerjinin teslim edilme tarihleri kullanılmıştır.
         - DateEnd > DateStart olmalıdır.
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
            path = "https://epys.epias.com.tr/reconciliation-market/v1/market/intraday-market/list"
        elif function == "export":
            path = "https://epys.epias.com.tr/reconciliation-market/v1/market/intraday-market/export"
        else:
            print("Function is not defined")
            return
                                        
        self.request_data(path, {
            "deliveryDayStart": DateStart,
            "deliveryDayEnd": DateEnd,
            "region": region,
            "page": {'number': self.page, 'size': 10000}})

        
        if self.final_response != None:
            self.formatted_final_response = self.format_files_market(function)
            return self.formatted_final_response


    def market_intraday_market_daily(self,
                           DateStart:tuple = None,
                           DateEnd:tuple = None, 
                           region = "TR1",
                           function = "list"):
        """
        #Market
        Gün İçi Piyasası(GİP) Uzlaştırma Detay Bildirimi 
        ---------
        Organizasyonun gün içi piyasasındaki eşleşme sonuçlarını saatlik kırılımda döner.

        İlgili Sayfa
        ---------
        https://epys.epias.com.tr/reconciliation-operations/idm-operations/idm-settlement-detail

        Parametre 
        ---------
         - DateStart: (2023,1,1,0) (Varsayılan: Güncel uzlaştırma periyotu)
         - DateEnd: (2023,1,31,23) (Varsayılan: Güncel uzlaştırma periyotu)
         - function : "list","export" (Varsayılan: "list" | list ile dict formatında, export ile dataframe veya dict olarak dönüş sağlar)
        
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
            path = "https://epys.epias.com.tr/reconciliation-market/v1/market/intraday-market/daily/list"
        elif function == "export":
            path = "https://epys.epias.com.tr/reconciliation-market/v1/market/intraday-market/daily/export"
        else:
            print("Function is not defined")
            return
                                        
        self.request_data(path, {
            "deliveryDayStart": DateStart,
            "deliveryDayEnd": DateEnd,
            "region": region,
            "page": {'number': self.page, 'size': 10000}})

        
        if self.final_response != None:
            self.formatted_final_response = self.format_files_market(function)
            return self.formatted_final_response
