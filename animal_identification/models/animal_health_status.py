# Copyright (C) 2025 - TODAY, Akretion
# @author Mourad EL HADJ MIMOUNE <mourad.elhadj.mimoune@akretion.com>

from odoo import fields, models


class AnimalHealthStatus(models.Model):
    _name = "animal.health.status"
    _description = "État sanitaire de l'animal"

    name = fields.Char(string="Libellé", required=True)
    code = fields.Char()
    event_date = fields.Date(string="Date")
    event = fields.Selection(
        [
            ("fsm_order", "Intervention"),
            ("enter", "Entrer en centre"),
            ("medical", "Visite medical"),
            ("exit", "Sortie"),
        ],
        string="Moment",
    )
    value = fields.Selection(
        [
            ("valeur_1", "Valeur_1"),
        ],
        string="Valeur",
    )


class AnimalBehavior(models.Model):
    _name = "animal.behavior"
    _description = "Comportement de l'animal"

    event_date = fields.Date(string="date")
    event = fields.Selection(
        [
            ("fsm_order", "Intervention"),
            ("enter", "Entrée en centre"),
            ("medical", "Visite médicale"),
            ("exit", "Sortie"),
        ]
    )
    value = fields.Selection(
        [
            ("valeur_1", "Valeur_1"),
        ],
        string="Valeur",
    )


class AnimalWeight(models.Model):
    _name = "animal.weight"
    _description = "Historique poids de l'animal"

    event_date = fields.Date(string="Date")
    value = fields.Float(string="Poids en kg")
    notes = fields.Text(string="Remarques")
