from typing import Required
from odoo import fields, models


class HotelReservation(models.Model):
    _inherit = "hotel.reservation"

    partner_id = fields.Many2one(required=False)
    adults = fields.Integer(
        required=False,
    )
    animal_id = fields.Many2one("animal.identification", string="Animal", required=True)
    # company_id = fields.Many2one("res.company", required=True, string="Société")
    job_type = fields.Selection(
        selection=[
            ("pension", "Pension"),
            ("fourriere", "Fourriere"),
            ("refuge", "Refuge"),
        ],
        string="Type de folio",
    )
