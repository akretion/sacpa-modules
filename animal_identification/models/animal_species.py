# Copyright (C) 2025 - TODAY, Akretion
# @author Mourad EL HADJ MIMOUNE <mourad.elhadj.mimoune@akretion.com>

from odoo import fields, models


class AnimalSpecies(models.Model):
    _name = "animal.species"
    _description = "Ensemeble des espèces d'animal"
    _order = "name"

    name = fields.Char(string="Libellé", required=True)
    code = fields.Char(string="Code Coaxis")
