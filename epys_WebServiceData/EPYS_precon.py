information = {
'meter-data-approved-meter-data' : ['export', 'list'] ,
'meter-data-approved-meter-data-hourly' : ['export', 'list'] ,
'meter-data-approved-meter-data-hourly-get' : ['list'] ,
'meter-data-approved-meter-data-profile-coefficient-get' : ['list'] ,
'meter-data-approved-meter-data-profile' : ['export', 'list'] ,
'meter-data-approved-meter-data-profile-get' : ['list'] ,
'meter-data-approved-meter-data-total' : ['list'] ,
'meter-data-approved-profile-meter-data' : ['export', 'list'] ,
'settlement-point-data' : ['export', 'list',] ,
'settlement-point-meter-data' : ['export', 'list'] ,
    }

dataset = {
    "meter-data-approved-meter-data": {
        "export": {
            "path": "https://epys.epias.com.tr/pre-reconciliation/v1/meter-data/approved-meter-data/export",
            "summary": "Sayaç Veri Listesi Export Servisi",
            "description": "Sayaç Veri Listesi Export",
            "operation": "export-meter-data",
            "required": {
                "period": "2023-01-01T00:00:00+03:00",
                "version": "2023-02-01T00:00:00+03:00",
                "region": "TR1",
                "isRetrospective": False,
                "organization": "Org ID"
            },
            "optional": {
                "meterIds": [],
                "readStatus": True,
                "meterReadingCompany": "653",
                "meterReadingType": "HOURLY",
                "usageType": "3"
            }
        },
        "list": {
            "path": "https://epys.epias.com.tr/pre-reconciliation/v1/meter-data/approved-meter-data/list",
            "summary": "Onaylı Sayaçların Sayaç Okunma Durumları",
            "description": "Onaylı sayaçların sayaç okunma durumlarına göre verilerini listeler.",
            "operation": "list-meter-datas",
            "required": {
                "period": "2023-01-01T00:00:00+03:00",
                "version": "2023-02-01T00:00:00+03:00",
                "region": "TR1",
                "isRetrospective": False,
                "organization": "Org ID",
                "page": {
                    "number": 1,
                    "size": 10000
                }
            },
            "optional": {
                "meterIds": [],
                "readStatus": True,
                "meterReadingCompany": "653",
                "meterReadingType": "HOURLY",
                "usageType": "3"
            }
        }
    },
    "meter-data-approved-meter-data-hourly": {
        "export": {
            "path": "https://epys.epias.com.tr/pre-reconciliation/v1/meter-data/approved-meter-data/hourly/export",
            "summary": "Saatlik Sayaç Verileri Detay Export Servisi",
            "description": "Saatlik Sayaç Verileri Detaylarının Excel veya CSV olarak indirilmesini sağlar.",
            "operation": "export-hourly-meter-data-details",
            "required": {
                "period": "2023-01-01T00:00:00+03:00",
                "meterId": "TR1",
                "organization": "Org ID",
                "page": {
                    "number": 1,
                    "size": 10000
                }
            },
            "optional": {
                "version": "2023-02-01T00:00:00+03:00"
            }
        },
        "list": {
            "path": "https://epys.epias.com.tr/pre-reconciliation/v1/meter-data/approved-meter-data/hourly/list",
            "summary": "Saatlik Sayaç Verileri Listeleme Servisi",
            "description": "Katılımcılara veya sayaç okuyan kurumlara ait saatlik sayaçların veriş/çekiş değerlerini topluca aldıkları servis",
            "operation": "list-hourly-meter-datas",
            "required": {
                "effectiveDateStart": "2022-08-01T00:00:00+03:00",
                "effectiveDateEnd": "2022-08-05T00:00:00+03:00",
                "meterId": "TR1",
                "organization": "Org ID",
                "page": {
                    "number": 1,
                    "size": 10000
                }
            },
            "optional": {
                "version": "2023-02-01T00:00:00+03:00"
            }
        }
    },
    "meter-data-approved-meter-data-hourly-get": {
        "list": {
            "path": "https://epys.epias.com.tr/pre-reconciliation/v1/meter-data/approved-meter-data/hourly/get",
            "summary": "Saatlik Sayaç Verileri Detay Servisi",
            "description": "Sisteme yüklenen saatlik sayaçların verilerini listeler.",
            "operation": "get-hourly-meter-data-details",
            "required": {
                "period": "2022-08-01T00:00:00+03:00",
                "meterId": "1",
                "organization": "Org ID",
                "page": {
                    "number": 1,
                    "size": 10000
                }
            },
            "optional": {
                "version": "2023-02-01T00:00:00+03:00"
            }
        }
    },
    "meter-data-approved-meter-data-profile-coefficient-get": {
        "list": {
            "path": "https://epys.epias.com.tr/pre-reconciliation/v1/meter-data/approved-meter-data/profile-coefficient/get",
            "summary": "Sayaç Katsayı Detayları Servisi",
            "description": "Sayaç Katsayı Detayları",
            "operation": "get-profile-coefficient-data-detail",
            "required": {
                "period": "2022-08-01T00:00:00+03:00",
                "version": "2022-08-01T00:00:00+03:00",
                "meterId": "1",
                "organization": "Org ID",
                "page": {
                    "number": 1,
                    "size": 10000
                }
            }
        }
    },
    "meter-data-approved-meter-data-profile": {
        "export": {
            "path": "https://epys.epias.com.tr/pre-reconciliation/v1/meter-data/approved-meter-data/profile/export",
            "summary": "Üç veya Tek Zamanlı Sayaç Veri Detay Export Servisi",
            "description": "Üç veya Tek Zamanlı sayacın detay verilerinin excel yada csv olarak indirilmesini sağlar.",
            "operation": "export-profile-meter-data-detail",
            "required": {
                "period": "2022-08-01T00:00:00+03:00",
                "version": "2022-08-01T00:00:00+03:00",
                "meterId": "1",
                "organization": "Org ID"
            }
        },
        "list": {
            "path": "https://epys.epias.com.tr/pre-reconciliation/v1/meter-data/approved-meter-data/profile/list",
            "summary": "Üç ve Tek Zamanlı Sayaç Verileri Listeleme Servisi",
            "description": "Katılımcılara veya sayaç okuyan kurumlara ait üç ve tek zamanlı sayaçların çekiş değerlerini topluca aldıkları servis.",
            "operation": "list-profile-meter-data",
            "required": {
                "period": "2022-08-01T00:00:00+03:00",
                "version": "2022-08-01T00:00:00+03:00",
                "meterId": "1",
                "organization": "Org ID",
                "page": {
                    "number": 1,
                    "size": 10000
                }
            }
        }
    },
    "meter-data-approved-meter-data-profile-get": {
        "list": {
            "path": "https://epys.epias.com.tr/pre-reconciliation/v1/meter-data/approved-meter-data/profile/get",
            "summary": "Üç veya Tek Zamanlı Sayaç Veri Detay Servisi",
            "description": "Üç veya Tek Zamanlı sayacın detay verilerini listeler.",
            "operation": "get-profile-meter-data-detail",
            "required": {
                "period": "2022-08-01T00:00:00+03:00",
                "meterId": "1",
                "organization": "Org ID",
                "page": {
                    "number": 1,
                    "size": 10000
                }
            },
            "optional": {
                "version": "2022-08-01T00:00:00+03:00"
            }
        }
    },
    "meter-data-approved-meter-data-total": {
        "list": {
            "path": "https://epys.epias.com.tr/pre-reconciliation/v1/meter-data/approved-meter-data/total",
            "summary": "Toplam Onaylı Sayaç Verileri Servisi",
            "description": "Organizasyonun toplam aylık veriş, çekiş ve tenizl değerlerini döner.",
            "operation": "get-total-data",
            "required": {
                "period": "2022-08-01T00:00:00+03:00",
                "page": {
                    "number": 1,
                    "size": 10000
                }
            }
        }
    },
    "meter-data-approved-profile-meter-data": {
        "export": {
            "path": "https://epys.epias.com.tr/pre-reconciliation/v1/meter-data/approved-profile-meter-data/export",
            "summary": "Sayaç Veri Listesi Export Servisi",
            "description": "Sayaç Veri Listesi Export",
            "operation": "export-meter-data",
            "required": {
                "period": "2022-08-01T00:00:00+03:00",
                "page": {
                    "number": 1,
                    "size": 10000
                }
            }
        },
        "list": {
            "path": "https://epys.epias.com.tr/pre-reconciliation/v1/meter-data/approved-profile-meter-data/list",
            "summary": "Onaylı Sayaçların Sayaç Okunma Durumları",
            "description": "Onaylı sayaçların sayaç okunma durumlarına göre verilerini listeler.",
            "operation": "list-meter-datas",
            "required": {
                "period": "2022-08-01T00:00:00+03:00",
                "page": {
                    "number": 1,
                    "size": 10000
                }
            }
        }
    },
    "settlement-point-data": {
        "list": {
            "path": "https://epys.epias.com.tr/pre-reconciliation/v1/settlement-point/data",
            "summary": "UEVÇB Verileri Listeleme Servisi",
            "description": "UEVÇB verilerini listeler.",
            "operation": "list-settlement-point-data",
            "required": {
                "period": "2022-08-01T00:00:00+03:00",
                "version": "2022-08-01T00:00:00+03:00",
                "region": "TR1",
                "effectiveDateStart": "2022-08-01T00:00:00+03:00",
                "effectiveDateEnd": "2022-08-05T23:00:00+03:00",
                "page": {
                    "number": 1,
                    "size": 10000
                }
            }
        },
        "export": {
            "path": "https://epys.epias.com.tr/pre-reconciliation/v1/settlement-point/data/export",
            "summary": "UEVÇB Verileri Export Servisi",
            "description": "UEVÇB verileri export servisi.",
            "operation": "export-settlement-point-data",
            "required": {
                "period": "2022-08-01T00:00:00+03:00",
                "version": "2022-08-01T00:00:00+03:00",
                "region": "TR1",
                "effectiveDateStart": "2022-08-01T00:00:00+03:00",
                "effectiveDateEnd": "2022-08-05T23:00:00+03:00"
            }
        }
    },
    "settlement-point-meter-data": {
        "export": {
            "path": "https://epys.epias.com.tr/pre-reconciliation/v1/settlement-point/meter-data/export",
            "summary": "UEVÇB'ye Bağlı Sayaçların Bilgilerini Listeleme Servisi",
            "description": "UEVÇB'ye Bağlı Sayaçların Bilgilerini Listeler.",
            "operation": "export-settlement-point-meter-details",
            "required": {
                "period": "2022-08-01T00:00:00+03:00",
                "region": "TR1"
            }
        },
        "list": {
            "path": "https://epys.epias.com.tr/pre-reconciliation/v1/settlement-point/meter-data/list",
            "summary": "UEVÇB'ye Bağlı Sayaçların Veriş-Çekiş Değerlerini Listeleme Servisi",
            "description": "UEVÇB'ye Bağlı Sayaçların Veriş-Çekiş Değerlerini Listeler.",
            "operation": "list-settlement-point-meter-details",
            "required": {
                "period": "2022-08-01T00:00:00+03:00",
                "region": "TR1"
            }
        }
    },
}