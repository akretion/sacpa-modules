# Copyright (C) 2025 - TODAY, Akretion
# @author Mourad EL HADJ MIMOUNE <mourad.elhadj.mimoune@akretion.com>

from datetime import date

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class FSMOrder(models.Model):
    _inherit = "fsm.order"

    # Détails d'intervention
    request_ref = fields.Char(string="Référence Demande")
    intervention_number = fields.Integer(string="N° Intervention")
    internal_reference = fields.Char(string="N° Interne")
    intervention_date = fields.Date(string="Date d'intervention")
    intervention_type_id = fields.Many2one(
        "helpdesk.intervention.type", string="Type d'intervention"
    )

    departure_time = fields.Float(string="Heure de départ")
    arrival_time = fields.Float(string="Heure d'arrivée")
    capture_time = fields.Float(string="Heure de capture")
    return_time = fields.Float(string="Heure de retour")

    # Bloc Animaux
    animal_order_number = fields.Char(string="N° Animal Intervention")
    tattoo_number = fields.Char(string="N° Tatouage")
    chip_number = fields.Char(string="N° Puce")
    medal_number = fields.Char(string="N° Médaille")
    specie_id = fields.Many2one("animal.species", string="Espèce")
    breed_id = fields.Many2one("animal.breed", string="Race")
    is_crossbreed = fields.Boolean(string="Croisé ?")
    crossbreed_breed_id = fields.Many2one("animal.breed", string="Race de croisement")
    gender = fields.Selection([("male", "Mâle"), ("female", "Femelle")], string="Sexe")
    animal_name = fields.Char(string="Nom de l’animal")
    pickup_location = fields.Char(string="Lieu de ramassage")
    birth_date = fields.Date(string="Date de naissance")
    calculated_age = fields.Char(
        string="Âge calculé", compute="_compute_calculated_age"
    )
    estimated_age_min_month = fields.Integer(string="Âge estimé (min) mois")
    estimated_age_min_year = fields.Integer(string="Âge estimé (min) année")
    estimated_age_max_month = fields.Integer(string="Âge estimé (max) mois")
    estimated_age_max_year = fields.Integer(string="Âge estimé (max) année")
    estimation_date = fields.Date(string="Date de l'Estimation")
    # caractéristiques
    animal_status_id = fields.Many2one("animal.status", string="Statut")
    size = fields.Selection(
        [("petit", "Petit"), ("moyen", "Moyen"), ("grand", "Grand")], string="Taille"
    )
    ears = fields.Selection(
        [("droites", "Droites"), ("tombantes", "Tombantes"), ("autres", "Autres")],
        string="Oreilles",
    )
    tail = fields.Selection(
        [("entiere", "Entière"), ("ecourtee", "Écourtée")], string="Queue"
    )
    hair = fields.Selection(
        [("court", "Court"), ("mi-long", "Mi-long"), ("long", "Long")], string="Poil"
    )
    color1 = fields.Char(string="Couleur 1")
    color2 = fields.Char(string="Couleur 2")
    color3 = fields.Char(string="Couleur 3")
    color4 = fields.Char(string="Couleur 4")
    pattern = fields.Char(string="Dessin")
    is_sterilized = fields.Boolean(string="Stérilisé")
    folder_pound_number = fields.Char(string="N° Dossier Fourrière")
    collar = fields.Char(string="Collier")
    leash = fields.Char(string="Laisse")
    muzzle = fields.Char(string="Muselière")
    other_restraints = fields.Char(string="Autre (attache)")
    behavior = fields.Text(string="Comportement")
    health_status = fields.Many2one("animal.health.status", string="État sanitaire")
    legal_deposit = fields.Many2one("res.partner", string="Dépôt légal")

    @api.depends("birth_date")
    def _compute_calculated_age(self):
        for record in self:
            if record.birth_date:
                today = date.today()
                delta = relativedelta(today, record.birth_date)
                years = delta.years
                months = delta.months
                record.calculated_age = f"{years} an(s) {months} mois"
            else:
                record.calculated_age = ""
