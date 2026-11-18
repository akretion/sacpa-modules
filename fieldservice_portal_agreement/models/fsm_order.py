# Copyright (C) 2026 - TODAY, Akretion
# @author Mourad EL HADJ MIMOUNE <mourad.elhadj.mimoune@akretion.com>

from odoo import fields, models


class FsmOrder(models.Model):
    _inherit = "fsm.order"

    # Stored copy of the agreement holder (e.g. the EPCI), used by the portal
    # record rule: it sees every record of its agreement, while the other
    # agreement partners (communes) only see their own.
    # The rule must not traverse agreement_id: some portal controllers
    # (helpdesk_mgmt) re-apply the rule domain as a regular search domain,
    # which would require read access on agreement for portal users.
    agreement_partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Agreement Partner",
        related="agreement_id.partner_id",
        store=True,
        index=True,
    )
