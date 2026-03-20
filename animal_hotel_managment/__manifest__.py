# Copyright (C) 2025 - TODAY, Akretion

{
    "name": "Animal hotel managment",
    "version": "18.0.1.0.0",
    "summary": "Gestion des box d'animaux",
    "category": "Uncategorized",
    "website": "https://github.com/akretion/sacpa-modules",
    "license": "AGPL-3",
    "author": " Akretion",
    "depends": [
        "hotel",
        "hotel_reservation",
    ],
    "data": [
        "security/groups_security_animal_hotel.xml",
        # "security/ir.model.access.csv",
        "views/view_hotel_folio.xml",
        "views/views_hotel_reservation.xml",
        "views/views_menu_item.xml",
    ],
    "installable": True,
    "application": True,
    "post_init_hook": "post_init_hook",
}
