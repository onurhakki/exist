
from pandas import ExcelFile
from timeformat.TimeFormat import TimeFormat
from timeformat.TimeFormatControl import TimeFormatControl


class Invoice():
    def format_files_invoice(self, function):
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

    def invoice_notice(self,
                       period:tuple = None,
                       function = "list"):
        """
        Aylık Uzlaştırma Bildirimi
        ---------
        Aylık uzlaştırma bildirimini döner.

        Parametre 
        ---------
         - period: "2023-01-01T00:00:00+03:00" (Varsayılan: Güncel uzlaştırma periyotu)         
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
            path = "https://epys.epias.com.tr/reconciliation-invoice/v1/invoice-notice/list"
        elif function == "export":
            path = "https://epys.epias.com.tr/reconciliation-invoice/v1/invoice-notice/export"
        else:
            print("Function is not defined")
            return
        
        self.request_data(path, {"period": period,
                                 "page": {'number': self.page, 'size': 10000}})

                                 
        if self.final_response != None:
            self.formatted_final_response = self.format_files_invoice(function)
            return self.formatted_final_response                    

    def invoice_notice_invoice_item_with_tax(self,
                                             period:tuple = None,
                                             function = "list"):
        """
        Fatura Bildirimi
        ---------
        Faturaya esas kalemlerinin tutarlarını döner.

        Parametre 
        ---------
         - effectiveDate: "2023-01-01T00:00:00+03:00" (Varsayılan: Güncel uzlaştırma periyotu)
         - function     : "list","export" (Varsayılan: "list" | list ile dict formatında, export ile dataframe veya dict olarak dönüş sağlar)
        
        Notlar
        ---------
         - Parametre olarak period verildiği halde request'de effectiveDate parametresi kullanılmaktadır.
         - Bir karışıklık veya yanlışlık bulunmamaktadır.
        """

        if period == None:
            period= TimeFormat.current_settlement_date()
        else:
            period= TimeFormat.get_settlement_date(period)
            if period == False:
                return

        if function == "list":
            path = "https://epys.epias.com.tr/reconciliation-invoice/v1/invoice-notice/invoice-item-with-tax/list"
        elif function == "export":
            path = "https://epys.epias.com.tr/reconciliation-invoice/v1/invoice-notice/invoice-item-with-tax/list/export"
        else:
            print("Function is not defined")
            return
        
        self.request_data(path, {"effectiveDate": period,
                                 "page": {'number': self.page, 'size': 10000}})

                                 
        if self.final_response != None:
            self.formatted_final_response = self.format_files_invoice(function)
            return self.formatted_final_response                    



    def invoice_notice_retrospective(self,
                                     period:tuple = None,
                                     function = "list"):
        """
        Dönemlik GDDK Bildirimi
        ---------
        Dönemlik GDDK tutarlarını döner.

        Parametre 
        ---------
         - effectiveDate: "2023-01-01T00:00:00+03:00" (Varsayılan: Güncel uzlaştırma periyotu)
         - function     : "list","export" (Varsayılan: "list" | list ile dict formatında, export ile dataframe veya dict olarak dönüş sağlar)
        
        Notlar
        ---------
         - Parametre olarak period verildiği halde request'de effectiveDate parametresi kullanılmaktadır.
         - Bir karışıklık veya yanlışlık bulunmamaktadır.
        """

        if period == None:
            period= TimeFormat.current_settlement_date()
        else:
            period= TimeFormat.get_settlement_date(period)
            if period == False:
                return

        if function == "list":
            path = "https://epys.epias.com.tr/reconciliation-invoice/v1/invoice-notice/retrospective/list"
        elif function == "export":
            path = "https://epys.epias.com.tr/reconciliation-invoice/v1/invoice-notice/retrospective/export"
        else:
            print("Function is not defined")
            return
        
        self.request_data(path, {"effectiveDate": period,
                                 "page": {'number': self.page, 'size': 10000}})

                                 
        if self.final_response != None:
            self.formatted_final_response = self.format_files_invoice(function)
            return self.formatted_final_response                    

