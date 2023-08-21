
information = {
    'advance-detail' : ['list'],
    'advance' : ['export', 'list'],
    'bilateral-contract-detail' : ['export', 'list'],
    'bilateral-contract' : ['export', 'list'],
    'market-day-ahead-market-daily' : ['export', 'list'],
    'market-day-ahead-market' : ['export', 'list'],
    'market-day-ahead-market-gap-amount' : ['list'],
    'market-day-ahead-market-mcp' : ['list'],
    'market-intraday-market-daily' : ['export', 'list'],
    'market-intraday-market' : ['export', 'list']
    }

dataset = {
    "advance-detail": {
        "list": {
            "path": "https://epys.epias.com.tr/reconciliation-market/v1/advance/detail/list",
            "summary": "Avans Bildirim Detayını Görüntüle",
            "description": "Organizasyonların avas alacak borç detaylarını döner.",
            "operation": "get-organization-advance-details",
            "required": {
                "paymentDateStart": "2023-01-01T00:00:00+03:00",
                "paymentDateEnd": "2023-01-31T23:00:00+03:00",
                "page": {
                    "number": 1,
                    "size": 10000
                }
            }
        }
    },
    "advance": {
        "export": {
            "path": "https://epys.epias.com.tr/reconciliation-market/v1/advance/export",
            "summary": "Avans Bildirim Detayını Görüntüle.",
            "description": "Organizasyonların avas alacak borç detaylarını excel export servisi.",
            "operation": "export-organization-advance-details",
            "required": {
                "paymentDateStart": "2023-01-01T00:00:00+03:00",
                "paymentDateEnd": "2023-01-31T23:00:00+03:00"
            }
        },
        "list": {
            "path": "https://epys.epias.com.tr/reconciliation-market/v1/advance/list",
            "summary": "Avans Bildirim Detayını Görüntüle",
            "description": "Organizasyonların avas alacak borç detaylarını döner.",
            "operation": "get-organization-advance",
            "required": {
                "paymentDateStart": "2023-01-01T00:00:00+03:00",
                "paymentDateEnd": "2023-01-31T23:00:00+03:00",
                "page": {
                    "number": 1,
                    "size": 10000
                }
            }
        }
    },
    "bilateral-contract-detail": {
        "export": {
            "path": "https://epys.epias.com.tr/reconciliation-market/v1/bilateral-contract/detail/export",
            "summary": "İkili Anlaşma Organizasyon Detay Version Dışarı Aktarma Servisi",
            "description": "Uzlaştırma dönemi bazından ikili anlaşma alış satış miktarlarını detaylarini export edilmesini yapar.",
            "operation": "export-organization-bilateral-contract-details",
            "required": {
                "effectiveDateStart": "2023-01-01T00:00:00+03:00",
                "effectiveDateEnd": "2023-01-31T23:00:00+03:00",
                "page": {
                    "number": 1,
                    "size": 10000
                }
            },
            "optional": {
                "targetOrganizationId": "ID in String or None"
            }
        },
        "list": {
            "path": "https://epys.epias.com.tr/reconciliation-market/v1/bilateral-contract/detail/list",
            "summary": "İkili Anlaşma Detay Servisi",
            "description": "Organizasyonların aralarında yapmış oldukları ikili anlaşma detaylarını döner.",
            "operation": "list-organization-bilateral-contract-details",
            "required": {
                "effectiveDateStart": "2023-01-01T00:00:00+03:00",
                "effectiveDateEnd": "2023-01-31T23:00:00+03:00",
                "page": {
                    "number": 1,
                    "size": 10000
                }
            },
            "optional": {
                "targetOrganizationId": "ID in String or None"
            }
        }
    },
    "bilateral-contract": {
        "export": {
            "path": "https://epys.epias.com.tr/reconciliation-market/v1/bilateral-contract/export",
            "summary": "İkili Anlaşma Dışarı Aktarma Servisi",
            "description": "Uzlaştırma dönemi bazından günlük toplam ikili anlaşma alış satış miktarlarını export edilmesini yapar.",
            "operation": "export-organization-bilateral-contract",
            "required": {
                "effectiveDateStart": "2023-01-01T00:00:00+03:00",
                "effectiveDateEnd": "2023-01-31T23:00:00+03:00",
                "page": {
                    "number": 1,
                    "size": 10000
                }
            }
        },
        "list": {
            "path": "https://epys.epias.com.tr/reconciliation-market/v1/bilateral-contract/list",
            "summary": "İkili Anlaşma Listeleme Servisi",
            "description": "Uzlaştırma dönemi bazından günlük toplam ikili anlaşma alış satış miktarlarını döner.",
            "operation": "list-organization-bilateral-contracts",
            "required": {
                "effectiveDateStart": "2023-01-01T00:00:00+03:00",
                "effectiveDateEnd": "2023-01-31T23:00:00+03:00",
                "page": {
                    "number": 1,
                    "size": 10000
                }
            }
        }
    },
    "market-day-ahead-market-daily": {
        "export": {
            "path": "https://epys.epias.com.tr/reconciliation-market/v1/market/day-ahead-market/daily/export",
            "summary": "GÖP Uzlaştırma Bildirimi Excele Aktarma (Saatlik Detay Ekranı)",
            "description": "Organizasyonların GÖP'de yapmış oldukları eşleşme detaylarını excel export işlemi.",
            "operation": "export-organization-dam-daily-transactions",
            "required": {
                "deliveryDayStart": "2023-01-01T00:00:00+03:00",
                "deliveryDayEnd": "2023-01-31T23:00:00+03:00",
                "region": "TR1"
            }
        },
        "list": {
            "path": "https://epys.epias.com.tr/reconciliation-market/v1/market/day-ahead-market/daily/list",
            "summary": "GÖP Uzlaştırma Bildirimini Görüntüle (Saatlik Detay Ekranı)",
            "description": "Organizasyonun gün öncesi piyasasındaki eşleşme sonuçlarını saatlik deatyını döner.",
            "operation": "get-organization-dam-daily-transactions",
            "required": {
                "deliveryDayStart": "2023-01-01T00:00:00+03:00",
                "deliveryDayEnd": "2023-01-31T23:00:00+03:00",
                "region": "TR1",
                "page": {
                    "number": 1,
                    "size": 10000
                }
            }
        }
    },
    "market-day-ahead-market": {
        "export": {
            "path": "https://epys.epias.com.tr/reconciliation-market/v1/market/day-ahead-market/export",
            "summary": "GÖP Uzlaştırma Bildirimi Excele Aktarma",
            "description": "Organizasyonların GÖP'de yapmış oldukları eşleşme detaylarını excel export işlemi.",
            "operation": "export-organization-dam-transaction-details",
            "required": {
                "deliveryDayStart": "2023-01-01T00:00:00+03:00",
                "deliveryDayEnd": "2023-01-31T23:00:00+03:00",
                "region": "TR1"
            }
        },
        "list": {
            "path": "https://epys.epias.com.tr/reconciliation-market/v1/market/day-ahead-market/list",
            "summary": "GÖP Uzlaştırma Bildirimi",
            "description": "Piyasa Katılımcılarının ilgili fatura döneminde GÖP sisteminde yaptıkları işlemlere ait Miktar ve Tutar bilgilerinin günlük bazda listelenmesidir. İhtiyaç halinde VEP Temerrüt Kaynaklı değerler de listelenebilmektedir.",
            "operation": "get-organization-dam-transactions",
            "required": {
                "deliveryDayStart": "2023-01-01T00:00:00+03:00",
                "deliveryDayEnd": "2023-01-31T23:00:00+03:00",
                "region": "TR1",
                "page": {
                    "number": 1,
                    "size": 10000
                }
            }
        }
    },
    "market-day-ahead-market-gap-amount": {
        "list": {
            "path": "https://epys.epias.com.tr/reconciliation-market/v1/market/day-ahead-market/gap-amount/list",
            "summary": "GÖP Uzlaştırma Bildirimini (Fark tutarını) Görüntüle (Saatlik Detay Ekranı).",
            "description": "Organizasyonun gün öncesi piyasasında fark fonu bilgilerini döner.",
            "operation": "get-organization-gap-amount-detail",
            "required": {
                "deliveryDayStart": "2023-01-01T00:00:00+03:00",
                "deliveryDayEnd": "2023-01-31T23:00:00+03:00",
                "region": "TR1",
                "page": {
                    "number": 1,
                    "size": 10000
                }
            }
        }
    },
    "market-day-ahead-market-mcp": {
        "list": {
            "path": "https://epys.epias.com.tr/reconciliation-market/v1/market/day-ahead-market/mcp/list",
            "summary": "Gün öncesi piyasasına ait PTF bilgilerini listeler.",
            "description": "Gün öncesi piyasasında oluşan piyasa takas fiyatı servisi.",
            "operation": "get-market-clearing-prices",
            "required": {
                "effectiveDateStart": "2023-01-01T00:00:00+03:00",
                "effectiveDateEnd": "2023-01-31T23:00:00+03:00"
            }
        }
    },
    "market-intraday-market-daily": {
        "export": {
            "path": "https://epys.epias.com.tr/reconciliation-market/v1/market/intraday-market/daily/export",
            "summary": "Organizasyonun güniçi piyasasındaki eşleşme sonuçlarını excel export servisi.",
            "description": "Organizasyonun güniçi piyasasındaki eşleşme sonuçlarını excel export servisi.",
            "operation": "export-organization-daily-idm-transactions",
            "required": {
                "deliveryDayStart": "2023-01-01T00:00:00+03:00",
                "deliveryDayEnd": "2023-01-31T23:00:00+03:00",
                "region": "TR1"
            }
        },
        "list": {
            "path": "https://epys.epias.com.tr/reconciliation-market/v1/market/intraday-market/daily/list",
            "summary": "Organizasyonun güniçi piyasasındaki eşleşme sonuçları",
            "description": "Organizasyonun güniçi piyasasındaki eşleşme sonuçlarını döner.",
            "operation": "get-organization-daily-idm-transactions",
            "required": {
                "deliveryDayStart": "2023-01-01T00:00:00+03:00",
                "deliveryDayEnd": "2023-01-31T23:00:00+03:00",
                "region": "TR1",
                "page": {
                    "number": 1,
                    "size": 10000
                }
            }
        }
    },
    "market-intraday-market": {
        "export": {
            "path": "https://epys.epias.com.tr/reconciliation-market/v1/market/intraday-market/export",
            "summary": "Organizasyonun güniçi piyasasındaki eşleşme sonuçlarını excel export servisi.",
            "description": "Organizasyonun güniçi piyasasındaki eşleşme sonuçlarını excel export servisi.",
            "operation": "export-organization-idm-transactions",
            "required": {
                "deliveryDayStart": "2023-01-01T00:00:00+03:00",
                "deliveryDayEnd": "2023-01-31T23:00:00+03:00",
                "region": "TR1"
            }
        },
        "list": {
            "path": "https://epys.epias.com.tr/reconciliation-market/v1/market/intraday-market/list",
            "summary": "Organizasyonun güniçi piyasasındaki eşleşme sonuçları",
            "description": "Organizasyonun güniçi piyasasındaki eşleşme sonuçlarını döner.",
            "operation": "get-organization-idm-transactions",
            "required": {
                "deliveryDayStart": "2023-01-01T00:00:00+03:00",
                "deliveryDayEnd": "2023-01-31T23:00:00+03:00",
                "region": "TR1",
                "page": {
                    "number": 1,
                    "size": 10000
                }
            }
        }
    }
}

        

