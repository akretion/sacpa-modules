from odoo import fields, models


class ServiceAgreement(models.Model):
    _name = "service.agreement"
    _description = "Available services on agreements"

    name = fields.Char(required=True)
    code = fields.Char(required=True)
    product_ids = fields.Many2many(
        comodel_name="product.product",
        domain=[("type", "=", "service")],
        help="Available products for current service",
    )
    company_id = fields.Char(comodel_name="res.company")
