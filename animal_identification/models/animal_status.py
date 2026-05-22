# Copyright (C) 2025 - TODAY, Akretion
# @author Mourad EL HADJ MIMOUNE <mourad.elhadj.mimoune@akretion.com>

from odoo import fields, models


class AnimalStatus(models.Model):
    _name = "animal.status"
    _description = "Statut de l'animal"
    _order = "name"

    name = fields.Char(string="Libellé", required=True)
    code = fields.Char()
    description = fields.Char(string="Description du status")
    parent_id = fields.Many2one(comodel_name="animal.status", string="Parent")
    child_ids = fields.One2many(
        comodel_name="animal.status", inverse_name="parent_id", string="Enfant"
    )
    infos = fields.Char(string="Information")
    time_guard = fields.Float(string="Durée de garde")
    vet_visit = fields.Boolean(string="Générer les visites au véterinaire")
    asso = fields.Boolean(string="Transferable association")
    reconciliation = fields.Boolean(string="Rapprochement possible")
    protocol_id = fields.Many2many("animal.protocol", string="List des protocols")
