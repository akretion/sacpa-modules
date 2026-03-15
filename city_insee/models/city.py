import unidecode

from odoo import api, fields, models


class ResCityZip(models.Model):
    _inherit = "res.city.zip"

    insee = fields.Char(string="Code INSEE", index=True)
    city = fields.Char(related="city_id.city_ref", store=True)
    zipcity = fields.Char(
        store=True,
        compute="_compute_zipcity",
        help="Concatenation of zip and city for easier search",
    )

    @api.depends("name", "city_id.city_ref")
    def _compute_zipcity(self):
        for rec in self:
            rec.zipcity = f"{rec.name}{rec.city_id.city_ref}"


class ResCity(models.Model):
    _inherit = "res.city"

    city_ref = fields.Char(
        compute="_compute_city_upper",
        store=True,
        help="Allow to search city without accent and in upper case "
        "for reliable matching.",
    )

    @api.depends("name")
    def _compute_city_upper(self):
        for rec in self:
            rec.city_ref = unidecode.unidecode(rec.name).upper()
