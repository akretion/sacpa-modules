# Copyright (C) 2025 - TODAY, Akretion
# @author Mourad EL HADJ MIMOUNE <mourad.elhadj.mimoune@akretion.com>

from datetime import date

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class AnimalIdentification(models.Model):
    _name = "animal.identification"
    _description = "Fiche d'identification de l'animal"
    _order = "name"

    name = fields.Char(string="Nom")
    fiche_number = fields.Char(string="N° Fiche", required=True)
    coaxis_id = fields.Char(
        string="ID coaxis",
    )
    species_id = fields.Many2one("animal.species", string="Espèce")
    breed_id = fields.Many2one("animal.breed", string="Race")
    is_crossed = fields.Boolean(string="Croisé")
    breed2_id = fields.Many2one(
        "animal.breed",
        string="Race-croisé",
    )
    gender = fields.Selection([("male", "Mâle"), ("female", "Femelle")], string="Sexe")
    chip_number = fields.Char(string="N° Puce")
    tattoo_number = fields.Char(string="N° Tatouage")
    medal_number = fields.Char(string="N° Médaille")
    birth_date = fields.Date(string="Date de Naissance")
    calculated_age = fields.Char(
        string="Âge calculé", compute="_compute_calculated_age"
    )
    estimated_age_min_month = fields.Integer(string="Âge estimé (min) mois")
    estimated_age_min_year = fields.Integer(string="Âge estimé (min) année")
    estimated_age_max_month = fields.Integer(string="Âge estimé (max) mois")
    estimated_age_max_year = fields.Integer(string="Âge estimé (max) année")
    estimation_date = fields.Date(string="Date de l'Estimation")
    status_id = fields.Many2one("animal.status", string="Statut")
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
    parent_1_id = fields.Many2one(
        "animal.identification",
        relation="parent_1_rel_animal_identification",
        column1="child_id",
        column2="parent_id",
        string="Affiliation Mère",
    )
    parent_2_id = fields.Many2one(
        "animal.identification",
        relation="parent_2_rel_animal_identification",
        column1="child_id",
        column2="parent_id",
        string="Affiliation Pére",
    )
    child_of_1_ids = fields.One2many(
        "animal.identification", "parent_1_id", string="Parent de"
    )

    owner_ids = fields.Many2many(
        "animal.owner",
        string="Détenteurs",
    )
    fsm_ids = fields.Many2many(
        "fsm.order",
        string="Interventions",
    )
    folio_ids = fields.Many2many("hotel.folio", string="Dossiers")

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
