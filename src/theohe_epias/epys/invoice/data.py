
from pandas import ExcelFile
from ...epys.utils.get_time import get_current_settlement_days
from ...epys.utils.time_format import tuple_to_datetime
from json import dumps
from requests import request

class Invoice():
    def request_invoice_data(self, path, payload, octet = False):
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


    def invoice_notice_invoice_item_with_tax(self,
                                             period:tuple = get_current_settlement_days(first_day = True, finalised = True),
                                             function = "export"):
        """
        #Invoice
        Fatura Kalemleri
        ---------
        Faturaya esas kalemlerinin tutarlarını KDV dahil fatura kalemi kırılımında döner.

        İlgili Sayfa
        ---------
        https://epys.epias.com.tr/invoice-operations/invoice-items

        Parametre 
        ---------
         - period       : (2023,1) (Varsayılan: Güncel KESİNLEŞMİŞ (15'i veya 15'i haftasonuna gelmesi durumunda bir sonraki iş günü) uzlaştırma dönemi kullanılmaktadır)
         - function     : "list","export" (Varsayılan: "list" | list ile dict formatında, export ile dataframe veya dict olarak dönüş sağlar)
        
        """

        period= tuple_to_datetime(period)
        if period == False:
            return

        if function == "list":
            path = "https://epys{}.epias.com.tr/reconciliation-invoice/v1/invoice-notice/invoice-item-with-tax/list".format(self.test_coef)
        elif function == "export":
            path = "https://epys{}.epias.com.tr/reconciliation-invoice/v1/invoice-notice/invoice-item-with-tax/list/export".format(self.test_coef)
        else:
            print("Function is not defined")
            return
        
        self.request_invoice_data(path, {"effectiveDate": period,
        "page": {'number': self.page, 'size': 10000}})

                                 
        if self.final_response != None:
            self.formatted_final_response = self.format_files_invoice(function)
            return self.formatted_final_response                    



