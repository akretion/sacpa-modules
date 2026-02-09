# Copyright (C) 2025 - TODAY, Akretion

{
    "name": "Animal helpdesk",
    "version": "18.0.1.0.0",
    "summary": "Helpdesk Extension - Appels et Animaux",
    "license": "AGPL-3",
    "category": "Uncategorized",
    "website": "https://github.com/akretion/sacpa-modules",
    "author": " Akretion",
    "depends": [
        "helpdesk_mgmt",
        "helpdesk_mgmt_fieldservice",
        "animal_identification",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/helpdesk_intervention_type_views.xml",
        "views/helpdesk_requester_views.xml",
        "views/helpdesk_ticket_views.xml",
    ],
    "installable": True,
}
