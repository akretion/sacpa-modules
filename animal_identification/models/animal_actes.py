from odoo import fields, models


class AnimalActes(models.Model):
    _name = "animal.actes"
    _description = "Actes on animal donne on date"

    name = fields.Char(string="Libellé")
    date = fields.Date(string="Date de l'actes")
    value = fields.Char(string="Value de l'actes")
    animal_id = fields.Many2one(
        string="animal",
        comodel_name="animal.identification",
    )
