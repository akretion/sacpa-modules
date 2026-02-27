from odoo import fields, models


class DataMap(models.Model):
    _inherit = "data.map"

    transformation = fields.Selection(
        selection_add=[("animacare_corps",) * 2, ("animacare_urne",) * 2]
    )

    def _df_transform(self):
        elm = super()._df_transform()
        if self.transformation == "animacare_corps":
            elm.append(
                (
                    "col",
                    "pl.col('cremation').alias('id')  # ajout colonne 'id' "
                    + "avec dossier comme clé",
                )
            )
        return elm
