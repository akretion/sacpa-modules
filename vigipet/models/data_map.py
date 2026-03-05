import polars as pl

from odoo import fields, models


class DataMap(models.Model):
    _inherit = "data.map"

    transformation = fields.Selection(
        selection_add=[("vigipet_found",) * 2, ("vigipet_lost",) * 2]
    )

    def _df_alter(self, df):
        "Method is firstly parsed by inspect before to be executed"
        df = super()._df_alter(df)
        clean_empty_field = {"-": "", "  ": " "}
        breed_color_c = (
            "Race Chien",
            "Race Chat",
            "Race NAC",
            "Couleur Chien",
            "Couleur Chat",
        )
        mapping_specie = {
            "autres": "autre",
            'nac (veuillez préciser dans "race")': "nac",
        }
        yes_no_mapping = {
            "Oui": "1",
            "Non": "0",
            "-": "0",
            "yes": "1",
            "Non accepté": "0",
            "Non merci": "0",
            "Je ne sais pas": "0",
        }
        if self.transformation in ("vigipet_found", "vigipet_lost"):
            if self.transformation == "vigipet_found":
                # ajout colonne domain avec la valeur 'found' pour les animaux trouvés
                df = df.with_columns(pl.lit("found").alias("domain"))
            if self.transformation == "vigipet_lost":
                # ajout colonne domain avec la valeur 'lost' pour les animaux perdus
                df = df.with_columns(pl.lit("lost").alias("domain"))
            for col in breed_color_c:  # Race Chien, Chat, NAC, Couleur Chien, Chat
                df = df.with_columns(pl.col(col).replace(clean_empty_field).alias(col))
            df = df.with_columns(pl.col("sex").str.to_lowercase().alias("sex"))
            df = df.with_columns(
                pl.col("specie").str.to_lowercase().str.replace_many(mapping_specie)
            )
            cols = [
                x
                for x in (
                    "sterilized",
                    "identified",
                    "crossbred",
                    "consent1",
                    "consent2",
                )
                if x in df.columns
            ]
            # TODO
            for col in cols:
                df = df.with_columns(  # "Oui": "1", "Non": "0", "-": "0"
                    pl.col(col).str.replace_many(yes_no_mapping).alias(col)
                )
            df = df.with_columns(
                (pl.col("Race Chien") + pl.col("Race Chat") + pl.col("Race NAC")).alias(
                    "breed"
                )
            )
            df = df.with_columns(
                (pl.col("Couleur Chien") + pl.col("Couleur Chat")).alias("color")
            )
        return df
