from odoo import fields, models

MODULE = __name__[12 : __name__.index(".", 13)]


class DataMap(models.Model):
    _inherit = "data.map"

    transformation = fields.Selection(
        selection_add=[("vigipet_found",) * 2, ("vigipet_lost",) * 2]
    )

    def _df_transform(self):
        elm = super()._df_transform()
        if self.transformation == "vigipet_found":
            elm.append(
                (
                    "col",
                    "pl.lit('found').alias('domain')  # ajout de la colonne domain "
                    + "avec la valeur 'found' pour les animaux trouvés",
                )
            )
        elif self.transformation == "vigipet_lost":
            elm.append(
                (
                    "col",
                    "pl.lit('lost').alias('domain')  # ajout de la colonne domain "
                    + "avec la valeur 'lost' pour les animaux perdus",
                )
            )
        if self.transformation in ("vigipet_found", "vigipet_lost"):
            for col in (
                "Race Chien",
                "Race Chat",
                "Race NAC",
                "Couleur Chien",
                "Couleur Chat",
            ):
                mapping = {"-": "", "  ": " "}
                elm.append(
                    ("col", f"pl.col('{col}').replace({mapping}).alias('{col}')")
                )
            elm.append(
                ("col", "pl.col('sex').str.to_lowercase().alias('sex')  # minuscule")
            )
            elm.append(
                (
                    "col",
                    "pl.col('specie').str.to_lowercase().str.replace_many({'autres': "
                    + "'autre', 'nac (veuillez préciser dans \"race\")': 'nac'})"
                    + ".alias('specie')",
                )
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
                elm.append(
                    (
                        "col",
                        f"pl.col('{col}').str.replace_many({yes_no}).alias('{col}')",
                    )
                )
            elm.append(
                (
                    "col",
                    "(pl.col('Race Chien') + pl.col('Race Chat') + pl.col('Race NAC'))"
                    + ".alias('breed')",
                )
            )
            elm.append(
                (
                    "col",
                    "(pl.col('Couleur Chien') + pl.col('Couleur Chat')).alias('color')",
                )
            )
        return elm
