# Copyright (C) 2025 - TODAY, Akretion
# @author Mourad EL HADJ MIMOUNE <mourad.elhadj.mimoune@akretion.com>

from odoo import fields, models


class AnimalStatus(models.Model):
    _name = "animal.status"
    _description = "Statut de l'animal"
    _order = "name"

    name = fields.Char(string="Libellé", required=True)
    code = fields.Char()
