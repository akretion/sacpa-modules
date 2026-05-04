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
        required=True,
        index=True,
        default=lambda self: self.env.company,
    )
    animal_id = fields.Many2one("animal.identification", required=True, string="Animal")
    job_type = fields.Selection(
        selection=[
            ("pension", "Pension"),
            ("fourrière", "Fourriere"),
            ("refuge", "Refuge"),
        ],
        string="Type",
    )

    def write(self, vals):
        for record in self:
            if record.reservation_id.job_type:
                job_type = record.reservation_id.job_type
            vals["job_type"] = job_type
        return super().write(vals)


class HotelFolioLine(models.Model):
    _inherit = "hotel.folio.line"

    animal_id = fields.Many2one("animal.identification", string="animal lier au box")

    def create(self, vals_list):
        return super().create(vals_list)
