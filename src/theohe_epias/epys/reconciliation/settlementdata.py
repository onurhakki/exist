
from pandas import ExcelFile
from ...epys.utils.get_time import get_current_settlement_days, get_last_day_of_month
from ...epys.utils.time_format import tuple_to_datetime, control_times
from json import dumps
from requests import request


class SettlementData():
    def request_data_data(self, path, payload, octet = False):
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


    def format_files_data(self, function):
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


    def meter_data_approved_meter_data(self,
                            period:tuple = get_current_settlement_days(first_day = True, finalised = False),
                            version:tuple = None,
                            meterIds:list = [],
                            readStatus=True,
                            isLastVersion = False,
                            isRetrospective = False,
                            meterReadingCompany:int = None,
                            meterReadingType:str = None,
                            usageType:str = None,
                            region="TR1",
                            function = "list"):
        """
        #Precon
        Onaylı Sayaç Verisi
        ---------
        Onaylı sayaçların sayaç okunma durumlarına göre verilerini döner.

        İlgili Sayfa
        ---------
        https://epys.epias.com.tr/reconciliation-operations/data-operation/approved-meter-data

        Parametre 
        ---------
         - period              : (2023,1) (Varsayılan: Güncel KESİNLEŞMEMİŞ (Ayın 6'sından sonra kesinleşmemiş Uzlaştırma çalışır) uzlaştırma dönemi kullanılmaktadır)
         - version             : (2023,1) (Varsayılan: Güncel KESİNLEŞMEMİŞ (Ayın 6'sından sonra kesinleşmemiş Uzlaştırma çalışır) uzlaştırma dönemi kullanılmaktadır)
         - meterIds            : [] (Varsayılan: None - Hepsi Gelir)
         - readStatus          : True (Varsayılan: True - Okunmuşlar gelir)
         - isLastVersion       : False (Varsayılan: False - Hepsi Gelir)
         - isRetrospective     : False (Varsayılan: False - Hepsi Gelir)
         - meterReadingCompany : 650 (Varsayılan None - Hepsi Gelir)
            - meterReadingCompany => {650: 2. Bölge Müdürlüğü - İletim}
         - meterReadingType    : "HOURLY", "THREE_PHASE", "SINGLE_PHASE" (Varsayılan None - Hepsi Gelir)
         - usageType           : 3 (Varsayılan None - Hepsi Gelir)
            - usageType => {
                1: Trafo Merkezi,
                2: Serbest Tüketici (Normal)

                4: Üretim Şirketi,
                5: Otop. Üretim Tesisi,
                6: Otop. Tüketim Tesisi,

                8: Tüketim Sayacı,
                9: Teiaş İç İhtiyaç,
                10: İthalat-İhracat,                
                11: İç-İhtiyaç Diğer,
                12: Serbest Tüketici (OSB Ana Sayacı),
                13: Lisanssız Elektrik Üretim,
                14: Ölçüm Noktası,
                15: Dağıtım Şebeke Geçiş,
                16: Kuplaj,
                }
                
        Notlar
        ---------
         - version >= period olmalıdır.
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
            path = "https://epys{}.epias.com.tr/pre-reconciliation/v1/meter-data/approved-meter-data/list".format(self.test_coef)
        elif function == "export":
            path = "https://epys{}.epias.com.tr/pre-reconciliation/v1/meter-data/approved-meter-data/export".format(self.test_coef)
        else:
            print("Function is not defined")
            return
                    
        self.request_data_data(path, {
            "period":period,
            "version":version,
            "organization": self.organizationId,
            "meterIds":meterIds,
            "readStatus":readStatus,
            "isLastVersion":isLastVersion,
            "isRetrospective" : isRetrospective,
            "meterReadingCompany":meterReadingCompany,
            "meterReadingType":meterReadingType,
            "usageType":usageType,
            "region":region,
            "page": {'number': self.page, 'size': 10000}})

        
        if self.final_response != None:
            self.formatted_final_response = self.format_files_data(function)
            return self.formatted_final_response



    def meter_data_approved_meter_data_profile_coefficient_get(self,
                            meterId:int,
                            period:tuple = get_current_settlement_days(first_day = True, finalised = False),
                            version:tuple = get_current_settlement_days(first_day = True, finalised = False),
                            function = "list"):
        """
        #Precon
        Profil Sayaç Katsayı Detayları
        ---------
        Onaylı sayaçların tek veya üç zamanlı sayaç verilerini döner.

        İlgili Sayfa
        ---------
        https://epys.epias.com.tr/reconciliation-operations/data-operation/approved-meter-data

        Parametre 
        ---------
         - meterId             : int: Zorunlu
         - period              : (2023,1) (Varsayılan: Güncel KESİNLEŞMEMİŞ (Ayın 6'sından sonra kesinleşmemiş Uzlaştırma çalışır) uzlaştırma dönemi kullanılmaktadır)
         - version             : (2023,1) (Varsayılan: Güncel KESİNLEŞMEMİŞ (Ayın 6'sından sonra kesinleşmemiş Uzlaştırma çalışır) uzlaştırma dönemi kullanılmaktadır)
                
        Notlar
        ---------
         - version >= period olmalıdır.
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
            path = "https://epys{}.epias.com.tr/pre-reconciliation/v1/meter-data/approved-meter-data/profile-coefficient/get".format(self.test_coef)
        elif function == "export":
            path = "https://epys{}.epias.com.tr/pre-reconciliation/v1/meter-data/approved-meter-data/profile/export".format(self.test_coef)
        else:
            print("Function is not defined")
            return
                    
        self.request_data_data(path, {
            "period":period,
            "version":version,
            "meterId":meterId,
            "page": {'number': self.page, 'size': 10000}})

        
        if self.final_response != None:
            self.formatted_final_response = self.format_files_data(function)
            return self.formatted_final_response


    def meter_data_approved_meter_data_period(self,
                            meterId:int,
                            period:tuple = get_current_settlement_days(first_day = True, finalised = False),
                            version:tuple = get_current_settlement_days(first_day = True, finalised = False),
                            function = "list"):
        """
        #Precon
        Saatlik Sayaç Verileri
        ---------
        Onaylı sayaçların saatlik olanlarının sayaç verilerini döner.

        İlgili Sayfa
        ---------
        https://epys.epias.com.tr/reconciliation-operations/data-operation/approved-meter-data

        Parametre 
        ---------
         - meterId             : int: Zorunlu
         - period              : (2023,1) (Varsayılan: Güncel KESİNLEŞMEMİŞ (Ayın 6'sından sonra kesinleşmemiş Uzlaştırma çalışır) uzlaştırma dönemi kullanılmaktadır)
         - version             : (2023,1) (Varsayılan: Güncel KESİNLEŞMEMİŞ (Ayın 6'sından sonra kesinleşmemiş Uzlaştırma çalışır) uzlaştırma dönemi kullanılmaktadır)
                
        Notlar
        ---------
         - version >= period olmalıdır.
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
            path = "https://epys{}.epias.com.tr/pre-reconciliation/v1/meter-data/approved-meter-data/hourly/get".format(self.test_coef)
        elif function == "export":
            path = "https://epys{}.epias.com.tr/pre-reconciliation/v1/meter-data/approved-meter-data/hourly/export".format(self.test_coef)
        else:
            print("Function is not defined")
            return
                    
        self.request_data_data(path, {
            "period":period,
            "version":version,
            "meterId":meterId,
            "page": {'number': self.page, 'size': 10000}})

        
        if self.final_response != None:
            self.formatted_final_response = self.format_files_data(function)
            return self.formatted_final_response


