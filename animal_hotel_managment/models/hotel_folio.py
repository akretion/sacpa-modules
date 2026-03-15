# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class FolioRoomLine(models.Model):
    _inherit = "folio.room.line"


class HotelFolio(models.Model):
    _inherit = "hotel.folio"

    checkout_date = fields.Datetime(required=False)

    company_id = fields.Many2one(
        "res.company",
        string="Société",
        # required="True",
    )
    animal_ids = fields.Many2many(
        "animal.identification", required=True, string="Animal"
    )
    type_folio = fields.Selection(
        selection=[
            ("Pension", "pension"),
            ("Fourrière", "fourriere"),
            ("Refuge", "refuge"),
        ],
        string="Type de folio",
    )

    def write(self, vals):
        for record in self:
            if record.reservation_id.type_folio:
                type_folio = record.reservation_id.type_folio
            vals["type_folio"] = type_folio
        return super().write(vals)


class HotelFolioLine(models.Model):
    _inherit = "hotel.folio.line"

    animal_id = fields.Many2one("animal.identification", string="animal lier au box")

    def create(self, vals_list):
        return super().create(vals_list)
