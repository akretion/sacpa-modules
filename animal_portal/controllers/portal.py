# Copyright (C) 2026 - TODAY, Akretion
# @author Mourad EL HADJ MIMOUNE <mourad.elhadj.mimoune@akretion.com>

from odoo import http
from odoo.http import request

from odoo.addons.fieldservice_portal.controllers.fsm_order_portal import (
    CustomerPortal as FsmCustomerPortal,
)
from odoo.addons.helpdesk_mgmt.controllers.myaccount import CustomerPortalHelpdesk


class AnimalPortalHelpdesk(CustomerPortalHelpdesk):
    def _ticket_get_searchbar_sortings(self):
        sortings = super()._ticket_get_searchbar_sortings()
        # Default sort ("date"): most recent call first, as on the old extranet
        sortings["date"]["order"] = "call_date desc, call_time desc, create_date desc"
        return sortings

    def _ticket_get_page_view_values(self, ticket, access_token, **kwargs):
        values = super()._ticket_get_page_view_values(ticket, access_token, **kwargs)
        # The ticket is already access-checked: list its interventions in sudo
        values["fsm_orders"] = ticket.sudo().fsm_order_ids.sorted(
            lambda o: (o.intervention_date or o.create_date.date(), o.id)
        )
        return values


class AnimalPortalFsm(FsmCustomerPortal):
    def _get_portal_ticket_filter(self):
        """Ticket used to filter the intervention list (?ticket_id=…), if any."""
        ticket_id = request.params.get("ticket_id")
        if not ticket_id or not str(ticket_id).isdigit():
            return request.env["helpdesk.ticket"]
        ticket = request.env["helpdesk.ticket"].browse(int(ticket_id)).exists()
        # Only keep the filter on a ticket the user is allowed to read
        return ticket if ticket and ticket.has_access("read") else ticket.browse()

    def _prepare_fsm_orders_domain(self):
        domain = super()._prepare_fsm_orders_domain()
        ticket = self._get_portal_ticket_filter()
        if ticket:
            domain = domain + [("ticket_id", "=", ticket.id)]
        return domain

    @http.route()
    def portal_my_fsm_orders(self, *args, **kw):
        response = super().portal_my_fsm_orders(*args, **kw)
        if hasattr(response, "qcontext"):
            response.qcontext["filter_ticket"] = self._get_portal_ticket_filter().sudo()
        return response
