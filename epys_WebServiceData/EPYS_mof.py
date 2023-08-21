
information = {
    'reconciliation-mof-organization' : ['export', 'list'] ,
    'reconciliation-mof-organization-retrospective' : ['export', 'list'] 
    }

dataset =     {
    "reconciliation-mof-organization": {
        "export": {
            "path": "https://epys.epias.com.tr/reconciliation-mof/v1/reconciliation/mof/organization/export",
            "summary": "Dönemlik organizasyon piu detayı",
            "description": "Dönemlik organizasyon piu detayını döner.",
            "operation": "export-organization-mof-details",
            "required": {
                "period": "2023-01-01T00:00:00+03:00",
                "version": "2023-01-01T00:00:00+03:00"
            },
            "note": "version >= period"
        },
        "list": {
            "path": "https://epys.epias.com.tr/reconciliation-mof/v1/reconciliation/mof/organization/list",
            "summary": "Dönemlik organizasyon piu detayı",
            "description": "Dönemlik organizasyon piu detayını döner.",
            "operation": "get-organization-mof-details",
            "required": {
                "period": "2023-01-01T00:00:00+03:00",
                "version": "2023-01-01T00:00:00+03:00"
            },
            "note": "version >= period"
        }
    },
    "reconciliation-mof-organization-retrospective": { 
        "export": {
            "path": "https://epys.epias.com.tr/reconciliation-mof/v1/reconciliation/mof/organization/retrospective/export",
            "summary": "GDDK Tutarı içerisindeki PİÜ detayları",
            "description": "GDDK Tutarı içerisindeki seçili döneme ait PİÜ detaylarının görüntülenmesi işlemidir.",
            "operation": "export-retrospective-organization-mof-details",
            "required": {
                "period": "2023-01-01T00:00:00+03:00",
                "version": "2023-02-01T00:00:00+03:00"
            },
            "note": "version > period"
        },
        "list": {
            "path": "https://epys.epias.com.tr/reconciliation-mof/v1/reconciliation/mof/organization/retrospective/list",
            "summary": "GDDK Tutarı içerisindeki PİÜ detayları",
            "description": "GDDK Tutarı içerisindeki seçili döneme ait PİÜ detaylarının görüntülenmesi işlemidir.",
            "operation": "list-retrospective-organization-mof-details",
            "required": {
                "period": "2023-01-01T00:00:00+03:00",
                "version": "2023-02-01T00:00:00+03:00"
            },
            "note": "version > period"
        }
    }
}


