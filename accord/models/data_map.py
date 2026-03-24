import polars as pl

from odoo import fields, models


class DataMap(models.Model):
    _inherit = "data.map"

    transformation = fields.Selection(selection_add=[("sacpa_agreement", "Accord")])

    def _df_pre_alter_sacpa_agreement(self, df):
        # define insee codes from commune list
        df = df.with_columns(insee=pl.col("insee_refs").str.split(by="&"))
        # on rajoute 0 si seulement 4 chiffres
        df = df.with_columns(
            insee=pl.col("insee").list.eval(
                pl.when(pl.element().str.len_chars() < 5)
                .then(pl.format("0{}", pl.element()))
                .otherwise(pl.element())
            )
        )
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
            return [f"Missing insee codes: {sorted(missing_insee)}"]
        return []

    def _df_alter_sacpa_agreement(self, df):
        # set column domain
        df = df.with_columns(domain=pl.lit("sale"))
        # define company
        cpny_map = {
            x.partner_id.ref: str(x.id)
            for x in self.env["res.company"].search([])
            if x.partner_id.ref
        }
        df = df.with_columns(code_cli=pl.lit("c") + pl.col("code_cli"))
        df = df.with_columns(company_id=pl.col("CodeDepot").str.replace_many(cpny_map))
        # TODO remove
        df, __ = self.env["df.process"]._df_filter_rows_when_no_numeric_val_in_column(
            df, "company_id"
        )
        # concatenate zip / city to create zipcity column for matching with res.city.zip
        df = df.with_columns(zipcity=pl.col("zip").cast(pl.String) + pl.col("city"))
        # add zip_city_id column with mapping from res.city.zip model and zipcity col
        df, unknown = self.env["df.process"]._subtitute_value_by_id_and_split(
            df, "res.city.zip", "zipcity", "zip_city_id"
        )
        df = df.with_columns(
            insee2=pl.when(pl.col("insee_refs").str.contains("&"))
            .then(pl.lit(""))
            .otherwise(pl.col("insee_refs"))
        )
        # df.select('insee', 'insee2')
        # search for partner_id in res.partner based on code_cli with partner ref
        # TODO code_cli ou insee
        # si code insee alors chercher par insee
        # si code_cli alors chercher par code_cli
        df = self.env["df.process"]._subtitute_value_by_id(
            df, "res.partner", "code_cli", "partner_id", ref_col="ref"
        )
        df, no_partner_df = self.env["df.process"]._subtitute_value_by_id_and_split(
            df, "res.partner", "insee2", "partner_id", ref_col="insee"
        )
        if not no_partner_df.is_empty():
            breakpoint()
            self._sacpa_agreement_create_missing_partners(no_partner_df)
        return df

    def _sacpa_agreement_create_missing_partners(self, no_partner_df):
        cols = ["zip_city_id", "client", "code_cli", "city", "street"]
        cols.extend(["street2", "phone", "mail", "insee_refs"])
        for part in no_partner_df.select(*cols).unique().to_dicts():
            zipcity = self.env["res.city.zip"].browse(part["zip_city_id"])
            self.env["res.partner"].create(
                self._sacpa_agreement_prepare_partner_vals(part, zipcity)
            )

    def _sacpa_agreement_prepare_partner_vals(self, partner, zipcity):
        res = {
            "name": partner["client"],
            "is_company": True,
            "zip_city_id": zipcity.id,
            "zip": zipcity.name,
            "city": zipcity.city_id.name,
            "ref": partner["code_cli"],
        }
        return res

    def _remove_cols_from_previewed_df(self, df):
        preview_df = super()._remove_cols_from_previewed_df(df)
        if self.transformation == "sacpa_agreement":
            cols = ["street", "street2", "phone", "mail", "domain"]
            cols += ["statut", "name", "code", "client"]
            return preview_df.drop(cols)
        return preview_df
