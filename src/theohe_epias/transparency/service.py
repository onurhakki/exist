from .data.dam import DAM
from .data.idm import IDM
from .data.pfm import PFM
from .data.ancillary_services import AS
from .data.bilateral_contracts import BC
from .data.bpm import BPM
from .data.yekg import YEKG
from .data.imbalance import IB
from .data.dams import Dams
from .data.general_data import GD
from .data.mms import MMS
from .data.renewables import Renewables
from .data.transmission import Transmission
from .data.consumption import Consumption
from .data.production import Production
from .data.reports import Reports


from requests import post, request
from json import dumps
from getpass import getpass
from pwinput import pwinput
import sys

import requests
import pandas as pd
from .utils.time_format import tuple_to_datetime
import re
import warnings


class Auth():
    def request_TGT(self, password):
        try:
            if password == None:
                password = self.type_password()
                if password == "q":
                    print("Exited.")
                    self.status  = False
                    self.tgt_response = "Exited"
                    return None

            self.tgt_request = post(
                self.cas_url, 
                params={
                    "username": self.username,
                    "password": password,
                    "format": "text"
                },
                headers = {
                    "Cache-Control": "no-cache",
                    "Accept": "text/plain",

                    "Content-Type": "application/x-www-form-urlencoded"
                })
            
            self.status  = self.check_password()
            self.tgt_response = self.tgt_request.text
        except Exception as e:
            raise e 

    def type_password(self):
        print("Enter your password: (q for quit)")

        if sys.__stdin__.isatty():
            password = pwinput()
        else:
            password = getpass('Password:')
        return password


    def check_password(self):
        if str(self.tgt_request.status_code)[0] != "2":
            print("Login is failed.")
            print(self.tgt_request.text)
            return False
        else:
            print("Successful login")
            return True
        
class WebServiceTransparency(
    Auth
    ):
    services = ['ancillary_services', 'bilateral_contracts', 'bpm', 'consumption', 'dam', 'dams', 'general_data', 'idm', 'imbalance', 'mms', 'pfm', 'production', 'renewables', 'reports', 'transmission', 'yekg']
    region = "TR1"
    def __init__(self, username, test = None, password = None):
        self.username = username
        self.cas_url = 'https://giris.epias.com.tr/cas/v1/tickets' if test == None else f'https://giris-{test}.epias.com.tr/cas/v1/tickets'
        self.root_url = 'https://seffaflik.epias.com.tr/' if test == None else f'https://seffaflik-{test}.epias.com.tr/'
        
        if password != None:
            self.login(password)


    def login(self, password = None):
        self.request_TGT(password)

    @property
    def ancillary_services(self):
        return AS(self.root_url, self)    

    @property
    def bilateral_contracts(self):
        return BC(self.root_url, self)    

    @property
    def bpm(self):
        return BPM(self.root_url, self)  
      
    @property
    def consumption(self):
        return Consumption(self.root_url, self)    

    @property
    def dam(self):
        return DAM(self.root_url, self)    
        
    @property
    def dams(self):
        return Dams(self.root_url, self)
    
    @property
    def general_data(self):
        return GD(self.root_url, self)    

    @property
    def idm(self):
        return IDM(self.root_url, self)    
        
    @property
    def imbalance(self):
        return IB(self.root_url, self)    
    
    @property
    def mms(self):
        return MMS(self.root_url, self)    
        
    @property
    def pfm(self):
        return PFM(self.root_url, self)    
        
    @property
    def production(self):
        return Production(self.root_url, self)    
        
    @property
    def renewables(self):
        return Renewables(self.root_url, self)    
        
    @property
    def reports(self):
        return Reports(self.root_url, self)    

        
    @property
    def transmission(self):
        return Transmission(self.root_url, self)    

    @property
    def yekg(self):
        return YEKG(self.root_url, self)    


    @staticmethod
    def get_url(main_url, information, attr, function):
        if function in ["export","list"]:
            url = main_url + information["data"][attr][function]
            return url
        else:
            print("Not Defined Function.")
            return None
    
    @staticmethod
    def control_time_between(url, startDate, endDate):
        startDate_tuple = tuple_to_datetime(startDate, string_=False)
        endDate_tuple = tuple_to_datetime(endDate, string_=False)
        check = True if startDate_tuple <= endDate_tuple else False
        if check == False:
            print("EndDate has to be greater or equal to StartDate.")
        if url == None or startDate_tuple == False or endDate_tuple == False or check == False:
            return False
        else:
            startDate = tuple_to_datetime(startDate, string_=True)
            endDate = tuple_to_datetime(endDate, string_=True)
            return [startDate, endDate]
    
    @staticmethod
    def control_time(url, date, hour = 0):
        date = tuple_to_datetime(date, hour= hour)
        if url == None or date == False:
            return False
        else:
            return date

    @staticmethod
    def request_data(url, data, function, headers, information):
        if function == "list":
            try:
                return requests.post(url, json=data, headers=headers).json()
            except Exception as e:
                raise e
            # except:
            #     try:
            #         return requests.get(url, json=data, headers=headers).json()            
            #     except Exception as e:
            #         raise e
            
        if function == "export":
            data["exportType"] = "XLSX"
            val = requests.post(url, json=data, headers=headers)
            try:
                with warnings.catch_warnings():
                    warnings.filterwarnings("ignore", category=UserWarning, module=re.escape('openpyxl.styles.stylesheet'))
                    res = pd.read_excel(val.content)
                    res = res.rename(columns = information["rename_columns"]) 
                    return res
            except Exception as e:
                print(val.json()["errors"])
                raise e
            
    @staticmethod
    def request_data_get(url, data, function, headers, information):
        if function == "list":
            try:
                return requests.get(url, json=data, headers=headers).json()
            except Exception as e:
                raise e
            # except:
            #     try:
            #         return requests.get(url, json=data, headers=headers).json()            
            #     except Exception as e:
            #         raise e
            

        #     if url in ["https://seffaflik.epias.com.tr/electricity-service/v1/markets/dam/data/interim-mcp-published-status"]:
        #         return requests.get(url, json=data).json()
        #     else:
                



# class WebServiceTransparency():
#     def __init__(self):
#         # self.reports = Reports()
#         # self.idm = IDM()        
#         # self.bpm = BPM()
#         # self.ancillary_services = AS()
#         # self.bilateral_contracts = BC()
#         # self.imbalance = IB()
#         # self.general_data = GD()
#         # self.production = Production()
#         # self.consumption = Consumption()
#         # self.renewables = Renewables()
#         # self.transmission = Transmission()
#         # self.dams = Dams()
#         # self.mms = MMS()        
#         # self.yekg = YEKG()
#         # self.pfm = PFM()



