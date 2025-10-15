# Copyright (C) 2025 - TODAY, Akretion
# @author Mourad EL HADJ MIMOUNE <mourad.elhadj.mimoune@akretion.com>

from odoo import fields, models


class HelpdeskRequester(models.Model):
    _name = "helpdesk.requester"
    _description = "Donneur d'ordre"
    _order = "name"

    name = fields.Char(string="Nom", required=True)
    code = fields.Char(string="Code")
