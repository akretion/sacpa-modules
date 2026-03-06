import polars as pl

from odoo import fields, models


class DataMap(models.Model):
    _inherit = "data.map"

    transformation = fields.Selection(
        selection_add=[("animacare_corps",) * 2, ("animacare_urne",) * 2]
    )

    def _df_alter_animacare_corps(self, df):
        df = self._animacare_df_alter(df)
        return df

    def _df_alter_animacare_urne(self, df):
        df = self._animacare_df_alter(df)
        return df

    def _animacare_df_alter(self, df):
        # ajout colonne 'id' avec dossier comme clé"
        df = df.with_columns(pl.col("cremation").alias("id"))
        return df
