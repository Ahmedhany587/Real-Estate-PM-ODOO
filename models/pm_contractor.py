from odoo import api, fields, models

class Contractor(models.Model):
    _inherit = 'res.partner'

    contractor_subterm_ids = fields.One2many(comodel_name='pm.contractor.subterm', inverse_name='contractor_id', string="Contractor Sub-Term", ondelete='restrict')
    