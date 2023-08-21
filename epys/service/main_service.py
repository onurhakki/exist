
from data.mof import MOF
from data.market import Market
from data.precon import Precon

from service.tgt import RequestFunctions

class WebService(RequestFunctions, MOF, Market, Precon): #, 
    def __init__(self, username, organizationId):
        """
        
        If you are tring to list data more than 10000 rows, you have to use page value and request again.
        
        """
        self.username = username
        self.status = False
        
        self.page = 1

        self.url = 'https://cas.epias.com.tr/cas/v1/tickets'
        self.organizationId = organizationId
        self.final_response = None

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
