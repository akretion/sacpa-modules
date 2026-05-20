# Copyright (C) 2025 - TODAY, Akretion
# @author Mourad EL HADJ MIMOUNE <mourad.elhadj.mimoune@akretion.com>

from odoo import fields, models


class AnimalHealthStatus(models.Model):
    _name = "animal.health.status"
    _description = "État sanitaire de l'animal a un instant donnée"

    name = fields.Char(string="Libellé", required=True)
    code = fields.Char(string="Code Coaxis")
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
    value = fields.Many2one(
        "animal.health.status.value",
        string="Valeur",
    )


class AnimalHealthStatusValue(models.Model):
    _name = "animal.health.status.value"
    _description = "Valeur du status de santé"

    name = fields.Char(string="Name value")
    animal_healt_status = fields.One2many(
        "animal.health.status", "value", string="Status de l'animal"
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
    value = fields.Many2one(
        "animal.behavior.value",
        string="Valeur",
    )


class AnimalBehaviorValue(models.Model):
    _name = "animal.behavior.value"
    _description = "Valeur du Comportement de l'animal"

    name = fields.Char("Valeur du comportement")
    behavior_id = fields.One2many(
        "animal.behavior", "value", string="Comportmenent de l'animal"
    )


class AnimalWeight(models.Model):
    _name = "animal.weight"
    _description = "Historique poids de l'animal"

    event_date = fields.Date(string="Date")
    value = fields.Float(string="Poids en kg")
    notes = fields.Text(string="Remarques")
