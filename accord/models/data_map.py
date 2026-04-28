import logging

import polars as pl

from odoo import exceptions, fields, models

logger = logging.getLogger(__name__)


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
        sql = df.sql("SELECT code_cli FROM self")
        sql = sql.get_column("code_cli").to_list()
        if sql and sql[0][0] == "c":
            df = df.with_columns(code_cli=pl.lit("c") + pl.col("code_cli"))
        df = self._sacpa_agreement_get_missing_partners(df)
        df = self.env["df.process"]._subtitute_value_by_id(
            df, "service.agreement", "contrat", "service_id", ref_col="code"
        )
        df = df.with_columns(
            service_id=pl.col("service_id").cast(pl.Int64, strict=False)
        )
        return df

    def _df_validate_sacpa_agreement(self, df):
        listing = []
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
            listing.append(f"Missing insee codes: {sorted(missing_insee)}")
        if "partner_id" in df.columns:
            nan = (
                df.filter(pl.col("partner_id").str.contains(r"\D"))
                .get_column("partner_id")
                .to_list()
            )
            listing.append(f"Partners inconnus {nan}")
        return listing

    def _sacpa_agreement_get_missing_partners(self, df):
        # define company
        original_df = df
        cpny_map = {
            x.company_ref: str(x.id)
            for x in self.env["res.company"].search([])
            if x.company_ref
        }
        df = df.with_columns(company_id=pl.col("CodeDepot").str.replace_many(cpny_map))
        # TODO remove
        df, excluded = self.env[
            "df.process"
        ]._df_filter_rows_when_no_numeric_val_in_column(df, "company_id")
        if not excluded.is_empty():
            logger.warning(excluded)
            raise exceptions.ValidationError(
                f"Des sociétés ne sont pas reconnues {excluded}"
            )
        # concatenate zip / city to create zipcity column for matching with res.city.zip
        df = df.with_columns(zipcity=pl.col("zip").cast(pl.String) + pl.col("city"))
        # add zip_city_id column with mapping from res.city.zip model and zipcity col

        df, unknown = self.env["df.process"]._subtitute_value_by_id_and_split(
            df, "res.city.zip", "zipcity", "zip_city_id"
        )
        if not unknown.is_empty():
            comma = unknown.sql("SELECT * FROM self WHERE insee_refs LIKE '%,%'")
            if not comma.is_empty():
                raise exceptions.ValidationError(f"To many insee codes here {unknown}")
            for elm in unknown.select("insee_refs", "code_cli").to_dicts():
                czip = self.env["res.city.zip"].search(
                    [("insee", "=", elm["insee_refs"])], limit=1
                )
                if czip and not self.env["res.partner"].search(
                    [("zip_city_id", "=", czip.id)]
                ):
                    vals = czip._prepare_commune_vals()
                    vals.update({"ref": elm["code_cli"]})
                    self.env["res.partner"].create(vals)
        df = self.env["df.process"]._subtitute_value_by_id(
            df, "res.partner", "code_cli", "partner_id", ref_col="ref"
        )
        return df

    def _df_alter_sacpa_agreement(self, df):
        original_df = df
        # set column domain
        df = df.with_columns(domain=pl.lit("sale"))

        def code_cli_to_partner_id(df):
            ref = df.get_column("code_cli").to_list()
            mapp = {
                x.ref: str(x.id)
                for x in self.env["res.partner"].search([("ref", "in", ref)])
                if x.ref
            }
            return df.with_columns(pl.col("partner_id").str.replace_many(mapp))

        df = code_cli_to_partner_id(df)
        no_partner_df = df.filter(pl.col("partner_id").str.contains(r"\D"))
        if not no_partner_df.is_empty():
            logger.info("Create missing partners")
            self._sacpa_agreement_create_missing_partners(no_partner_df)
            # We renew alteration with new partners
            return self._df_alter_sacpa_agreement(original_df)
        df = df.with_columns(partner_id=pl.col("partner_id").cast(pl.Int64))
        return df

    def _sacpa_agreement_create_missing_partners(self, no_partner_df):
        cols = ["zip_city_id", "client", "code_cli", "city", "street"]
        cols.extend(["street2", "phone", "mail", "insee_refs"])
        for part in no_partner_df.select(*cols).unique().to_dicts():
            zipcity = self.env["res.city.zip"].browse(part["zip_city_id"])
            # TODO bad performance here
            existing = self.env["res.partner"].search(
                [("zip_city_id", "=", zipcity.id)]
            )
            if existing:
                existing[0].ref = part["code_cli"]
            else:
                vals = zipcity._prepare_commune_vals()
                vals["name"] = part["client"]
                vals["ref"] = part["code_cli"]
                self.env["res.partner"].create(vals)

    def _remove_cols_from_previewed_df(self, df):
        preview_df = super()._remove_cols_from_previewed_df(df)
        if self.transformation == "sacpa_agreement":
            cols = ["street", "street2", "phone", "mail", "domain"]
            cols += ["statut", "name", "code", "client"]
            cols = [x for x in cols if x in df.columns and x != "N°"]
            return preview_df.drop(cols)
        return preview_df
