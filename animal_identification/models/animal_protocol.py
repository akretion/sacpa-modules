from odoo import fields, models


class AnimalProtocol(models.Model):
    _name = "animal.protocol"
    _description = "Protocol sanitaire lier aux animaaux"

    name = fields.Char(string="Nom du protocol")
    code = fields.Char(string="Code")

    event_date = fields.Date(string="Date de l'évènement")
