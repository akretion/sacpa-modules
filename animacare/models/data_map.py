import polars as pl

from odoo import fields, models


class DataMap(models.Model):
    _inherit = "data.map"

    transformation = fields.Selection(
        selection_add=[("animacare_corps",) * 2, ("animacare_urne",) * 2]
    )

    def _df_alter(self, df):
        "Method is firstly parsed by inspect before to be executed"
        df = super()._df_alter(df)
        if self.transformation == "animacare_corps":
            # ajout colonne 'id' avec dossier comme clé"
            df = df.with_columns(pl.col("cremation").alias("id"))
        if self.transformation in ("animacare_corps", "animacare_urne"):
            # ajout colonne 'id' avec dossier comme clé"
            df = df.with_columns(pl.col("cremation").alias("id"))
        return df
