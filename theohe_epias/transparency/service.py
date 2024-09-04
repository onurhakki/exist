from ..transparency.data.reports import Reports
from ..transparency.data.dam import DAM
from ..transparency.data.idm import IDM
from ..transparency.data.bpm import BPM
from ..transparency.data.ancillary_services import AS
from ..transparency.data.bilateral_contracts import BC
from ..transparency.data.imbalance import IB
from ..transparency.data.general_data import GD
from ..transparency.data.production import Production
from ..transparency.data.consumption import Consumption
from ..transparency.data.renewables import Renewables
from ..transparency.data.transmission import Transmission
from ..transparency.data.dams import Dams
from ..transparency.data.mms import MMS
from ..transparency.data.yekg import YEKG
from ..transparency.data.pfm import PFM

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
