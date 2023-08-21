


import pandas as pd
pd.set_option('display.max_columns', None)
            
from service.main_service import WebService


ws = WebService(username = "USERNAME", organizationId = 123456789) ## Your Username and Organization ID
ws.login("PASSWORD") ## Your Password


ws.market_day_ahead_market()


res= ws.settlement_point_meter_data(
    period=(2023,4),
    version=(2023,4),
    function = "export")

print(res)

