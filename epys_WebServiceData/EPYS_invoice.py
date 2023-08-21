
information = {
    'invoice-notice' : ['export', 'list'] ,
    'invoice-notice-invoice-item-with-tax' : ['export', 'list'] ,
    'invoice-notice-retrospective' : ['export', 'list'] ,
}



dataset = {
    "invoice-notice": {
        "export": {
            "path": "https://epys.epias.com.tr/reconciliation-invoice/v1/invoice-notice/export",
            "summary": "Aylık Uzlaştırma Bildirimi Dışarı Aktarma",
            "description": "Aylık uzlaştırma bildiriminin excel, csv ve pdf olarak dışarı aktarılmasını sağlar.",
            "operation": "excel-export-reconciliation-notice",
            "required": {
                "period": "2023-01-01T00:00:00+03:00"
            }
        },
        "list": {
            "path": "https://epys.epias.com.tr/reconciliation-invoice/v1/invoice-notice/list",
            "summary": "Aylık Uzlaştırma Bildirimi ",
            "description": "Aylık uzlaştrıma bildirimi listeleme servisi.",
            "operation": "get-reconciliation-notice",
            "required": {
                "period": "2023-01-01T00:00:00+03:00"
            }
        }
    },
    "invoice-notice-invoice-item-with-tax": {
        "list": {
            "path": "https://epys.epias.com.tr/reconciliation-invoice/v1/invoice-notice/invoice-item-with-tax/list",
            "summary": "Fatura Bildirimi Servisi",
            "description": "Faturaya esas kalemlerinin tutarlarının dönüldüğü servis.",
            "operation": "get-invoice-item-details-with-tax",
            "required": {
                "effectiveDate": "2023-01-01T00:00:00+03:00"
            }
        },
        "export": {
            "path": "https://epys.epias.com.tr/reconciliation-invoice/v1/invoice-notice/invoice-item-with-tax/list/export",
            "summary": "Fatura Bildirimi Dışarı Aktarma Servisi",
            "description": "Faturaya esas kalemlerinin tutarlarının dışarı aktarılmasını sağlar.",
            "operation": "export-invoice-item-details-with-tax",
            "required": {
                "effectiveDate": "2023-01-01T00:00:00+03:00"
            }
        }
    },
    "invoice-notice-retrospective": {
        "export": {
            "path": "https://epys.epias.com.tr/reconciliation-invoice/v1/invoice-notice/retrospective/export",
            "summary": "Dönemlik GDDK Dışarı Aktarma",
            "description": "Dönemlik GDDK tutarlarının excel olarak dışarı aktarılmasını sağlar.",
            "operation": "export-reconciliation-retrospective-notice",
            "required": {
                "effectiveDate": "2023-01-01T00:00:00+03:00"
            }
        },
        "list": {
            "path": "https://epys.epias.com.tr/reconciliation-invoice/v1/invoice-notice/retrospective/list",
            "summary": "Dönemlik GDDK Listeleme",
            "description": "Dönemlik GDDK tutarlarının listelendiği servis.",
            "operation": "get-reconciliation-retrospective-notice",
            "required": {
                "effectiveDate": "2023-01-01T00:00:00+03:00"
            }
        }
    }
}