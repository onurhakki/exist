
information = {
    'aic' : ['export', 'list'] ,
    'fddp' : ['export', 'list'] ,
    'instruction' : ['export', 'list'] ,
    'reconciliation-detail' : ['export', 'list'] ,
    'reconciliation-instruction-undeliverable' : ['export', 'list'] ,
    'reconciliation-organization' : ['export', 'list'] ,
    'reconciliation-retrospective-bpm' : ['export', 'list'] ,
    'reconciliation-retrospective-sbfgp' : ['export', 'list'] ,
    'reconciliation-sbfgp' : ['export', 'list'] ,
    'smp' : ['list'] ,
}

dataset =    {
    "aic": {
        "export": {
            "path": "https://epys.epias.com.tr/reconciliation-bpm/v1/aic/export",
            "summary": "EAK Listesini excel ile export işlemi.",
            "description": "EAK Listesini excel ile export işlemi.",
            "operation": "export-available-installed-capacity-details",
            "required": {
                "effectiveDateStart": "2023-01-01T00:00:00+03:00",
                "effectiveDateEnd": "2023-01-31T23:00:00+03:00"
            },
            "optional": {
                "powerPlantId": None,
                "settlementPointId": None
            }
        },
        "list": {
            "path": "https://epys.epias.com.tr/reconciliation-bpm/v1/aic/list",
            "summary": "EAK Listesi",
            "description": "EAK Listesini Döner.",
            "operation": "get-available-installed-capacity-details",
            "required": {
                "effectiveDateStart": "2023-01-01T00:00:00+03:00",
                "effectiveDateEnd": "2023-01-31T23:00:00+03:00",
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
    "fddp": {
        "export": {
            "path": "https://epys.epias.com.tr/reconciliation-bpm/v1/fddp/export",
            "summary": "KGÜP Detaylarını Görüntüleme",
            "description": "Yetkili kullanıcıların KGÜP Detaylarının Listelendiği Ekranı Görüntüleme işlemidir.",
            "operation": "export-final-daily-production-program-details",
            "required": {
                "effectiveDateStart": "2023-01-01T00:00:00+03:00",
                "effectiveDateEnd": "2023-01-31T23:00:00+03:00"
            },
            "optional": {
                "powerPlantId": None,
                "settlementPointId": None
            }
        },
        "list": {
            "path": "https://epys.epias.com.tr/reconciliation-bpm/v1/fddp/list",
            "summary": "KGÜP Detaylarını Görüntüleme",
            "description": "Yetkili kullanıcıların KGÜP Detaylarının Listelendiği Ekranı Görüntüleme işlemidir.",
            "operation": "get-final-daily-production-program-details",
            "required": {
                "effectiveDateStart": "2023-01-01T00:00:00+03:00",
                "effectiveDateEnd": "2023-01-31T23:00:00+03:00",
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
    "instruction": {
        "list": {
            "path": "https://epys.epias.com.tr/reconciliation-bpm/v1/instruction/list",
            "summary": "DGP Talimatları",
            "description": "DGP Talimatlarının Listesini Döner.",
            "operation": "get-bpm-instruction-list",
            "required": {
                "effectiveDateStart": "2023-01-01T00:00:00+03:00",
                "effectiveDateEnd": "2023-01-31T23:00:00+03:00",
                "region": "TR1",
                "page": {
                    "number": 1,
                    "size": 10000
                }

            },
            "optional": {
                "powerPlantId": None,
                "settlementPointId": None
            }
        },
        "export": {
            "path": "https://epys.epias.com.tr/reconciliation-bpm/v1/instruction/list/export",
            "summary": "DGP Talimatlarının Listesini EXCEL export ",
            "description": "DGP Talimatlarının Listesini EXCEL export işlemi.",
            "operation": "export-bpm-instruction-list",
            "required": {
                "effectiveDateStart": "2023-01-01T00:00:00+03:00",
                "effectiveDateEnd": "2023-01-31T23:00:00+03:00",
                "region": "TR1"
            },
            "optional": {
                "powerPlantId": None,
                "settlementPointId": None
            }
        }

    },




    "reconciliation-detail": {
        "export": {
            "path": "https://epys.epias.com.tr/reconciliation-bpm/v1/reconciliation/detail/export",
            "summary": "Talimat Detay Listelerinin Görüntülenmesi.",
            "description": "Yetkili kullanıcıların Talimat Detaylarının Listelendiği Ekranı Görüntüleme işlemidir",
            "operation": "export-bpm-instruction-detail-response-dto",
                        "required": {
                "period": "2023-01-01T00:00:00+03:00",
                "effectiveDateStart": "2023-01-01T00:00:00+03:00",
                "effectiveDateEnd": "2023-01-01T23:00:00+03:00",
                "versions": [
                    "2023-01-01T00:00:00+03:00"
                ],
                "region": "TR1",
            },
            "optional": {
                "powerPlantId": None,
                "settlementPointId": None
            }

        },
        "list": {
            "path": "https://epys.epias.com.tr/reconciliation-bpm/v1/reconciliation/detail/list",
            "summary": "Dengeleme Güç Piyasası Uzlaştırmasını Görüntüle.",
            "description": "Yetkili kullanıcıların Dengeleme Güç Piyasası Uzlaştırma Verilerinin Listelendiği EkranıGörüntüleme işlemidir.",
            "operation": "get-bpm-instruction-reconciliation-details",
                        "required": {
                "period": "2023-01-01T00:00:00+03:00",
                "effectiveDateStart": "2023-01-01T00:00:00+03:00",
                "effectiveDateEnd": "2023-01-01T23:00:00+03:00",
                "versions": [
                    "2023-01-01T00:00:00+03:00"
                ],
                "region": "TR1",
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





    "reconciliation-instruction-undeliverable": {
        "list": {
            "path": "https://epys.epias.com.tr/reconciliation-bpm/v1/reconciliation/instruction/undeliverable",
            "summary": "DGP Yerine Getirilmeyen Talimat Maliyet Listeleme.",
            "description": "DGP Yerine Getirilmeyen Talimat Maliyet Listeleme.",
            "operation": "get-instruction-undeliverable-details",
            "required": {
                "period": "2023-01-01T00:00:00+03:00",
                "effectiveDateStart": "2023-01-01T00:00:00+03:00",
                "effectiveDateEnd": "2023-01-01T23:00:00+03:00",
                "versions": [
                    "2023-01-01T00:00:00+03:00"
                ],
                "region": "TR1",
                "page": {
                    "number": 1,
                    "size": 10000
                }

            },
            "optional": {
                "powerPlantId": None,
                "settlementPointId": None
            }
        },
        "export": {
            "path": "https://epys.epias.com.tr/reconciliation-bpm/v1/reconciliation/instruction/undeliverable/export",
            "summary": "Talimat Teslim Etmeme Detayını excel export işlemi.",
            "description": "Talimat Teslim Etmeme Detayını excel export işlemi.",
            "operation": "export-instruction-undeliverable-details",
            "required": {
                "period": "2023-01-01T00:00:00+03:00",
                "effectiveDateStart": "2023-01-01T00:00:00+03:00",
                "effectiveDateEnd": "2023-01-01T23:00:00+03:00",
                "versions": [
                    "2023-01-01T00:00:00+03:00"
                ],
                "region": "TR1"
            },
            "optional": {
                "powerPlantId": None,
                "settlementPointId": None
            }
        }
    },

    "reconciliation-organization": {
        "export": {
            "path": "https://epys.epias.com.tr/reconciliation-bpm/v1/reconciliation/organization/export",
            "summary": "Dengeleme Güç Piyasası Uzlaştırmasını Görüntüle.",
            "description": "Yetkili kullanıcıların Dengeleme Güç Piyasası Uzlaştırma Verilerinin Listelendiği Ekranı Görüntüleme işlemidir.",
            "operation": "export-bpm-instruction-reconciliation-details",
            "required": {
                "period": "2023-01-01T00:00:00+03:00",
                "effectiveDateStart": "2023-01-01T00:00:00+03:00",
                "effectiveDateEnd": "2023-01-01T23:00:00+03:00",
                "versions": [
                    "2023-01-01T00:00:00+03:00"
                ],
                "region": "TR1",
                
            },
            "optional": {
                "powerPlantId": None,
                "settlementPointId": None
            }
        },
        "list": {
            "path": "https://epys.epias.com.tr/reconciliation-bpm/v1/reconciliation/organization/list",
            "summary": "Dengeleme Güç Piyasası Uzlaştırmasını Görüntüle",
            "description": "Yetkili kullanıcıların Dengeleme Güç Piyasası Uzlaştırma Verilerinin Listelendiği Ekranı Görüntüleme işlemidir.",
            "operation": "get-bpm-instruction-reconciliation",
            "required": {
                "period": "2023-01-01T00:00:00+03:00",
                "effectiveDateStart": "2023-01-01T00:00:00+03:00",
                "effectiveDateEnd": "2023-01-01T23:00:00+03:00",
                "versions": [
                    "2023-01-01T00:00:00+03:00"
                ],
                "region": "TR1",
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
    "reconciliation-retrospective-bpm": {
        "list": {
            "path": "https://epys.epias.com.tr/reconciliation-bpm/v1/reconciliation/retrospective/bpm/list",
            "summary": "UEVCB Farkları",
            "description": "Organizasyonlara ait uevcb'lerin fatura dönemine ait farklarını döner.",
            "operation": "list-difference-settlement-entity-instruction-response-dto",
            "required": {
                "period": "2023-01-01T00:00:00+03:00",
                "effectiveDateStart": "2023-01-01T00:00:00+03:00",
                "effectiveDateEnd": "2023-01-01T23:00:00+03:00",
                "version": "2023-01-01T00:00:00+03:00",
                "region": "TR1",
                "page": {
                    "number": 1,
                    "size": 10000
                }

            },
            "optional": {
                "powerPlantId": None,
                "settlementPointId": None
            }
        },
        "export": {
            "path": "https://epys.epias.com.tr/reconciliation-bpm/v1/reconciliation/retrospective/bpm/list/export",
            "summary": "DGP GDDK Export.",
            "description": "DGP GDDK Export.",
            "operation": "export-bpm-retrospective-list",
            "required": {
                "period": "2023-01-01T00:00:00+03:00",
                "effectiveDateStart": "2023-01-01T00:00:00+03:00",
                "effectiveDateEnd": "2023-01-01T23:00:00+03:00",
                "version": "2023-01-01T00:00:00+03:00",
                "region": "TR1"
            },
            "optional": {
                "powerPlantId": None,
                "settlementPointId": None
            }
        }
    },

    "reconciliation-retrospective-sbfgp": {
        "list": {
            "path": "https://epys.epias.com.tr/reconciliation-bpm/v1/reconciliation/retrospective/sbfgp",
            "summary": "GDDK Detay Listeleme",
            "description": "Organizasyonlara ait UEVCB'lere ait KUDUP uzlaştırma sonucu oluşan GDDK detaylarini listeler",
            "operation": "list-diff-recon-organization-settlement-based-final-generation-plan-response-dto",
            "required": {
                "period": "2023-01-01T00:00:00+03:00",
                "effectiveDateStart": "2023-01-01T00:00:00+03:00",
                "effectiveDateEnd": "2023-01-01T23:00:00+03:00",
                "version": "2023-01-01T00:00:00+03:00",
                "region": "TR1",
                "page": {
                    "number": 1,
                    "size": 10000
                }

            },
            "optional": {
                "powerPlantId": None,
                "settlementPointId": None
            }
        },
        "export": {
            "path": "https://epys.epias.com.tr/reconciliation-bpm/v1/reconciliation/retrospective/sbfgp/export",
            "summary": "GDDK Detay Export",
            "description": "Organizasyonlara ait UEVCB'lere ait KUDUP uzlaştırma sonucu oluşan GDDK detaylarini export eder",
            "operation": "bpm-reconciliation-retrospective",
            "required": {
                "period": "2023-01-01T00:00:00+03:00",
                "effectiveDateStart": "2023-01-01T00:00:00+03:00",
                "effectiveDateEnd": "2023-01-01T23:00:00+03:00",
                "version": "2023-01-01T00:00:00+03:00",
                "region": "TR1"
            },
            "optional": {
                "powerPlantId": None,
                "settlementPointId": None
            }
        }
    },
    "reconciliation-sbfgp": {
        "list": {
            "path": "https://epys.epias.com.tr/reconciliation-bpm/v1/reconciliation/sbfgp",
            "summary": "KÜPST Detay Listelerinin Görüntülenmesi.",
            "description": "Yetkili kullanıcıların KÜPST Detaylarının Listelendiği Ekranı Görüntüleme işlemidir.",
            "operation": "get-sbfgp-reconciliation-detail-response-dtos-list",
            "required": {
                "period": "2023-01-01T00:00:00+03:00",
                "effectiveDateStart": "2023-01-01T00:00:00+03:00",
                "effectiveDateEnd": "2023-01-01T23:00:00+03:00",
                "versions": [
                    "2023-01-01T00:00:00+03:00"
                ],
                "region": "TR1",
                "page": {
                    "number": 1,
                    "size": 10000
                }

            },
            "optional": {
                "powerPlantId": None,
                "settlementPointId": None
            }
        },
        "export": {
            "path": "https://epys.epias.com.tr/reconciliation-bpm/v1/reconciliation/sbfgp/export",
            "summary": "KÜPST Detay Listelerinin Görüntülenmesi.",
            "description": "Yetkili kullanıcıların KÜPST Detaylarının Listelendiği Ekranı Görüntüleme işlemidir.",
            "operation": "export-sbfgp-reconciliation-detail-response-dtos-list",
            "required": {
                "period": "2023-01-01T00:00:00+03:00",
                "effectiveDateStart": "2023-01-01T00:00:00+03:00",
                "effectiveDateEnd": "2023-01-01T23:00:00+03:00",
                "versions": [
                    "2023-01-01T00:00:00+03:00"
                ],
                "region": "TR1"
            },
            "optional": {
                "powerPlantId": None,
                "settlementPointId": None
            }
        }
    },
    "smp": {
        "list": {
            "path": "https://epys.epias.com.tr/reconciliation-bpm/v1/smp/list",
            "summary": "SMF değer Listeleme",
            "description": "SMF değerlerini listeler.",
            "operation": "list-system-marginal-price-list",
            "required": {
                "effectiveDateStart": "2023-01-01T00:00:00+03:00",
                "effectiveDateEnd": "2023-01-31T23:00:00+03:00",
                "page": {
                    "number": 1,
                    "size": 10000
                }

            }
        }
    }
}