from typing import Required
from odoo import fields, models, api

from odoo.exceptions import ValidationError


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
        default=lambda self: self.env.context.get("job_type", False),
    )

    @api.constrains("reservation_line", "animal_id")
    def _check_reservation_rooms(self):
        """
        This method is used to validate the reservation_line.
        -----------------------------------------------------
        @param self: object pointer
        @return: raise a warning depending on the validation
        """
        ctx = dict(self._context) or {}
        for reservation in self:
            room_cap = []
            for rec in reservation.reservation_line:
                cap = 0
                if len(rec.reserve) == 0:
                    raise ValidationError(_("Please Select Rooms For Reservation."))
                cap = sum(room.capacity for room in rec.reserve)
                room_cap.append(cap)
            if not ctx.get("duplicate"):
                if (reservation.adults + reservation.children) > sum(room_cap):
                    raise ValidationError(
                        _(
                            "Room Capacity Exceeded \n"
                            " Please Select Rooms According to"
                            " Members Accommodation."
                        )
                    )
            if not reservation.animal_id:
                raise ValidationError(_("Animal must be more than 0"))

    def create_folio(self):
        """
        This method is for create new hotel folio.
        -----------------------------------------
        @param self: The object pointer
        @return: new record set for hotel folio.
        """
        hotel_folio_obj = self.env["hotel.folio"]
        for reservation in self:
            folio_lines = []
            checkin_date = reservation["checkin"]
            checkout_date = reservation["checkout"]
            duration_vals = self._onchange_check_dates(
                checkin_date=checkin_date,
                checkout_date=checkout_date,
                duration=False,
            )
            duration = duration_vals.get("duration") or 0.0
            folio_vals = {
                "date_order": reservation.date_order,
                "company_id": reservation.company_id.id,
                "partner_id": reservation.partner_id.id,
                "animal_id": reservation.animal_id.id,
                "pricelist_id": reservation.pricelist_id.id,
                "partner_invoice_id": reservation.partner_invoice_id.id
                or reservation.partner_id.id,
                "partner_shipping_id": reservation.partner_shipping_id.id
                or reservation.partner_id.id,
                "checkin_date": reservation.checkin,
                "checkout_date": reservation.checkout,
                "duration": duration,
                "reservation_id": reservation.id,
            }
            for line in reservation.reservation_line:
                for r in line.reserve:
                    folio_lines.append(
                        (
                            0,
                            0,
                            {
                                "checkin_date": checkin_date,
                                "checkout_date": checkout_date,
                                "product_id": r.product_id and r.product_id.id,
                                "name": reservation["reservation_no"],
                                "price_unit": r.list_price,
                                "product_uom_qty": duration,
                                "tax_id": [(6, 0, r.product_id.taxes_id.ids)],
                                "is_reserved": True,
                            },
                        )
                    )
                    r.write({"status": "occupied", "isroom": False})
                folio_vals.update({"room_line_ids": folio_lines})
                folio = hotel_folio_obj.create(folio_vals)
                for rm_line in folio.room_line_ids:
                    rm_line._onchange_product_id_warning()
                self.write({"folio_id": [(6, 0, folio.ids)], "state": "done"})
        return True
