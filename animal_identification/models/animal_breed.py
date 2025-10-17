# Copyright (C) 2025 - TODAY, Akretion
# @author Mourad EL HADJ MIMOUNE <mourad.elhadj.mimoune@akretion.com>

from odoo import fields, models


class AnimalBreed(models.Model):
    _name = "animal.breed"
    _description = "Race d'animal"
    _order = "name"

    name = fields.Char(string="Libellé", required=True)
    code = fields.Char()
    species_id = fields.Many2one("animal.species", string="Espèce")
    code_group = fields.Char(
        string="Code Groupe",
    )
    code_scc = fields.Char(string="Code SCC")
    classification = fields.Char()
    categorie = fields.Char(string="Catégorie")
