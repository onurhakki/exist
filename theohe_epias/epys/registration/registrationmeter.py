
from pandas import ExcelFile
from ...epys.utils.get_time import get_current_settlement_days, get_last_day_of_month
from ...epys.utils.time_format import tuple_to_datetime, control_times
from json import dumps
from requests import request


class RegistrationMeter():
    def request_registrationmeter_data(self, path, payload, octet = False):
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


    def format_files_registrationmeter(self, function):
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


    def registration_meter_data(self,
                        id:int = None,
                        effectiveDate:tuple = None,
                        eic:str = None,
                        mainMeterId:int = None,
                        readingOrganizationId:int = None,
                        recordUsageStatusId:int = 1, # Mevcut Durum: 1 Kullanımda, 2 Kullanım dışı
                        statusId:int = 2, #Durum: 2 Aktif, 3 Pasif
                        substationId:int = None, # Trafo Merkezi
                        usageTypeIds:list = [],
                        supplySettlementPointId:int = None,
                        supplyDeductionSettlementPointId:int = None,
                        withdrawDeductionSettlementPointId:int = None,
                        withdrawSettlementPointId:int = None,
                        function = "list"
):
        """
        #Registration
        Sayaç Listeleme
        ---------
        Sayaçların kayıt detaylarını döner.

        İlgili Sayfa
        ---------
        https://epys.epias.com.tr/registration-operations/meter-operations/meter-list

        Parametre 
        ---------
         - id:int = None,
         - effectiveDate:tuple = None,
         - eic:str = None,
         - mainMeterId:int = None,
         - readingOrganizationId:int = None,
         - recordUsageStatusId:int = 1, # Mevcut Durum: 1 Kullanımda, 2 Kullanım dışı
         - statusId:int = 2, #Durum: 2 Aktif, 3 Pasif
         - substationId:int = None, # Trafo Merkezi
         - usageTypeIds:list = None
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

         - supplySettlementPointId:int = None,
         - supplyDeductionSettlementPointId:int = None,
         - withdrawDeductionSettlementPointId:int = None,
         - withdrawSettlementPointId:int = None,
                
        Notlar
        ---------
         - Eğer ID girilirse diğer parametreler boş olabilir.
         - Eğer ID girilmezse zorunlu parametrelerin doldurulması gerekir.
         - contains'ler eklenmedi.
        """

        if effectiveDate != None:
            effectiveDate= tuple_to_datetime(effectiveDate)
            if effectiveDate == False:
                return

            
        if function == "list":
            path = "https://epys{}.epias.com.tr/grid/v1/meter/query".format(self.test_coef)
        else:
            print("Function is not defined")
            return
                    
        self.request_registrationmeter_data(path, {
                                    "effectiveDate":effectiveDate,
                        "id":id,
                        "eic":eic,
                        "mainMeterId":mainMeterId,
                        "organizationId":None if self.organizationId == 2 else self.organizationId,
                        "readingOrganizationId":readingOrganizationId,
                        "recordUsageStatusId":recordUsageStatusId, # Mevcut Durum: 1 Kullanımda, 2 Kullanım dışı
                        "statusId":statusId, #Durum: 2 Aktif, 3 Pasif
                        "substationId":substationId, # Trafo Merkezi
                        "usageTypeIds":usageTypeIds,

                        "supplySettlementPointId":supplySettlementPointId,
                        "supplyDeductionSettlementPointId":supplyDeductionSettlementPointId,
                        "withdrawDeductionSettlementPointId":withdrawDeductionSettlementPointId,
                        "withdrawSettlementPointId":withdrawSettlementPointId,

            "page": {'number': self.page, 'size': 10000}})

        
        if self.final_response != None:
            self.formatted_final_response = self.format_files_registrationmeter(function)
            return self.formatted_final_response



    def registration_unlicensed_meter_data(self,
                        id:int = None,
                        effectiveDate:tuple = None,
                        eic:str = None,
                        mainMeterId:int = None,
                        readingOrganizationId:int = None,
                        recordUsageStatusId:int = 1, # Mevcut Durum: 1 Kullanımda, 2 Kullanım dışı
                        statusId:int = 2, #Durum: 2 Aktif, 3 Pasif
                        substationId:int = None, # Trafo Merkezi
                        supplySettlementPointId:int = None,
                        supplyDeductionSettlementPointId:int = None,
                        function = "list"
):
        """
        #Registration
        LÜY Sayaç Listeleme

        ---------
        LÜY Sayaçların kayıt detaylarını döner.

        İlgili Sayfa
        ---------
        https://epys.epias.com.tr/registration-operations/meter-operations/uleg-meter-list

        Parametre 
        ---------
         - id:int = None,
         - effectiveDate:tuple = None,
         - eic:str = None,
         - mainMeterId:int = None,
         - readingOrganizationId:int = None,
         - recordUsageStatusId:int = 1, # Mevcut Durum: 1 Kullanımda, 2 Kullanım dışı
         - statusId:int = 2, #Durum: 2 Aktif, 3 Pasif
         - substationId:int = None, # Trafo Merkezi
         - supplySettlementPointId:int = None,
         - supplyDeductionSettlementPointId:int = None,
                
        Notlar
        ---------
         - Eğer ID girilirse diğer parametreler boş olabilir.
         - Eğer ID girilmezse zorunlu parametrelerin doldurulması gerekir.
         - contains'ler eklenmedi.
        """

        if effectiveDate != None:
            effectiveDate= tuple_to_datetime(effectiveDate)
            if effectiveDate == False:
                return

            
        if function == "list":
            path = "https://epys{}.epias.com.tr/grid/v1/uleg-meter/query".format(self.test_coef)
        else:
            print("Function is not defined")
            return
                    
        self.request_registrationmeter_data(path, {
                                    "effectiveDate":effectiveDate,
                        "id":id,
                        "eic":eic,
                        "mainMeterId":mainMeterId,
                        "organizationId":None if self.organizationId == 2 else self.organizationId,
                        "readingOrganizationId":readingOrganizationId,
                        "recordUsageStatusId":recordUsageStatusId, # Mevcut Durum: 1 Kullanımda, 2 Kullanım dışı
                        "statusId":statusId, #Durum: 2 Aktif, 3 Pasif
                        "substationId":substationId, # Trafo Merkezi
                        "supplySettlementPointId":supplySettlementPointId,
                        "supplyDeductionSettlementPointId":supplyDeductionSettlementPointId,

            "page": {'number': self.page, 'size': 10000}})


        
        if self.final_response != None:
            self.formatted_final_response = self.format_files_registrationmeter(function)
            return self.formatted_final_response



    def registration_uevcb_data(self,
                        id:int = None,
                        effectiveDate:tuple = None,
                        eic:str = None,
                        name:str = None,
                        greenTariffTypeIds:list =  [],
                        balancingMarketParticipationStatusIds:list =  [],
                        powerPlantEffectiveId:int = None,
                        recordStatusIds:list = [],
                        statusIds:list = [], 
                        typeIds:list = [],

                        function = "list"
):
        """
        #Registration
        UEVÇB Listeleme
        ---------
        Sayaçların kayıt detaylarını döner.

        İlgili Sayfa
        ---------
        https://epys.epias.com.tr/registration-operations/settlement-withdrawal-unit-operations/settlement-withdrawal-unit-list

        Parametre 
        ---------
         - id:int = None,
         - effectiveDate:tuple = None,
         - eic:str = None,
         - name:str = None,
         - greenTariffTypeIds:list =  [], ## YETA [1,2,3,4,5,6,7,8,9]
         - balancingMarketParticipationStatusIds:list =  [], 2 Katılıyor, 3 Katılmıyor
         - powerPlantEffectiveId:int = None, Santral
         - recordStatusIds:list = [], # Mevcut Durum: 1 Kullanımda, 2 Kullanım dışı
         - statusIds:list = [], #Durum: 2 Aktif, 3 Pasif
         - typeIds:list = [],
            - typeIds => {
                0: Sanal
                1: Dengelemeye Dahil Olmayan Üretim Birimi
                2: Dengeleme Birimi
                3: Serbest Tüketici
                4: Otoproduktor Tüketim Tesisi
                5: Dağıtım Bölgesi
                7: Otoproduktor Grup Ortağı
                8: Santral İç Tüketimi
                10: İki Bölge Arasında Koridor
                11: Serbest Tüketici (OSB)
                12: YEKDEM Kapsamındaki Lisanslı Üretim Birimi
                13: YEKDEM Kapsamındaki Lisanssız Üretim Birimi
                14: ST Olmayan Tüketiciler
                15: Perakende Müşterisi Olan Dağıtımdan Bağlı Serbest Tüketiciler
                16: Tedarikçiden Perakendeye Dönen Dağıtımdan Bağlı Serbest Tüketiciler
                17: Perakende Müşterisi Olan İletimden Bağlı Serbest Tüketiciler
                18: Tedarikçiden Perakendeye Dönen İletimden Bağlı Serbest Tüketiciler
                20: Sıfır Bakiye Çekişlerinin Tutulduğu UEVÇB
                21: YEKDEM Dengeleme Birimi
                22: YEKDEM Üretim Birimi
                23: LÜY
                24: TEİAŞ - İç İhtiyaç
                25: YETA
                26: İç İhtiyaç – Diğer
                27: İthalat - İhracat
                28: TEİAŞ - İSKK
                29: Aydınlatma
                }

        Notlar
        ---------
         - Yok.
        """

        if effectiveDate != None:
            effectiveDate= tuple_to_datetime(effectiveDate)
            if effectiveDate == False:
                return

            
        if function == "list":
            path = "https://epys{}.epias.com.tr/registration/v1/sae/query".format(self.test_coef)
        else:
            print("Function is not defined")
            return
                    
        self.request_registrationmeter_data(path, {
                                    "effectiveDate":effectiveDate,
                        "effectiveId":id,
                        "eic":eic,
                        "name":name,
                        "organizationEffectiveId":None if self.organizationId == 2 else self.organizationId,
                        "greenTariffTypeIds":greenTariffTypeIds,
                        "balancingMarketParticipationStatusIds":balancingMarketParticipationStatusIds,
                        "powerPlantEffectiveId":powerPlantEffectiveId,
                        "recordStatusIds":recordStatusIds,
                        "statusIds":statusIds,
                        "typeIds": typeIds,

            "page": {'number': self.page, 'size': 10000}})

        
        if self.final_response != None:
            self.formatted_final_response = self.format_files_registrationmeter(function)
            return self.formatted_final_response

    def registration_powerplant_data(self,
                        id:int = None,
                        #idContains: null,
                        installedPowerMax:float = None,
                        installedPowerMin:float = None,
                        licenseNumber:str = None,
                        licenseTypeIds:list =  [], 
                        # 11: Üretim Lisansı
                        # 8 : OSB Üretim Lisansı
                        # 9 : İletim Lisansı
                        # 12: Tedarik Lisansı
                        # 13: Dağıtım Lisansı
                        # 7 : OSB Dağıtım Lisansı
                        # 14: Şarj Ağı Lisansı



                        effectiveDate:tuple = None,
                        eic:str = None,
                        name:str = None,

                        recordStatusIds:list = [],
                        rsmStatusIds:list = [0, 1, 2], # Kayıtlı, Kayıtsız, YEKA
                        sourceGroupIds:list = [], # [0,1,2] ...
                        sourceTypeIds:list = [] , # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 31, 32, 33, 41, 43, 44, 48, 49, 50, 53, 54, 141, 12]
                        trimmingStatusIds:list = [], # 0 , 1

                        statusIds:list = [], 
                        typeIds:list = [],

                        function = "list"
):

        
        """
        #Registration
        Santral Listeleme
        ---------
        Santrallerin kayıt detaylarını döner.

        İlgili Sayfa
        ---------
        https://epys.epias.com.tr/registration-operations/power-plant-operations/power-plant-operation-list

        Parametre 
        ---------
         - id:int = None,
         - effectiveDate:tuple = None,
         - eic:str = None,
         - name:str = None,
         - greenTariffTypeIds:list =  [], ## YETA [1,2,3,4,5,6,7,8,9]
         - balancingMarketParticipationStatusIds:list =  [], 2 Katılıyor, 3 Katılmıyor
         - powerPlantEffectiveId:int = None, Santral
         - recordStatusIds:list = [], # Mevcut Durum: 1 Kullanımda, 2 Kullanım dışı
         - statusIds:list = [], #Durum: 2 Aktif, 3 Pasif
         - typeIds:list = [],
            - typeIds => {
                0: Sanal
                1: Dengelemeye Dahil Olmayan Üretim Birimi
                2: Dengeleme Birimi
                3: Serbest Tüketici
                4: Otoproduktor Tüketim Tesisi
                5: Dağıtım Bölgesi
                7: Otoproduktor Grup Ortağı
                8: Santral İç Tüketimi
                10: İki Bölge Arasında Koridor
                11: Serbest Tüketici (OSB)
                12: YEKDEM Kapsamındaki Lisanslı Üretim Birimi
                13: YEKDEM Kapsamındaki Lisanssız Üretim Birimi
                14: ST Olmayan Tüketiciler
                15: Perakende Müşterisi Olan Dağıtımdan Bağlı Serbest Tüketiciler
                16: Tedarikçiden Perakendeye Dönen Dağıtımdan Bağlı Serbest Tüketiciler
                17: Perakende Müşterisi Olan İletimden Bağlı Serbest Tüketiciler
                18: Tedarikçiden Perakendeye Dönen İletimden Bağlı Serbest Tüketiciler
                20: Sıfır Bakiye Çekişlerinin Tutulduğu UEVÇB
                21: YEKDEM Dengeleme Birimi
                22: YEKDEM Üretim Birimi
                23: LÜY
                24: TEİAŞ - İç İhtiyaç
                25: YETA
                26: İç İhtiyaç – Diğer
                27: İthalat - İhracat
                28: TEİAŞ - İSKK
                29: Aydınlatma
                }

        Notlar
        ---------
         - Yok.
        """

        if effectiveDate != None:
            effectiveDate= tuple_to_datetime(effectiveDate)
            if effectiveDate == False:
                return

            
        if function == "list":
            path = "https://epys{}.epias.com.tr/registration/v1/power-plant/query".format(self.test_coef)
        else:
            print("Function is not defined")
            return
                    
        self.request_registrationmeter_data(path, {
                                    "effectiveDate":effectiveDate,
                        "eic":eic,
                        "id":id,
                        "name":name,
                        
                        "installedPowerMax": installedPowerMax,
                        "installedPowerMin":installedPowerMin,
                        "licenseNumber":licenseNumber,
                        "licenseTypeIds": licenseTypeIds,

                        "organizationId":None if self.organizationId == 2 else self.organizationId,
                        "recordStatusIds":recordStatusIds,
                        "rsmStatusIds":rsmStatusIds,
                        "sourceGroupIds": sourceGroupIds,
                        "sourceTypeIds": sourceTypeIds,
                        "statusIds":statusIds,
                        "trimmingStatusIds": trimmingStatusIds,
                        "typeIds":typeIds,

            "page": {'number': self.page, 'size': 10000}})

        
        if self.final_response != None:
            self.formatted_final_response = self.format_files_registrationmeter(function)
            return self.formatted_final_response


