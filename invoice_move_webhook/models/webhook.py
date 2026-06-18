# Akretion Copyright (c) 2025 Author. All Rights Reserved.
#

from odoo import api, fields, models


class WebhookMove(models.Model):
    _name = "webhook.move"

    name = fields.Char(
        string="Nome du lier webhook", compute="_compute_name", store=True
    )

    code_entite = fields.Char(string="code entité")
    entite = fields.Char(string="Nom de l'entité")
    code_site = fields.Char(string="code site")
    nom_fournisseur = fields.Char(string="nom_fournisseur")
    code_fournisseur = fields.Char(string="Code fournisseur")
    dwdocid = fields.Char(string="code document")
    dwsys_doc_url = fields.Char(string="Lien url")
    date_du_document = fields.Char(string="Date du document")
    mois_du_document = fields.Char(string="Mois du document")
    annee_du_document = fields.Char(string="Année du document")
    reference_interne_de_la_da = fields.Char(string="Ref interne")
    reference_de_la_commande = fields.Char(string="Ref de la commande")
    mt_tva = fields.Char(string="montant TVA")
    mt_ht = fields.Char(string="Montant HT")
    mt_ttc = fields.Char(string="Montant TTC")
    type_de_tva = fields.Char(string="Type de TVA")
    devise = fields.Char(string="devise")
    adresse_de_livraison = fields.Char(string="adresse de livraison")
    commentaires = fields.Text(string="commentaires")

    account_move_id = fields.One2many("account.move", "webhook_id", "Facture lié")
    partner_id = fields.Many2one(
        "res.partner", string="Fournisseur", compute="_compute_fournisseur", store=True
    )

    @api.depends("nom_fournisseur", "code_fournisseur")
    def _compute_fournisseur(self):
        for record in self:
            partner_id = record.env["res.partner"].search(
                [
                    ("name", "ilike", record.nom_fournisseur),
                    ("ref", "=", record.code_fournisseur),
                ]
            )
            record.partner_id = partner_id.id

    @api.depends("reference_de_la_commande")
    def _compute_name(self):
        for record in self:
            record.name = "WBHK//" + record.reference_de_la_commande
