import polars as pl

from odoo import fields, models

MODULE = __name__[12 : __name__.index(".", 13)]


class DataMap(models.Model):
    _inherit = "data.map"

    transformation = fields.Selection(
        selection_add=[("vigipet_found",) * 2, ("vigipet_lost",) * 2]
    )

    def _df_alter(self, df):
        "Method is firstly parsed by inspect before to be executed"
        df = super()._df_alter(df)
        clean_empty_field = {"-": "", "  ": " "}
        if self.transformation == "vigipet_found":
            # ajout de la colonne domain avec la valeur 'found' pour les animaux trouvés
            df = df.with_columns(pl.lit("found").alias("domain"))
        if self.transformation == "vigipet_lost":
            # ajout de la colonne domain avec la valeur 'lost' pour les animaux perdus
            df = df.with_columns(pl.lit("lost").alias("domain"))
            for col in (
                "Race Chien",
                "Race Chat",
                "Race NAC",
                "Couleur Chien",
                "Couleur Chat",
            ):  # noqa
                df = df.with_columns(pl.col(col).replace(clean_empty_field).alias(col))
        if self.transformation in ("vigipet_found", "vigipet_lost"):
            df = df.with_columns(
                pl.col("sex").str.to_lowercase().alias("sex")
            )  # minuscule"  # noqa
            df = df.with_columns(
                pl.col("specie")
                .str.to_lowercase()
                .str.replace_many(
                    {"autres": "autre", 'nac (veuillez préciser dans "race")': "nac"}
                )
                .alias("specie")
            )  # noqa
            yes_no = {
                "Oui": "1",
                "Non": "0",
                "-": "0",
                "yes": "1",
                "Non accepté": "0",
                "Non merci": "0",
                "Je ne sais pas": "0",
            }  # noqa
            cols = (
                "sterilized",
                "identified",
                "crossbred",
                "consentement1",
                "consentement2",
            )  # noqa
            for col in cols:
                df = df.with_columns(pl.col(col).str.replace_many(yes_no).alias(col))
            df = df.with_columns(
                (pl.col("Race Chien") + pl.col("Race Chat") + pl.col("Race NAC")).alias(
                    "breed"
                )
            )  # noqa
            df = df.with_columns(
                (pl.col("Couleur Chien") + pl.col("Couleur Chat")).alias("color")
            )  # noqa
        return df
