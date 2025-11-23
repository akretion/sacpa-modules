# Copyright (C) 2025 - TODAY, Akretion

{
    "name": "Invoice move webhook",
    "version": "18.0.1.0.0",
    "summary": "Gestion du webhook pour les factures",
    "category": "Uncategorized",
    "website": "https://github.com/akretion/sacpa-modules",
    "license": "AGPL-3",
    "author": " Akretion",
    "depends": [
        "base",
        "account",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/account_move_view.xml",
    ],
    "installable": True,
    "application": True,
}
