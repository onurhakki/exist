
information = {
    'imbalance-balance-group-organization-detail' : ['export', 'list'] ,
    'imbalance-balance-group-organization-detail-monthly' : ['export', 'list'] ,
    'imbalance' : ['export', 'list'] ,
    'retrospective-imbalance-list-balance-group-detail' : ['export', 'list']}

dataset ={
    "imbalance-balance-group-organization-detail": {
        "export": {
            "path": "https://epys.epias.com.tr/reconciliation-imbalance/v1/imbalance/balance-group-organization/detail/export",
            "summary": "DSG Enerji Dengesizlik Detay Dışarı Aktarma Servisi",
            "description": "Dengeden sorumlu grup üyelerinin enerji dengesizlik bilgilerinin dışarı aktarılmasını sağlar.",
            "operation": "export-balance-group-organization-detail",
            "required": {
                "period": "2023-01-01T00:00:00+03:00",
                "effectiveDateStart": "2023-01-01T00:00:00+03:00",
                "effectiveDateEnd": "2023-01-31T23:00:00+03:00",
                "version": "2023-01-01T00:00:00+03:00",
                "region": "TR1"
            }
        },
        "list": {
            "path": "https://epys.epias.com.tr/reconciliation-imbalance/v1/imbalance/balance-group-organization/detail/list",
            "summary": "DSG Enerji Dengesizlik Detay Servisi",
            "description": "Dengeden sorumlu grup üyelerinin enerji dengesizlik bilgilerini döner.",
            "operation": "get-balance-group-imbalance-details",
            "required": {
                "period": "2023-01-01T00:00:00+03:00",
                "effectiveDateStart": "2023-01-01T00:00:00+03:00",
                "effectiveDateEnd": "2023-01-31T23:00:00+03:00",
                "version": "2023-01-01T00:00:00+03:00",
                "region": "TR1",
                "page": {
                    "number": 1,
                    "size": 10000
                }
            }
        }
    },
    "imbalance-balance-group-organization-detail-monthly": {
        "export": {
            "path": "https://epys.epias.com.tr/reconciliation-imbalance/v1/imbalance/balance-group-organization/detail/monthly/export",
            "summary": "DSG Aylık Organizasyon Detay Dışarı Aktarma Servisi",
            "description": "DSG üyelerinin aylık dengesizlik bilgilerinin dışarı aktarılmasını sağlar.",
            "operation": "export-balance-group-organization-monthly-and-hourly-details",
            "required": {
                "period": "2023-01-01T00:00:00+03:00",
                "effectiveDateStart": "2023-01-01T00:00:00+03:00",
                "effectiveDateEnd": "2023-01-31T23:00:00+03:00",
                "version": "2023-01-01T00:00:00+03:00",
                "region": "TR1"
            }
        },
        "list": {
            "path": "https://epys.epias.com.tr/reconciliation-imbalance/v1/imbalance/balance-group-organization/detail/monthly/list",
            "summary": "DSG Aylık Organizasyon Detay Servisi",
            "description": "DSG üyelerinin aylık dengesizlik bilgilerini döner.",
            "operation": "get-balance-group-imbalance-monthly-details",
            "required": {
                "period": "2023-01-01T00:00:00+03:00",
                "effectiveDateStart": "2023-01-01T00:00:00+03:00",
                "effectiveDateEnd": "2023-01-31T23:00:00+03:00",
                "version": "2023-01-01T00:00:00+03:00",
                "region": "TR1",
                "page": {
                    "number": 1,
                    "size": 10000
                }
            }
        }
    },
    "imbalance": {
        "export": {
            "path": "https://epys.epias.com.tr/reconciliation-imbalance/v1/imbalance/export",
            "summary": "Organizasyon Enerji Dengesizlik Dışarı Aktarma Servisi",
            "description": "Organizasyonların saatlik detayda dengesizlik detaylarını dışarı aktarılmasını sağlar.",
            "operation": "export-organization-imbalance-details",
            "required": {
                "period": "2023-01-01T00:00:00+03:00",
                "effectiveDateStart": "2023-01-01T00:00:00+03:00",
                "effectiveDateEnd": "2023-01-31T23:00:00+03:00",
                "version": "2023-01-01T00:00:00+03:00",
                "region": "TR1"
            }
        },
        "list": {
            "path": "https://epys.epias.com.tr/reconciliation-imbalance/v1/imbalance/list",
            "summary": "Organizasyon Enerji Dengesizlik Servisi",
            "description": "Organizasyonların saatlik detayda dengesizlik detaylarını döner.",
            "operation": "get-organization-imbalance-details",
            "required": {
                "period": "2023-01-01T00:00:00+03:00",
                "effectiveDateStart": "2023-01-01T00:00:00+03:00",
                "effectiveDateEnd": "2023-01-31T23:00:00+03:00",
                "version": "2023-01-01T00:00:00+03:00",
                "region": "TR1",
                "page": {
                    "number": 1,
                    "size": 10000
                }
            }
        }
    },
    "retrospective-imbalance-list-balance-group-detail": {
        "list": {
            "path": "https://epys.epias.com.tr/reconciliation-imbalance/v1/retrospective-imbalance/list-balance-group-detail",
            "summary": "DSG GDDK Detay Servisi",
            "description": "DSG üyelerinin aylık GDDK değişimlerine ait dengesizlik bilgilerini döner.",
            "operation": "get-balance-group-imbalance-difference-details",
            "required": {
                "period": "2023-01-01T00:00:00+03:00",
                "effectiveDateStart": "2023-01-01T00:00:00+03:00",
                "effectiveDateEnd": "2023-01-31T23:00:00+03:00",
                "version": "2023-01-01T00:00:00+03:00",
                "region": "TR1",
                "page": {
                    "number": 1,
                    "size": 10000
                }
            }
        },
        "export": {
            "path": "https://epys.epias.com.tr/reconciliation-imbalance/v1/retrospective-imbalance/list-balance-group-detail/export",
            "summary": "DSG GDDK Detay Dışarı Aktarma Servisi",
            "description": "DSG üyelerinin aylık GDDK değişimlerine ait dengesizlik bilgilerinin dışarı aktarılmasın sağlar.",
            "operation": "export-balance-group-detail",
            "required": {
                "period": "2023-01-01T00:00:00+03:00",
                "effectiveDateStart": "2023-01-01T00:00:00+03:00",
                "effectiveDateEnd": "2023-01-31T23:00:00+03:00",
                "version": "2023-01-01T00:00:00+03:00",
                "region": "TR1"
            }
        }
    }
}