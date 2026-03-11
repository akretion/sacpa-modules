from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    # TODO make it m2o
    insee = fields.Char(compute="_compute_insee", store=True)

    @api.depends("city_id", "zip")
    def _compute_insee(self):
        for rec in self:
            if rec.city_id and rec.zip:
                city = self.env["res.city.zip"].search(
                    [("city_id", "=", rec.city_id.id), ("name", "=", rec.zip)], limit=1
                )
                rec.insee = city.insee if city else False
            else:
                rec.insee = False

    def _complete_city_id(self):
        """Complete city_id based on city name and zip code.
        To be used in a post_init_hook or standalone cli:
        env["res.partner"]._complete_city_id()
        """
        parts = self.search([("city_id", "=", False), ("is_company", "=", True)])
        map_city = {
            x.name: x.id
            for x in self.env["res.city"].search([("name", "in", parts.mapped("city"))])
            if x.zip_ids and len(x.zip_ids) == 1
        }
        for rec in parts:
            if map_city.get(rec.city):
                rec.city_id = map_city.get(rec.city)
