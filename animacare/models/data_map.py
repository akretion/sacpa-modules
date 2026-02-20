from odoo import fields, models

MODULE = __name__[12 : __name__.index(".", 13)]


class DataMap(models.Model):
    _inherit = "data.map"

    transformation = fields.Selection(
        selection_add=[("animacare_corps",) * 2, ("animacare_urne",) * 2]
    )

    def _additionnal_df_columns_hook(self):
        cols = super()._additionnal_df_columns_hook()
        if self.transformation == "animacare_corps":
            cols["id"] = (
                "pl.col('cremation').alias('id')  # ajout colonne 'id' "
                + "avec dossier comme clé"
            )
        return cols

    # def _add_checks_df_columns_hook(self, df):
    #     df, cols = super()._add_checks_df_columns_hook(df)
    #     if "collector_id" in df.columns:
    #         res = df.filter(df["ref"].is_duplicated())
    #         cols["ref"] = {"Références en doublon (ref)": res}
    #     return df, cols
