from odoo import models, fields


class ResCompany(models.Model):
    _inherit = "res.company"

    signature = fields.Binary('Signature')
    accreditation = fields.Text('Accreditation')
    approval_authority = fields.Text('Approval Authority')