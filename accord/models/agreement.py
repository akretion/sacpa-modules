from odoo import Command, api, fields, models


class Agreement(models.Model):
    _inherit = "agreement"

    insee_refs = fields.Char(string="Communes", help="Provient du fichier d'import")
    partner_ids = fields.Many2many(
        comodel_name="res.partner",
        string="Partners",
        compute="_compute_partner_ids",
        readonly=False,
    )
    field_log_ids = fields.Many2many(comodel_name="field.log")
    statut = fields.Char(readonly=True)
    contrat = fields.Char(readonly=True)
    service_id = fields.Many2one(comodel_name="service.agreement")
    product_ids = fields.Many2many(
        comodel_name="product.product", related="service_id.product_ids", readonly=True
    )

    @api.depends("insee_refs")
    def _compute_partner_ids(self):
        for rec in self:
            if rec.insee_refs:
                rec.partner_ids = rec._get_communes()
            else:
                rec.partner_ids = False

    def _get_communes(self):
        """If insee/commune partner doesn't exists, this method'll create it."""
        insee_refs = [x for x in self.insee_refs.split("&") if x]

        def get_insee_map(codes):
            insee_p_map = {
                x.insee: x.id
                for x in self.env["res.partner"].search([("insee", "in", codes)])
            }
            missing_cities = [x for x in insee_refs if x not in insee_p_map.keys()]
            return insee_p_map, missing_cities

        insee_p_map, missing_cities = get_insee_map(insee_refs)
        if missing_cities:
            # Communes creation
            insee_c_map = {
                x.insee: x
                for x in self.env["res.city.zip"].search(
                    [("insee", "in", missing_cities)]
                )
            }
            for rec in [x for x in insee_c_map.values()]:
                self.env["res.partner"].create(rec._prepare_commune_vals())
            insee_p_map, missing_cities = get_insee_map(insee_refs)
            if missing_cities:
                # TODO purge log when ok
                self.env["field.log"].create(
                    {
                        "info": f"Missing insee codes {missing_cities}",
                        "res_id": self.id,
                        "field_id": self.env.ref(
                            "accord.field_agreement__partner_ids"
                        ).id,
                    }
                )
        if insee_p_map:
            return [Command.set([x for x in insee_p_map.values()])]
        return False

    def unlink(self):
        """Logs must be unlinked before the record to avoid
        integrity error on field_log_ids"""
        res = super().unlink()
        self.env["field.log"]._unlink_logs_from_unlinked_resources(
            "agreement", self.ids
        )
        return res
