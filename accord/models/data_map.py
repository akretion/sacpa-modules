import polars as pl

from odoo import fields, models


class DataMap(models.Model):
    _inherit = "data.map"

    transformation = fields.Selection(selection_add=[("sacpa_agreement", "Accord")])

    def _df_pre_alter_sacpa_agreement(self, df):
        # define insee codes from commune list
        df = df.with_columns(insee=pl.col("ListeCommunes").str.split(by="&"))
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
            x.name: str(x.id)
            for x in self.env["res.company"].search([])
            if "SACPA" in x.name and x.name != "SACPA"
        }
        df = df.with_columns(
            company_id=pl.col("CodeDepot")
            .str.replace(r"(\w+)_SA", r"SACPA $1")
            .str.replace_many(cpny_map)
            .cast(pl.Int32)
        )
        # concatenate zip / city to create zipcity column for matching with res.city.zip
        df = df.with_columns(zipcity=pl.col("zip").cast(pl.String) + pl.col("city"))
        # add zip_city_id column with mapping from res.city.zip model and zipcity col
        df, unknown = self._subtitute_value_by_id(
            df, "res.city.zip", "zipcity", "zip_city_id"
        )
        # search for partner_id in res.partner based on code_cli with partner ref
        params = "res.partner", "code_cli", "partner_id"
        df, no_partner = self._subtitute_value_by_id(df, *params, ref_col="ref")
        if not no_partner.is_empty():
            self._sacpa_agreement_create_missing_partners(no_partner)
        return df

    def _sacpa_agreement_create_missing_partners(self, df):
        for part in df.select("zip_city_id", "code_cli", "city").unique().to_dicts():
            zipcity = self.env["res.city.zip"].browse(part["zip_city_id"])
            self.env["res.partner"].create(
                self._sacpa_agreement_prepare_partner_vals(part, zipcity)
            )

    def _sacpa_agreement_prepare_partner_vals(self, part_dict, zipcity):
        return {
            "name": part_dict["city"],
            "is_company": True,
            "zip": zipcity.name,
            "city": zipcity.city_id.name,
            "ref": part_dict["code_cli"],
        }

    def _remove_cols_from_previewed_df(self, df):
        preview_df = super()._remove_cols_from_previewed_df(df)
        if self.transformation == "sacpa_agreement":
            cols = ["street", "street2", "phone", "mail", "domain"]
            cols += ["ETAT STATUT CONTRAT", "name", "code", "client"]
            return preview_df.drop(cols)
        return preview_df
