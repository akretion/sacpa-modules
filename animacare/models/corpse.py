from odoo import fields, models


class CorpseTransit(models.Model):
    _name = "corpse.transit"
    _description = "Animacare"
    _rec_name = "cremation"

    collector_id = fields.Many2one(comodel_name="res.partner", string="Point collecte")
    back_collector_id = fields.Many2one(
        comodel_name="res.partner", string="Collecte retour"
    )
    cremation = fields.Char("Id dossier de crémation")
    crematorium = fields.Char()
    animal = fields.Char("Type animal")
    breed = fields.Char("Race")
    weight = fields.Float("Poids")
    death_date = fields.Date(string="Date décès")
    date = fields.Date()
    return_date = fields.Date(string="Date retour", help="Date retour urne max")
    process = fields.Char("Type de crémation")
    initial_state = fields.Char("Statut initial")
    final_state = fields.Char("Statut final")
    operator1 = fields.Char()
    operator2 = fields.Char()
