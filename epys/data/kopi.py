from pandas import ExcelFile
from timeformat.TimeFormat import TimeFormat
from timeformat.TimeFormatControl import TimeFormatControl


class KOPI():
    def format_files_kopi(self, function):
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

    
    def objections(self,
                   DateStart:tuple = None,
                   DateEnd:tuple = None, 
                   objectionStatus:str = None,
                   function = "list"):
        """
        #KOPİ
        KOPİ (Karşılığı Olmayan Piyasa İşlemleri) İtirazlar
        ---------
        KOPİ itirazlarını döner.

        İlgili Sayfa
        ---------
        https://epys.epias.com.tr/reconciliation-operations/unrequited-market-transactions/objections

        Parametre 
        ---------
         - DateStart: (2023,1,1) (Varsayılan: Güncel uzlaştırma periyotu)         
         - DateEnd  : (2023,1,31) (Varsayılan: Güncel uzlaştırma periyotu)
         - objectionStatus: None (Tamamı gelir)
            - "REJECTED",
            - "ACCEPTED",
            - "PASSIVE"
         - function : "list","export" (Varsayılan: "list" | list ile dict formatında, export ile dataframe veya dict olarak dönüş sağlar)
        
        Notlar
        ---------
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
            path = "https://epys.epias.com.tr/reconciliation-umt/v1/unrequited-sales-control/objection/list"
        elif function == "export":
            path = "https://epys.epias.com.tr/reconciliation-umt/v1/unrequited-sales-control/objection/export"
        else:
            print("Function is not defined")
            return
                    
        self.request_data(path, {
            "paymentDateStart": DateStart,
            "paymentDateEnd": DateEnd,
            "objectionStatus": objectionStatus,
            "page": {'number': self.page, 'size': 10000}})

        
        if self.final_response != None:
            self.formatted_final_response = self.format_files_market(function)
            return self.formatted_final_response




    def unrequited_sales_control(self,
                           DateStart:tuple = None,
                           DateEnd:tuple = None,
                           sanctionStatus:str = None,
                           advanceBlockingStatuses:list = ["BLOCKED","UNBLOCKED","NO_BLOCK"],
                           function = "list"):
        """
        #KOPİ
        KOPİ Kontrol İşlemleri
        ---------
        KOSM𝑝,𝑠 = (VEPSM𝑝,𝑠 + GÖPVTSM𝑝,𝑠 + GİPVTSM𝑝,𝑠 + GÖPSSM𝑝,𝑠 + GİPSM𝑝,𝑠 + İASM𝑝,𝑠 ) 
        − maks [ TM, (KGÜP𝑝,𝑠 + VEPAM𝑝,𝑠 + GÖPVTAM𝑝,𝑠 + GİPVTAM𝑝,𝑠 + GÖPSAM𝑝,𝑠 + GİPAM𝑝,𝑠 + İAAM𝑝,𝑠 + SPİM𝑝,𝑠 + LÜM𝑝,𝑠 ) × 𝑟 ]
        
        Karşılığı Olmayan Satış Miktarı; "Negatif" ise açığa satış yok, "Pozitif" ise açığa satış var.

        İlgili Sayfa
        ---------
        https://epys.epias.com.tr/reconciliation-operations/unrequited-market-transactions/control-operations

        Parametre 
        ---------
         - DateStart: (2023,1,1,0) (Varsayılan: Güncel uzlaştırma periyotu)
         - DateEnd  : (2023,1,31,23) (Varsayılan: Güncel uzlaştırma periyotu)
         - advanceBlockingStatuses: ["BLOCKED","UNBLOCKED","NO_BLOCK"] (Varsayılan)
         - sanctionStatus:
          - "ACTIVE",
          - "PASSIVE",
          - "NONE",
         - function : "list","export" (Varsayılan: "list" | list ile dict formatında, export ile dataframe veya dict olarak dönüş sağlar)
        
        Notlar
        ---------
         - export fonksiyonu market transaction control ile aynı çıktıyı vermektedir.
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
            path = "https://epys.epias.com.tr/reconciliation-umt/v1/unrequited-sales-control/list"
        elif function == "export":
            path = "https://epys.epias.com.tr/reconciliation-umt/v1/unrequited-sales-control/export"
        else:
            print("Function is not defined")
            return
                    
        self.request_data(path, {
            "dueDateStart": DateStart,
            "dueDateEnd": DateEnd,
            "sanctionStatus": sanctionStatus,
            "advanceBlockingStatuses": advanceBlockingStatuses,
            "page": {'number': self.page, 'size': 10000}})

        
        if self.final_response != None:
            self.formatted_final_response = self.format_files_res(function)
            return self.formatted_final_response
        



    def transaction_control(self,
                           DateStart:tuple = None,
                           DateEnd:tuple = None,
                           function = "list"):
        """
        #KOPİ
        KOPİ Kontrol İşlemleri
        ---------
        "*" ile başlayan yaptırım tarihi katılımcıların ihlal durumları kesinleşmemiştir. GİP Ticaretinin bitişinden sonra kesinleşecektir.

        "**" ile işaretlenmiş Avans Bloke Yaptırım Tutarı yaptırım tarihinde kesinleşecektir.

        İlgili Sayfa
        ---------
        https://epys.epias.com.tr/reconciliation-operations/unrequited-market-transactions/control-operations

        Parametre 
        ---------
         - DateStart: (2023,1,1,0) (Varsayılan: Güncel uzlaştırma periyotu)
         - DateEnd  : (2023,1,31,23) (Varsayılan: Güncel uzlaştırma periyotu)
         - function : "list","export" (Varsayılan: "list" | list ile dict formatında, export ile dataframe veya dict olarak dönüş sağlar)
        
        Notlar
        ---------
         - export fonksiyonu unrequited_sales_control ile aynı çıktıyı vermektedir.
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
            path = "https://epys.epias.com.tr/reconciliation-umt/v1/market-transaction/list"
        elif function == "export":
            path = "https://epys.epias.com.tr/reconciliation-umt/v1/unrequited-sales-control/export"
        else:
            print("Function is not defined")
            return
                    
        self.request_data(path, {
            "dueDateStart": DateStart,
            "dueDateEnd": DateEnd,
            "page": {'number': self.page, 'size': 10000}})

        
        if self.final_response != None:
            self.formatted_final_response = self.format_files_res(function)
            return self.formatted_final_response
        


