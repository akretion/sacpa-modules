# Copyright (C) 2025 - TODAY, Akretion
# @author Mourad EL HADJ MIMOUNE <mourad.elhadj.mimoune@akretion.com>

from odoo import models, fields

class HelpdeskInterventionType(models.Model):
    _name = "helpdesk.intervention.type"
    _description = "Type d'intervention"
    _order = "name"

    name = fields.Char(string="Nom", required=True)
    code = fields.Char(string="Code")