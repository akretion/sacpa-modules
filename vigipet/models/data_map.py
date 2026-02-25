from odoo import fields, models

MODULE = __name__[12 : __name__.index(".", 13)]


class DataMap(models.Model):
    _inherit = "data.map"

    transformation = fields.Selection(
        selection_add=[("vigipet_found",) * 2, ("vigipet_lost",) * 2]
    )

    def _additionnal_df_columns_hook(self):
        cols = super()._additionnal_df_columns_hook()
        if self.transformation == "vigipet_found":
            cols["domain"] = (
                "pl.lit('found')  # ajout de la colonne domaine avec "
                + "la valeur 'found' pour les animaux trouvés"
            )
        elif self.transformation == "vigipet_lost":
            cols["domain"] = (
                "pl.lit('lost')  # ajout de la colonne domaine avec "
                + "la valeur 'lost' pour les animaux trouvés"
            )
        if self.transformation in ("vigipet_found", "vigipet_lost"):
            for col in (
                "Race Chien",
                "Race Chat",
                "Race NAC",
                "Couleur Chien",
                "Couleur Chat",
            ):
                cols[col] = f"pl.col('{col}')" + ".replace({'-': '', '  ': ' '})"
            cols["sex"] = "pl.col('sex').str.to_lowercase()  # minuscule"
            cols["specie"] = (
                "pl.col('specie').str.to_lowercase().str.replace_many({'autres': "
                + "'autre', 'nac (veuillez préciser dans \"race\")': 'nac'})"
            )
            yes_no = (
                "{'Oui': '1', 'Non': '0', '-': '0', 'yes': '1', "
                + "'Non accepté': '0', 'Non merci': '0', 'Je ne sais pas': '0'}"
            )
            for col in (
                "sterilized",
                "identified",
                "crossbred",
                "consentement1",
                "consentement2",
            ):
                cols[col] = f"pl.col('{col}').str.replace_many({yes_no})"
            cols["breed"] = (
                "(pl.col('Race Chien') + pl.col('Race Chat') + pl.col('Race NAC'))"
                + ".alias('breed')"
            )
            cols["color"] = (
                "(pl.col('Couleur Chien') + pl.col('Couleur Chat')).alias('color')"
            )
        return cols
