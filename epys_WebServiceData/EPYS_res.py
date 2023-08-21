
information = {
    'luy-invoice-upr-retro-correction' : ['export', 'list'] ,
    'luy-invoice-invoice' : ['export', 'list'] ,
    'luy-invoice-invoice-history' : ['export', 'list'] ,
    'payment-obligation-details' : ['export', 'list'] ,
    'payment-obligation' : ['export', 'list'] ,
    'res-retrospective-detail': ['export', 'list'] ,
    'res-retrospective' : ['export', 'list'] ,
    'res-unit-price' : ['export', 'list'] ,
    'rescostsettlement' : ['export', 'list'] ,
}

dataset =   {
    "luy-invoice-upr-retro-correction": {
        "export": {
            "path": "https://epys.epias.com.tr/reconciliation-res/v1/luy-invoice/export/upr/retro/correction",
            "summary": "LUY GDDK Değişim Raporu Listeleme",
            "description": "LUY GDDK değişim raporunu listeler.",
            "operation": "exportUprRetroCorrection",
            "required": {
                "period": "2023-01-01T00:00:00+03:00",
                "version": "2023-02-01T00:00:00+03:00",
                "region": "TR1"
            }
        },
        "list": {
            "path": "https://epys.epias.com.tr/reconciliation-res/v1/luy-invoice/list/upr/retro/correction",
            "summary": "LUY GDDK Değişim Raporu Listeleme",
            "description": "LUY GDDK değişim raporunu listeler.",
            "operation": "listUprRetroCorrection",
            "required": {
                "period": "2023-01-01T00:00:00+03:00",
                "version": "2023-02-01T00:00:00+03:00",
                "region": "TR1",
                "page": {
                    "number": 1,
                    "size": 10000
                }
            }
        }
    },

    "luy-invoice-invoice": {
        "export": {
            "path": "https://epys.epias.com.tr/reconciliation-res/v1/luy-invoice/invoice/export",
            "summary": "LUY Fatura Listeleme",
            "description": "Lisansız üretim yapan UEVCB'lere ait faturaları listeler.",
            "operation": "export-luy-invoices",
            "required": {
                "period": "2023-01-01T00:00:00+03:00",
                "region": "TR1"
            },
            "optional": {
                "settlementPointId": None
            }
        },
        "list": {
            "path": "https://epys.epias.com.tr/reconciliation-res/v1/luy-invoice/invoice/list",
            "summary": "LUY Fatura Listeleme",
            "description": "Lisansız üretim yapan UEVCB'lere ait faturaları listeler.",
            "operation": "get-luy-invoices",
            "required": {
                "period": "2023-01-01T00:00:00+03:00",
                "region": "TR1",
                "page": {
                    "number": 1,
                    "size": 10000
                }
            },
            "optional": {
                "settlementPointId": None
            }
        },
    },
    "luy-invoice-invoice-history": {
        "export": {
            "path": "https://epys.epias.com.tr/reconciliation-res/v1/luy-invoice/invoice/history/export",
            "summary": "LUY Fatura Geçmiş Listeleme",
            "description": "Lisanssız üretim yapan UEVCB'lere ait faturaların versiyon geçmişini listeler.",
            "operation": "export-luy-invoice-history",
            "required": {
                "period": "2023-01-01T00:00:00+03:00",
                "version": "2023-01-01T00:00:00+03:00",
                "region": "TR1",
                "settlementPointId": "UEVCB ID"
            }
        },
        "list": {
            "path": "https://epys.epias.com.tr/reconciliation-res/v1/luy-invoice/invoice/history/list",
            "summary": "LUY Fatura Geçmiş Listeleme",
            "description": "Lisanssız üretim yapan UEVCB'lere ait faturaların versiyon geçmişini listeler.",
            "operation": "get-luy-invoice-history",
            "required": {
                "period": "2023-01-01T00:00:00+03:00",
                "version": "2023-01-01T00:00:00+03:00",
                "region": "TR1",
                "settlementPointId": "UEVCB ID",
                "page": {
                    "number": 1,
                    "size": 10000
                }
            }
        }
    },
    "payment-obligation-details": {
        "export": {
            "path": "https://epys.epias.com.tr/reconciliation-res/v1/payment-obligation/details/export",
            "summary": "",
            "description": "",
            "operation": "export-res-reconciliation-details",
            "required": {
                "effectiveDate": "2023-01-01T00:00:00+03:00",
                "region": "TR1",
                "version": "2023-02-01T00:00:00+03:00",
            },
            "optional": {
                "powerPlantId": None,
                "settlementPointId": None
            }
        },
        "list": {
            "path": "https://epys.epias.com.tr/reconciliation-res/v1/payment-obligation/details/list",
            "summary": "",
            "description": "",
            "operation": "list-res-reconciliation-details",
            "required": {
                "effectiveDate": "2023-01-01T00:00:00+03:00",
                "region": "TR1",
                "versions": [
                    "2023-02-01T00:00:00+03:00"
                ],
                "page": {
                    "number": 1,
                    "size": 10000
                }
            },
            "optional": {
                "powerPlantId": None,
                "settlementPointId": None
            }
        }
    },
    "payment-obligation": {
        "export": {
            "path": "https://epys.epias.com.tr/reconciliation-res/v1/payment-obligation/export",
            "summary": "",
            "description": "",
            "operation": "export-recon-payment-obligations",
            "required": {
                "effectiveDate": "2023-01-01T00:00:00+03:00",
                "region": "TR1",
                "versions": [
                    "2023-02-01T00:00:00+03:00"
                ]
            }
        },
        "list": {
            "path": "https://epys.epias.com.tr/reconciliation-res/v1/payment-obligation/list",
            "summary": "",
            "description": "",
            "operation": "list-recon-payment-obligations",
            "required": {
                "effectiveDate": "2023-01-01T00:00:00+03:00",
                "region": "TR1",
                "versions": [
                    "2023-02-01T00:00:00+03:00"
                ],
                "page": {
                    "number": 1,
                    "size": 10000
                }
            }
        }
    },
    "res-retrospective-detail": {
        "export": {
            "path": "https://epys.epias.com.tr/reconciliation-res/v1/res/retrospective/detail-export",
            "summary": "",
            "description": "",
            "operation": "export-diff-recon-res-cost-settlement-point-details",
            "required": {
                "period": "2023-01-01T00:00:00+03:00",
                "version": "2023-02-01T00:00:00+03:00",
            },
            "optional": {
                "powerPlantId": None,
                "settlementPointId": None
            }

        },
        "list": {
            "path": "https://epys.epias.com.tr/reconciliation-res/v1/res/retrospective/detail-list",
            "summary": "",
            "description": "",
            "operation": "list-diff-recon-res-cost-settlement-point-details",
            "required": {
                "period": "2023-01-01T00:00:00+03:00",
                "version": "2023-02-01T00:00:00+03:00",
            },
            "optional": {
                "powerPlantId": None,
                "settlementPointId": None
            }

        }
    },
    "res-retrospective": {
        "export": {
            "path": "https://epys.epias.com.tr/reconciliation-res/v1/res/retrospective/export",
            "summary": "",
            "description": "",
            "operation": "export-diff-recon-payment-obligation",
            "required": {
                "periodList": ["2023-01-01T00:00:00+03:00"],
                "version": "2023-02-01T00:00:00+03:00",
                "page": {
                    "number": 1,
                    "size": 10000
                }
            },
        },
        "list": {
            "path": "https://epys.epias.com.tr/reconciliation-res/v1/res/retrospective/list",
            "summary": "",
            "description": "",
            "operation": "list-diff-recon-payment-obligation",
            "required": {
                "periodList": ["2023-01-01T00:00:00+03:00"],
                "version": "2023-02-01T00:00:00+03:00",
                "page": {
                    "number": 1,
                    "size": 10000
                }
            },
        }
    },
    "res-unit-price": {
        "export": {
            "path": "https://epys.epias.com.tr/reconciliation-res/v1/res/unit-price/export",
            "summary": "",
            "description": "",
            "operation": "unit-prices",
            "required": {
                "effectiveDateEnd": "2022-05-05T00:00:00+03:00",
                "effectiveDateStart": "2022-05-01T00:00:00+03:00"
            }
        },
        "list": {
            "path": "https://epys.epias.com.tr/reconciliation-res/v1/res/unit-price/list",
            "summary": "",
            "description": "",
            "operation": "get-unit-prices",
            "required": {
                "effectiveDateEnd": "2022-05-05T00:00:00+03:00",
                "effectiveDateStart": "2022-05-01T00:00:00+03:00",
                "page": {
                    "number": 1,
                    "size": 10000
                }
            }
        }
    },
    "rescostsettlement": {
        "export": {
            "path": "https://epys.epias.com.tr/reconciliation-res/v1/rescostsettlement/export",
            "summary": "",
            "description": "",
            "operation": "export-loss-generation",
            "required": {
                "period": "2023-01-01T00:00:00+03:00",
                "version": "2023-01-01T00:00:00+03:00",
                "region": "TR1",
                "category": [],
                "page": {
                    "number": 1,
                    "size": 10000
                }
            }
        },
        "list": {
            "path": "https://epys.epias.com.tr/reconciliation-res/v1/rescostsettlement/list",
            "summary": "",
            "description": "",
            "operation": "list-loss-generation",
            "required": {
                "period": "2023-01-01T00:00:00+03:00",
                "version": "2023-01-01T00:00:00+03:00",
                "region": "TR1",
                "category": [],
                "page": {
                    "number": 1,
                    "size": 10000
                }
            }
        }
    },
}