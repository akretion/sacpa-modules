# Copyright (C) 2025 - TODAY, Akretion

{
    "name": "Animal Identification",
    "version": "18.0.1.0.0",
    "summary": "Gestion des fiches d'animaux",
    "category": "Uncategorized",
    "website": "https://github.com/akretion/sacpa-modules",
    "license": "AGPL-3",
    "author": " Akretion",
    "depends": ["base"],
    "data": [
        "security/animal_security.xml",
        "security/ir.model.access.csv",
        "views/animal_species_views.xml",
        "views/animal_breed_views.xml",
        "views/animal_status_views.xml",
        "views/animal_health_status_views.xml",
        "views/animal_identification_views.xml",
        "views/animal_menuitem.xml",
    ],
    "installable": True,
    "application": True,
}
