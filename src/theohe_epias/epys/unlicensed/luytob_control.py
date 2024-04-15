
from pandas import ExcelFile
from theohe_epias.epys.utils.get_time import get_current_settlement_days, get_last_day_of_month
from theohe_epias.epys.utils.time_format import tuple_to_datetime, control_times
from json import dumps
from requests import request


class LUYTOB():
    def request_luytob_data(self, path, payload, octet = False):
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
            if self.organizationId != 2:
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


    def format_files_luytob(self, function):
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

    def luytob_control(self,
                        period:tuple = get_current_settlement_days(first_day = True, finalised = False),
                        version:tuple = None,
                        function = "list"):
        """
        #Unlicensed
        LÜYTOB Kontrol
        ---------
        Fatura dönemi ve versiyonuna göre LÜY Fatura Tutarı (TL) ve LÜM Hesaplama Tutarı (TL) değerlerini döner.

        İlgili Sayfa
        ---------
        https://epys.epias.com.tr/unlicensed-electricity-generation-module-operation/reports/upr-control

        Parametre 
        ---------
         - period   : (2023,1) (Varsayılan: Güncel KESİNLEŞMEMİŞ (Ayın 6'sından sonra kesinleşmemiş Uzlaştırma çalışır) uzlaştırma dönemi kullanılmaktadır)
         - version   : (2023,1) (Varsayılan: None)
         - function : "list","export" (Varsayılan: "list" | list ile dict formatında, export ile dataframe veya dict olarak dönüş sağlar)
        
        """

        period= tuple_to_datetime(period)
        if period == False:
            return

        if version != None:
            version= tuple_to_datetime(version)
            if version == False:
                return

            if control_times(period, version, equal = True, label = "period") == False:
                return

        if function == "list":
            path = "https://epys{}.epias.com.tr/reconciliation-unlicensed/v1/luytop-report/list".format(self.test_coef)
        elif function == "export":
            path = "https://epys{}.epias.com.tr/reconciliation-unlicensed/v1/luytop-report/export".format(self.test_coef)
        else:
            print("Function is not defined")
            return
        
        self.request_luytob_data(path, {"period": period,"version": version,
                                 "page": {'number': self.page, 'size': 10000}})

                                 
        if self.final_response != None:
            self.formatted_final_response = self.format_files_luytob(function)
            return self.formatted_final_response                    


