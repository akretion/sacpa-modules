from odoo import fields, models


class AnimalProtocol(models.Model):
    _name = "animal.protocol"
    _description = "Protocol sanitaire lier aux animaaux"

    name = fields.Char(string="Nom du protocol")
    code = fields.Char(string="Code Coaxis")


class AnimalProtocolEvent(models.Model):
    _name = "animal.protocol.event"
    _description = "Event of a protocol"

    protocol_id = fields.Many2one(comodel_name="animal.protocol", string="Protocol")
    code = fields.Char(string="Code", related="protocol_id.code")
    name = fields.Char(string="Name", related="protocol_id.name")
    event_date = fields.Date(string="Date de l'évènement")
