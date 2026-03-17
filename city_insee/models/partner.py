from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    zip_city_id = fields.Many2one(
        comodel_name="res.city.zip", groups="base.group_no_one"
    )
    insee = fields.Char(related="zip_city_id.insee", readonly=True)
