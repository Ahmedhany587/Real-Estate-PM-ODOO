from odoo import api, fields, models


class Project(models.Model):
    _name = 'pm.project'
    _description = 'Real Estate Project'

    name = fields.Char()

    contract_id = fields.Many2one(comodel_name='pm.contract', string="Contract", readonly=False)
    customer = fields.Many2one(comodel_name='res.partner', string="Customer", related='contract_id.partner_id',
                               readonly=True)
    
    term_ids = fields.One2many(comodel_name='pm.term', inverse_name='project_id', string="Terms", readonly=False)
    total_cost = fields.Integer(compute='_compute_total_cost', string='Total Cost', store=True)

    @api.depends('term_ids')
    def _compute_total_cost(self):
        for rec in self:
            rec.total_cost = sum(rec.term_ids.mapped('total_cost'))

    def show_pr_form(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'pm.purchase.request',
            'view_mode': 'form',
            'target': 'new',
        }
