from odoo import fields, models


class PetDeclaration(models.Model):
    _name = "pet.declaration"
    _description = "Vigipet"

    raw_time = fields.Char(string="Timestamp")
    # TODO compute date possible
    date = fields.Date()
    entry_time = fields.Char(string="Date d'entrée")
    entry_date = fields.Date()
    entry = fields.Char(string="Entry ID")
    declaration_ref = fields.Char(string="ID Déclaration")
    domain = fields.Selection([("lost", "Perdu"), ("found", "Trouvé")], required=True)
    specie = fields.Selection(
        selection=[
            ("chat", "Chat"),
            ("chien", "Chien"),
            ("volatile", "Volatile"),
            ("nac", "NAC"),
            ("autre", "Autre"),
        ],
        string="Espèce",
    )
    sex = fields.Selection(
        selection=[("mâle", "Mâle"), ("femelle", "Femelle")], string="Sexe"
    )
    sterilized = fields.Boolean("Stérilisée")
    identified = fields.Boolean("Identifié")
    identifiant = fields.Char()
    breed = fields.Char("Race")
    crossbred = fields.Boolean("Croisé")
    color = fields.Char("Couleur")
    pet_name = fields.Char("Nom animal")
    age = fields.Char()
    age_unit = fields.Char("Age Unite")
    url = fields.Char("PJ")
    comment = fields.Char("Signes distinctifs")
    address_area = fields.Char("Adresse lieu de perte")
    city_area = fields.Char("Ville lieu de perte")
    zip_area = fields.Char("Code postal lieu de perte")
    last_name = fields.Char("Nom Declarant")
    first_name = fields.Char("Prénom Declarant")
    address = fields.Char("Adresse Declarant")
    zip = fields.Char("Code postal Declarant")
    city = fields.Char("Ville Declarant")
    phone = fields.Char("Tel Declarant")
    email = fields.Char("Email Declarant")
    consent1 = fields.Char("Consentement CGS 1")
    consent2 = fields.Char("Consentement CGS 2")
    ip = fields.Char("IP")
    infosupp1 = fields.Char("InfoSupp1")
    infosupp2 = fields.Char("InfoSupp2")
