from odoo import fields, models


class AnimalCare(models.Model):
    _name = "animal.care"
    _description = "Animale care"

    name = fields.Char(string="Nom du soin")
    date = fields.Date(string="Date du soin")
    animal_id = fields.Many2one("animal.identification", string="animal")
    value = fields.Many2one("animal.care.definition", string="Soins appliquer")


class AnimaleCareDéfinition(models.Model):
    _name = "animal.care.definition"
    _description = "Définition du soin éffectué"

    name = fields.Char(string="Nom du soins")
    note = fields.Text(string="Information sur le soin")


class AnimalVetVisit(models.Model):
    _name = "animal.vet.visit"
    _description = "Visite vétérinaire"

    before_date = fields.Date(string="A planifier avant le ")
    after_date = fields.Date(string="A planifier après le")
    date = fields.Date(string="Date du rdv")
    state_date = fields.Selection(
        [("confirm", "confirmer"), ("to_confirm", "Provisoire")],
        string="Etat de la date de rdv",
    )
    partner_id = fields.Many2one("res.partner", string="Vétérinaire contact")
    visit_state = fields.Selection(
        [("waitting", "En attente"), ("canceled", "Annulé"), ("confirm", "Confirmé")],
        string="Etat de la visite",
        default="waitting",
    )
    subjet = fields.Selection([("soin", "soin1")], string="Objet")
    reason = fields.Selection([("beethen", "mordeur")], string="Motifs")
    other_reason = fields.Text(string="Autre motif")

    animal_id = fields.Many2one("animal.identification", string="Animal")
    # Pour le relever du poids faire avec l'interface.
    # Mettre dans la vue le liens vers le poids de l'animal.
    #
    actes_id = fields.Many2many("animal.care.acte", string="Actes de soins")
    traitement = fields.Many2many("animal.care.treatment", string="Traitement délivré")


class AnimalCareTreatment(models.Model):
    _name = "animal.care.treatment"
    _description = "Traitement délivré au animaux"

    name = fields.Char(string="Nom")
    start_date = fields.Date(string="Date de début")
    end_date = fields.Date(string="Date de fin")
    medic = fields.Char(string="Produit/Médicament")
    nb_medic = fields.Float(string="Posologie (nb d'unité)")
    fq_nb = fields.Float(string="Nombre de fois")
    fq_time = fields.Selection(
        [
            ("all", "Tous le jours"),
            ("2_days", "Tous les 2 jours"),
            ("3_days", "Tous les 3 jours"),
            ("4_days", "Tous les 4 jours"),
            ("5_days", "Tous les 5 jours"),
            ("6_days", "Tous les 6 jours"),
            ("7_days", "Tous les 7 jours"),
        ]
    )
    duration = fields.Float(string="Durée en jours")
    comment = fields.Text(string="Commentaires")
    animal_id = fields.Many2one("animal.identification", string="Animal")
