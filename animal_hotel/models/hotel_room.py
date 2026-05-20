import logging
from datetime import datetime, timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as dt

_logger = logging.getLogger(__name__)

try:
    import pytz
except (OSError, ImportError) as err:
    _logger.debug(err)


class HotelRoom(models.Model):
    _inherit = "hotel.room"
    _description = "Hotel Room"

    job_type = fields.Selection(
        selection=[
            ("pension", "Pension"),
            ("fourriere", "Fourriere"),
            ("refuge", "Refuge"),
        ],
        string="Type",
        compute="_compute_job_type_category",
        store=True,
    )

    @api.depends("room_categ_id")
    def _compute_job_type_category(self):
        for record in self:
            if record.room_categ_id:
                record.job_type = record.room_categ_id.job_type


class HotelRoomType(models.Model):
    _inherit = "hotel.room.type"

    job_type = fields.Selection(
        selection=[
            ("pension", "Pension"),
            ("fourriere", "Fourriere"),
            ("refuge", "Refuge"),
        ],
        string="Type",
    )


class RoomReservationSummary(models.Model):
    _inherit = "room.reservation.summary"

    def _get_domain_room(self):
        domain = []
        job_context = self.env.context.get("job_type", False)
        if job_context:
            domain = [("job_type", "=", job_context)]
        return domain

    @api.onchange("date_from", "date_to")  # noqa C901 (function is too complex)
    def get_room_summary(self):  # noqa C901 (function is too complex)
        """
        @param self: object pointer
        """
        domain_room = []
        domain_room = self._get_domain_room()
        res = {}
        all_detail = []
        room_obj = self.env["hotel.room"]
        reservation_line_obj = self.env["hotel.room.reservation.line"]
        folio_room_line_obj = self.env["folio.room.line"]
        user_obj = self.env["res.users"]
        date_range_list = []
        main_header = []
        summary_header_list = ["Rooms"]
        if self.date_from and self.date_to:
            if self.date_from > self.date_to:
                raise UserError(
                    self.env._("Checkout date should be later than Checkin date.")
                )
            if self._context.get("tz", False):
                timezone = pytz.timezone(self._context.get("tz", False))
            else:
                timezone = pytz.timezone("UTC")
            d_frm_obj = (
                (self.date_from)
                .replace(tzinfo=pytz.timezone("UTC"))
                .astimezone(timezone)
            )
            d_to_obj = (
                (self.date_to).replace(tzinfo=pytz.timezone("UTC")).astimezone(timezone)
            )
            temp_date = d_frm_obj
            while temp_date <= d_to_obj:
                val = ""
                val = (
                    str(temp_date.strftime("%a"))
                    + " "
                    + str(temp_date.strftime("%b"))
                    + " "
                    + str(temp_date.strftime("%d"))
                )
                summary_header_list.append(val)
                date_range_list.append(temp_date.strftime(dt))
                temp_date = temp_date + timedelta(days=1)
            all_detail.append(summary_header_list)
            room_ids = room_obj.search(domain_room)
            all_room_detail = []
            for room in room_ids:
                room_detail = {}
                room_list_stats = []
                room_detail.update({"name": room.name or ""})
                if not room.room_reservation_line_ids and not room.room_line_ids:
                    for chk_date in date_range_list:
                        room_list_stats.append(
                            {
                                "state": "Free",
                                "date": chk_date,
                                "room_id": room.id,
                            }
                        )
                else:
                    for chk_date in date_range_list:
                        ch_dt = chk_date[:10] + " 23:59:59"
                        ttime = datetime.strptime(ch_dt, dt)
                        c = ttime.replace(tzinfo=timezone).astimezone(
                            pytz.timezone("UTC")
                        )
                        chk_date = c.strftime(dt)
                        reserline_ids = room.room_reservation_line_ids.ids
                        reservline_ids = reservation_line_obj.search(
                            [
                                ("id", "in", reserline_ids),
                                ("check_in", "<=", chk_date),
                                ("check_out", ">=", chk_date),
                                ("state", "=", "assigned"),
                            ]
                        )
                        if not reservline_ids:
                            sdt = dt
                            chk_date = datetime.strptime(chk_date, sdt)
                            chk_date = datetime.strftime(
                                chk_date - timedelta(days=1), sdt
                            )
                            reservline_ids = reservation_line_obj.search(
                                [
                                    ("id", "in", reserline_ids),
                                    ("check_in", "<=", chk_date),
                                    ("check_out", ">=", chk_date),
                                    ("state", "=", "assigned"),
                                ]
                            )
                            for res_room in reservline_ids:
                                cid = res_room.check_in
                                cod = res_room.check_out
                                dur = cod - cid
                                if room_list_stats:
                                    count = 0
                                    for rlist in room_list_stats:
                                        cidst = datetime.strftime(cid, dt)
                                        codst = datetime.strftime(cod, dt)
                                        rm_id = res_room.room_id.id
                                        ci = rlist.get("date") >= cidst
                                        co = rlist.get("date") <= codst
                                        rm = rlist.get("room_id") == rm_id
                                        st = rlist.get("state") == "Reserved"
                                        if ci and co and rm and st:
                                            count += 1
                                    if count - dur.days == 0:
                                        c_id1 = user_obj.browse(self._uid)
                                        c_id = c_id1.company_id
                                        con_add = 0
                                        amin = 0.0
                                        # When configured_addition_hours is
                                        # greater than zero then we calculate
                                        # additional minutes
                                        if c_id:
                                            con_add = c_id.additional_hours
                                        if con_add > 0:
                                            amin = abs(con_add * 60)
                                        hr_dur = abs(dur.seconds / 60)
                                        if amin > 0:
                                            # When additional minutes is greater
                                            # than zero then check duration with
                                            # extra minutes and give the room
                                            # reservation status is reserved
                                            # --------------------------
                                            if hr_dur >= amin:
                                                reservline_ids = True
                                            else:
                                                reservline_ids = False
                                        else:
                                            if hr_dur > 0:
                                                reservline_ids = True
                                            else:
                                                reservline_ids = False
                                    else:
                                        reservline_ids = False
                        fol_room_line_ids = room.room_line_ids.ids
                        chk_state = ["draft", "cancel"]
                        folio_resrv_ids = folio_room_line_obj.search(
                            [
                                ("id", "in", fol_room_line_ids),
                                ("check_in", "<=", chk_date),
                                ("check_out", ">=", chk_date),
                                ("status", "not in", chk_state),
                            ]
                        )
                        if reservline_ids or folio_resrv_ids:
                            room_list_stats.append(
                                {
                                    "state": "Reserved",
                                    "date": chk_date,
                                    "room_id": room.id,
                                    "is_draft": "No",
                                    "data_model": "",
                                    "data_id": 0,
                                }
                            )
                        else:
                            room_list_stats.append(
                                {
                                    "state": "Free",
                                    "date": chk_date,
                                    "room_id": room.id,
                                }
                            )

                room_detail.update({"value": room_list_stats})
                all_room_detail.append(room_detail)
            main_header.append({"header": summary_header_list})
            self.summary_header = str(main_header)
            self.room_summary = str(all_room_detail)
        return res
