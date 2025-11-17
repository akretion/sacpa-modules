# Akretion Copyright (c) 2025 Author. All Rights Reserved.
#

from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    webhook_id = fields.Many2one("webhook.move", string="webhook connector")

    state_webhook = fields.Selection(
        [
            ("no_return", "Pas de retour"),
            ("to_validate", "Conforme"),
            ("to_correct", "A corriger"),
        ],
        string="Etat demat",
        default="no_return",
        compute="_compute_state_webhook",
    )
    ttc_ok = fields.Boolean(
        string="Amount TTC_webhook = TTC_invoice", compute="_compute_ttc"
    )
    tva_ok = fields.Boolean(
        string="Amount TVA_webhook = TVA_invoice", compute="_compute_tva"
    )

    # address_ok = fields.Boolean(string="address webhook = invoice")
    @api.depends("amount_total", "webhook_id")
    def _compute_ttc(self):
        for record in self:
            val = False
            if record.webhook_id:
                if float(record.webhook_id.mt_ttc) == record.amount_total:
                    val = True
            record.ttc_ok = val

    @api.depends("amount_tax", "webhook_id")
    def _compute_tva(self):
        for record in self:
            val = False
            if record.webhook_id:
                if float(record.webhook_id.mt_tva) == record.amount_tax:
                    val = True
            record.tva_ok = val

    @api.onchange("webhook_id", "state_webhook", "ttc_ok")
    def _compute_state_webhook(self):
        for record in self:
            if record.webhook_id:
                if record.ttc_ok:
                    record.state_webhook = "to_validate"
                else:
                    record.state_webhook = "to_correct"
