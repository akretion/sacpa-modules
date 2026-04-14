from odoo import fields, models


class AttachmentSynchronizeTask(models.Model):
    _inherit = "attachment.synchronize.task"

    file_type = fields.Selection(selection_add=[("sacpa_agreement", "Contrats")])
