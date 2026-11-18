from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    # No groups restriction: ``insee`` is related to this field, so searching
    # on ``insee`` (agreement communes, partner filter) checks access to it.
    zip_city_id = fields.Many2one(comodel_name="res.city.zip")
    # needs to bypass rights to read in extra table
    insee = fields.Char(related="zip_city_id.insee", compute_sudo=True, readonly=True)

    _sql_constraints = [
        (
            "zip_city_id_unique",
            "UNIQUE(zip_city_id)",
            "Field zip_city_id must be unique",
        )
    ]
