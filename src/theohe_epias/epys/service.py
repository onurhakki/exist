
from ..epys.utils.tgt import RequestFunctions

from ..epys.invoice.data import Invoice

from ..epys.reconciliation.settlement import Settlement
from ..epys.reconciliation.reports import Reports
from ..epys.reconciliation.settlementdata import SettlementData
from ..epys.reconciliation.advance import Advance
from ..epys.reconciliation.imbalance import Imbalance


from ..epys.registration.registrationmeter import RegistrationMeter

from ..epys.eligible_customer.eligible_customer_meter import EligibleCustomerMeter

from ..epys.unlicensed.luytob_control import LUYTOB


class WebServiceEPYS(
    RequestFunctions, 
    Invoice, 
    Settlement, Reports, SettlementData, Advance, Imbalance,
    RegistrationMeter,
    EligibleCustomerMeter,
    LUYTOB
    ): 
    def __init__(self, username, organizationId, test = None):
        """
        
        If you are tring to list data more than 10000 rows, you have to use page value and request again.
        
        """
        self.username = username
        self.status = False
        
        self.page = 1
        
        if test == None:
            self.url = 'https://cas.epias.com.tr/cas/v1/tickets'
            self.test_coef = ""
        else:
            if test in ["prp", "qa", "uat"]:
                if test == "prp":
                    self.url = 'https://testcas.epias.com.tr/cas/v1/tickets'
                else:
                    self.url = 'https://cas-{}.epias.com.tr/cas/v1/tickets'.format(test)
                self.test_coef = "-"+test

            else:
                print("Not valid test id. ({})".format(test))
                self.test_coef = None
        self.organizationId = organizationId
        self.final_response = None

        self.services = dict({
            "reconciliation":{
                "advance": ["advance"],
                "invoice": ["invoice_notice_invoice_item_with_tax"],
                "settlement": ['invoice_notice', 'invoice_notice_daily', 'invoice_notice_hourly'],
                "reports": ['settlement_point_data', 'settlement_point_meter_data'],
                "settlementdata" : ["meter_data_approved_meter_data"],
                },
            "registration":{
                "registrationmeter": ["registration_meter_data"]
            }
            })

    def login(self, password = None):
        self.request_TGT(password)

    def check_response(self, final_response):
        if str(final_response.status_code)[0] != "2":
            print("Request is failed.")
            for i in final_response.json()["errors"]:
                print(i["errorMessage"])
                return False
        else:
            return True
