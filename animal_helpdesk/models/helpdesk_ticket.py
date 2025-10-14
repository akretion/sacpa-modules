# Copyright (C) 2025 - TODAY, Akretion
# @author Mourad EL HADJ MIMOUNE <mourad.elhadj.mimoune@akretion.com>

from odoo import fields, models


class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"


    call_date = fields.Date(string="Date de l'appel")
    call_time = fields.Float(string="Heure de l'appel")

    agency_id = fields.Many2one("res.partner", string="Agence")
    requester_id = fields.Many2one("helpdesk.requester", string="Donneur d'ordre")
    requester_name = fields.Char(string="Nom du donneur d'ordre")
    requester_phone = fields.Char(string="Téléphone du donneur d'ordre")

    nature_id = fields.Many2one("helpdesk.intervention.type", string="Nature de l'intervention")

    address = fields.Char(string="Adresse")
    zip = fields.Char(string="Code Postal")
    city = fields.Char(string="Ville")
    contact_phone = fields.Char(string="Téléphone de contact")
    fax = fields.Char(string="Fax")

    species_id = fields.Many2one("animal.species", string="Espèce")
    breed_id = fields.Many2one("animal.breed", string="Race")
    is_crossbreed = fields.Boolean(string="Croisé ?")
    crossbreed_breed_id = fields.Many2one("animal.breed", string="Race de croisement")

    animal_count = fields.Integer(string="Nombre d'animaux concernés")
    animal_status_id = fields.Many2one("animal.status", string="Statut de l'animal")

    notes = fields.Text(string="Commentaires")