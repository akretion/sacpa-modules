# Copyright (C) 2025 - TODAY, Akretion
# @author Mourad EL HADJ MIMOUNE <mourad.elhadj.mimoune@akretion.com>

from odoo import api, fields, models


class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    fsm_order_date = fields.Date(
        string="Date de l'intervention", compute="_compute_date_intervention"
    )
    fsm_vhl = fields.Many2one(string="Vehicule", related="fsm_order_ids.vehicle_id")

    call_date = fields.Date(string="Date de l'appel")
    call_time = fields.Float(string="Heure de l'appel")
    canal_request = fields.Char(string="Canal de la demande")

    partner_order_type = fields.Selection(
        [
            ("police", "Police"),
        ],
        string="Type de donneur ordre",
    )
    partner_order_id = fields.Many2one(
        "res.partner", string="Contact du donneur d'ordre"
    )

    agency_id = fields.Many2one("res.partner", string="Agence")
    requester_id = fields.Many2one("helpdesk.requester", string="Donneur d'ordre")
    requester_name = fields.Char(string="Nom du donneur d'ordre")
    requester_phone = fields.Char(string="Téléphone du donneur d'ordre")

    nature_id = fields.Many2one(
        "helpdesk.intervention.type", string="Nature de l'intervention"
    )

    animal_ids = fields.Many2many("animal.identification", string="Animaux")

    location_address = fields.Char(related="fsm_location_id.street", string="Adresse")
    location_address2 = fields.Char(
        related="fsm_location_id.street2", string="Adresse2"
    )
    location_zip = fields.Char(related="fsm_location_id.zip", string="Code Postal")
    location_city = fields.Char(related="fsm_location_id.city", string="Ville")
    location_country = fields.Many2one(
        related="fsm_location_id.country_id", string="Pays"
    )
    location_latitude = fields.Float(
        related="fsm_location_id.partner_latitude", string="Latitude"
    )
    location_longitude = fields.Float(
        related="fsm_location_id.partner_longitude", string="Longitude"
    )
    url_google_location = fields.Char(
        string="Lien_google", compute="_compute_google_map_url"
    )
    contact_on_place = fields.Char(string="Contact sur place")
    contact_phone = fields.Char(string="Téléphone de contact")
    fax = fields.Char()
    blood = fields.Boolean(string="Présence de sang?")
    infos_location = fields.Text(string="Informations sur la localisation")

    animal_count = fields.Integer(string="Nombre d'animaux concernés")
    animal_status_id = fields.Many2one("animal.status", string="Statut de l'animal")

    notes = fields.Text(string="Commentaires")

    @api.depends("location_latitude", "location_longitude")
    def _compute_google_map_url(self):
        for record in self:
            record.url_google_location = (
                "http://google.map:"
                + str(record.location_longitude)
                + ","
                + str(record.location_latitude)
                + "z"
            )

    def geo_localize(self):
        return self.fsm_location_id.geo_localize()

    def action_open_google_map(self):
        if not self.url_google_location:
            return
        else:
            return {
                "type": "ir.action.act_url",
                "url": self.url_google_location,
                "target": "new",
            }

    @api.depends("create_date")
    def _compute_date_intervention(self):
        for record in self:
            if record.fsm_order_ids:
                record.fsm_order_date = record.fsm_order_ids[0].create_date
            else:
                record.fsm_order_date = record.create_date
