# Copyright (C) 2025 - TODAY, Akretion
# @author Mourad EL HADJ MIMOUNE <mourad.elhadj.mimoune@akretion.com>

from odoo import fields, models


class AnimalHealthStatus(models.Model):
    _name = "animal.health.status"
    _description = "État sanitaire de l'animal"

    name = fields.Char(string="Libellé", required=True)
    code = fields.Char(string="Code")
