# Energy Exchange Istanbul (EXIST)

Energy Exchange Istanbul (EXIST) or Enerji Piyasaları İşletme A.Ş. (EPİAŞ) by its Turkish name is an energy exchange company.

## Services

 - Transparency Platform (Şeffaflık Platformu)
 - EMMS (Energy Markets Management System) - EPYS (Enerji Piyasaları Yönetim Sistemi)

### download via pip

```
!pip install theohe-epias
```

## Transparency Platform (Şeffaflık Platformu)

Transparency Platform provides necessary data for the transparent, reliable, fair and predictable operation of energy markets. You can access platform from [here](https://seffaflik.epias.com.tr/home).

Also, Transparency API is available for everyone. In the [Notebook](https://github.com/onurhakki/exist/blob/main/example-notebooks/Transparency%20WebService.ipynb), you can access example details.

### usage - (example: Market Clearing Price (MCP) - Piyasa Takas Fiyatı (PTF))

```
from theohe_epias.transparency.service import WebServiceTransparency
ws = WebServiceTransparency()
ws.dam.mcp()
```


### usage - between selected dates (example: Market Clearing Price (MCP) - Piyasa Takas Fiyatı (PTF))

```
from theohe_epias.transparency.service import WebServiceTransparency
ws = WebServiceTransparency()
ws.dam.mcp(startDate=(2023, 12, 1), endDate=(2023, 12, 31), function = "export")
```


### usage - (example: Market Clearing Price (MCP))

##### 2023 MCP hourly averages on monthly basis

In the [Notebook](https://github.com/onurhakki/exist/blob/main/example-notebooks/Transparency%20WebService%20(MCP%20-%20SMP%20-%20Direction).ipynb), you can access example details.


![mcp_2023](https://github.com/onurhakki/exist/assets/53830179/54c7390c-cc11-4230-9e40-ceda4a1f0592)


### usage - (example: System's Direction)

##### 2023 System's Direction averages on monthly basis

In the [Notebook](https://github.com/onurhakki/exist/blob/main/example-notebooks/Transparency%20WebService%20(MCP%20-%20SMP%20-%20Direction).ipynb), you can access example details.


![direction_2023](https://github.com/onurhakki/exist/assets/53830179/8f19d58e-344e-4253-aa69-8217f1b84113)


## EPYS (Enerji Piyasaları Yönetim Sistemi) - EMMS (Energy Markets Management System)

You can access platform from [here](https://epys.epias.com.tr/home).

Also, EPYS is only available for market participants. In the [Notebook](https://github.com/onurhakki/exist/blob/main/example-notebooks/EPYS%20WebService%20.ipynb), you can access example details.

### usage - login 

```
from theohe_epias.epys.service import WebServiceEPYS
import warnings

warnings.simplefilter("ignore")

ws = WebServiceEPYS(username = "USERNAME", organizationId = 123456789, test=None)
### None for prod
### "prp" for test
ws.login()
### or directly use below code
### ws.login("password")
```

