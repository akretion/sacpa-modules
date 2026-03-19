# Copyright (C) 2025 - TODAY, Akretion
# @author Mourad EL HADJ MIMOUNE <mourad.elhadj.mimoune@akretion.com>

from odoo import fields, models


class AnimalHealthStatus(models.Model):
    _name = "animal.health.status"
    _description = "État sanitaire de l'animal"

    name = fields.Char(string="Libellé", required=True)
    code = fields.Char()
    date_event = fields.Date(string="Date")
    event = fields.Selection(
        [
            ("fsm_order", "Intervention"),
            ("enter", "Entrer en centre"),
            ("medical", "Visite medical"),
            ("exit", "Sortie"),
        ],
        string="Moment",
    )
    value = fields.Selection([()], string="Valeur")


class AnimalComportement(models.Model):
    _name = "animal.comportement"
    _description = "Comportement de l'animal"

    date = fields.Date(string="date")
    event = fields.Selection(
        [
            ("fsm_order", "Intervention"),
            ("enter", "Entrée en centre"),
            ("medical", "Visite médicale"),
            ("exit", "Sortie"),
        ]
    )
    value = fields.Selection(
        [],
        string="Valeur",
    )


class AnimalWeight(models.Model):
    _name = "animal.weight"
    _description = "Comportement de l'animal"

    date_event = fields.Date(string="Date")
    value = fields.Float(string="Poids en kg")
    notes = fields.Text(string="Remarques")
