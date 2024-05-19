from odoo import api, fields, models


class Project(models.Model):
    _name = 'pm.project'
    _description = 'Real Estate Project'

    name = fields.Char()

    contract_id = fields.Many2one(comodel_name='pm.contract', string="Contract", readonly=False)
    customer = fields.Many2one(comodel_name='res.partner', string="Customer", related='contract_id.partner_id',
                               readonly=True)

