from theohe_epias.transparency.data.reports import Reports
from theohe_epias.transparency.data.dam import DAM
from theohe_epias.transparency.data.idm import IDM
from theohe_epias.transparency.data.bpm import BPM
from theohe_epias.transparency.data.ancillary_services import AS
from theohe_epias.transparency.data.bilateral_contracts import BC
from theohe_epias.transparency.data.imbalance import IB
from theohe_epias.transparency.data.general_data import GD
from theohe_epias.transparency.data.production import Production
from theohe_epias.transparency.data.consumption import Consumption
from theohe_epias.transparency.data.renewables import Renewables
from theohe_epias.transparency.data.transmission import Transmission
from theohe_epias.transparency.data.dams import Dams
from theohe_epias.transparency.data.mms import MMS
from theohe_epias.transparency.data.yekg import YEKG
from theohe_epias.transparency.data.pfm import PFM

class WebServiceTransparency():
    def __init__(self):
        self.reports = Reports()
        self.dam = DAM()        
        self.idm = IDM()        
        self.bpm = BPM()
        self.ancillary_services = AS()
        self.bilateral_contracts = BC()
        self.imbalance = IB()
        self.general_data = GD()
        self.production = Production()
        self.consumption = Consumption()
        self.renewables = Renewables()
        self.transmission = Transmission()
        self.dams = Dams()
        self.mms = MMS()        
        self.yekg = YEKG()
        self.pfm = PFM()

        self.services = ['ancillary_services', 'bilateral_contracts', 'bpm', 'consumption', 'dam', 'dams', 'general_data', 'idm', 'imbalance', 'mms', 'pfm', 'production', 'renewables', 'reports', 'transmission', 'yekg']
