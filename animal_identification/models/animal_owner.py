from odoo import api, fields, models


class AnimalOwner(models.Model):
    _name = "animal.owner"
    _description = "Owner of animal"

    partner_id = fields.Many2one("res.partner", string="Propriétaire du l'animal")
    name = fields.Char(
        string="Nom du Propriétaire"
    )  # Auto remplis si partner_id renseigner
    start_date = fields.Date(string="Propriétaire depuis")
    end_date = fields.Date(string="N'est plus propriétaire depuis")
    city = fields.Char(string="ville")
    legal = fields.Boolean(string="Propriétaire légal")

    @api.onchange("partner_id")
    def _set_name_city(self):
        for record in self:
            if record.partner_id:
                record.name = record.partner_id.name
                record.city = record.partner_id.city
            else:
                record.name = ""
                record.city = ""
