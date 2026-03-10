import polars as pl

from odoo import fields, models

MODULE = __name__[12 : __name__.index(".", 13)]


class DataMap(models.Model):
    _inherit = "data.map"

    transformation = fields.Selection(selection_add=[("agreement", "Accord")])

    def _df_alter_agreement(self, df):
        df = df.with_columns(domain=pl.lit("sale"))
        cpny_map = {x.name: str(x.id) for x in self.env["res.company"].search([])}
        df = df.with_columns(
            company_id=pl.col("CodeDepot").str.replace(r"(\w+)_SA", r"SACPA $1")
        )
        df = df.with_columns(company_id=pl.col("company_id").str.replace_many(cpny_map))
        return df

    def _remove_cols_from_previewed_df(self, df):
        preview_df = super()._remove_cols_from_previewed_df(df)
        if self.transformation == "agreement":
            cols = ["street", "street2", "zip", "city", "phone", "mail", "domain"]
            cols += ["ETAT STATUT CONTRAT", "name"]
            return preview_df.drop(cols)
        return preview_df
