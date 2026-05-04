from odoo import fields, models


class HotelRoom(models.Model):
    _inherit = "hotel.room"
    _description = "Hotel Room"

    company_id = fields.Many2one(
        "res.company",
        string="Société détentris",
        required=True,
        index=True,
        default=lambda self: self.env.company,
    )
