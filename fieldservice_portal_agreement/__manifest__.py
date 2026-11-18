# Copyright (C) 2026 - TODAY, Akretion

{
    "name": "Field Service Portal Agreement",
    "summary": "Portal visibility of FSM orders and tickets based on the agreement partner",
    "version": "18.0.1.2.0",
    "development_status": "Alpha",
    "category": "Services/Field Service",
    "website": "https://github.com/akretion/sacpa-modules",
    "author": "Akretion",
    "license": "AGPL-3",
    "depends": [
        "fieldservice_portal",
        "fieldservice_agreement",
        "helpdesk_mgmt_fieldservice",
        "agreement_helpdesk_mgmt",
        "accord",
    ],
    "data": [
        "security/portal_security.xml",
    ],
    "installable": True,
}
