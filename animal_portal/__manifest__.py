# Copyright (C) 2026 - TODAY, Akretion

{
    "name": "Animal Portal",
    "summary": "Espace clients : demandes d'intervention et interventions",
    "version": "18.0.1.0.0",
    "development_status": "Alpha",
    "category": "Services/Field Service",
    "website": "https://github.com/akretion/sacpa-modules",
    "author": "Akretion",
    "license": "AGPL-3",
    "depends": [
        "animal_helpdesk",
        "animal_fieldservice",
        "fieldservice_portal",
        "helpdesk_mgmt",
    ],
    "data": [
        "views/helpdesk_ticket_templates.xml",
        "views/fsm_order_templates.xml",
    ],
    "installable": True,
}
