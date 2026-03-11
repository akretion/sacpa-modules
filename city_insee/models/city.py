import unidecode

from odoo import api, fields, models


class ResCityZip(models.Model):
    _inherit = "res.city.zip"

    insee = fields.Char(string="Code INSEE", index=True)
    city = fields.Char(related="city_id.city_ref", store=True)


class ResCity(models.Model):
    _inherit = "res.city"

    city_ref = fields.Char(compute="_compute_city_upper", store=True)

    @api.depends("name")
    def _compute_city_upper(self):
        for rec in self:
            rec.city_ref = unidecode.unidecode(rec.name).upper()
