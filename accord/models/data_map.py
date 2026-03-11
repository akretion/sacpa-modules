import polars as pl

from odoo import fields, models

MODULE = __name__[12 : __name__.index(".", 13)]


class DataMap(models.Model):
    _inherit = "data.map"

    transformation = fields.Selection(selection_add=[("sacpa_agreement", "Accord")])

    def _df_pre_alter_sacpa_agreement(self, df):
        # define insee codes from commune list
        df = df.with_columns(insee=pl.col("ListeCommunes").str.split(by="&"))
        return df

    def _df_validate_sacpa_agreement(self, df):
        # liste of insee codes from the dataframe
        insee = (
            (df.explode("insee").select(pl.col("insee").unique()))
            .get_column("insee")
            .to_list()
        )
        # check if insee codes exist in res.city.zip model
        existing_codes = (
            self.env["res.city.zip"].search([("insee", "in", insee)]).mapped("insee")
        )
        missing_insee = [x for x in insee if x not in existing_codes and x]
        if missing_insee:
            return [f"Missing insee codes: {', '.join(missing_insee)}"]
        return []

    def _df_alter_sacpa_agreement(self, df):
        # set column domain
        df = df.with_columns(domain=pl.lit("sale"))
        # define company
        # cpny_map = {
        #     x.name: str(x.id)
        #     for x in self.env["res.company"].search([])
        #     if "SACPA" in x.name and x.name != "SACPA"
        # }
        # df = df.with_columns(
        #     company_id=pl.col("CodeDepot")
        #     .str.replace(r"(\w+)_SA", r"SACPA $1")
        #     .str.replace_many(cpny_map)
        #     .cast(pl.Int32)
        # )
        return df

    def _remove_cols_from_previewed_df(self, df):
        preview_df = super()._remove_cols_from_previewed_df(df)
        if self.transformation == "sacpa_agreement":
            cols = ["street", "street2", "phone", "mail", "domain"]
            cols += ["ETAT STATUT CONTRAT", "name", "code", "client"]
            return preview_df.drop(cols)
        return preview_df
