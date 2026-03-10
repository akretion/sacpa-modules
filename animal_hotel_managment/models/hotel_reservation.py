from odoo import fields, models


class HotelReservation(models.Model):
    _inherit = "hotel.reservation"

    partner_id = fields.Many2one(required=False)
    adults = fields.Integer(
        required=False,
    )
    animal_id = fields.Many2one("animal.identification", required=True, string="Animal")
    company_id = fields.Many2one("res.company", required=True, string="Société")
    type_reservation = fields.Selection(
        selection=[
            ("Pension", "pension"),
            ("Fourrière", "fourriere"),
            ("Refuge", "refuge"),
        ],
        string="Type de folio",
    )
