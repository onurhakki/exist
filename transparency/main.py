

from dataset.create import read_json
from service.details import show_information, create_link
from service.control import service_check
from requests import get
import pandas as pd


service = read_json(export = True)
# 'path', 'bulletin', 'compare', 'consumption', 'dam', 'market', 'mobile', 'production', 'stp-transmission', 'stp', 'transmission', 'vep', 'vgp', 'yekdem', 'yekg'

service1, service2 = "consumption", "getDistrubitonCompany"

try:
    check = service_check(service, service1, service2)
    if check:
        detail = service[service1][service2]
        show_information(detail)
    else:
        pass
except Exception as e:
    print("Error:")
    print(e)


payload = dict({
    "date": "2022-01-01",
    "startDate":"2022-01-01",
    "endDate":"2022-05-03"})

api_link  = create_link(detail, payload)
print(api_link)

response = get(api_link)
print(pd.DataFrame(list(response.json()['body'].values())[0]))
