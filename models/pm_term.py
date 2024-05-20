from odoo import models, fields, api

class Term(models.Model):
    _name = 'pm.term'
    _description = 'Real Estate Project Term'

    name = fields.Char(string='Name', required=True)
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)

    project_id = fields.Many2one(comodel_name='pm.project', string="Project", ondelete='cascade')
    contractor_id = fields.Many2one(comodel_name='res.partner', string="Contractor", ondelete='restrict')
    employee_ids = fields.Many2many(comodel_name='pm.employee', string="Employees", ondelete='restrict')

    sub_term_ids = fields.One2many(comodel_name='pm.subterm', inverse_name='term_id', string="Sub-Term", ondelete='restrict')
    total_cost = fields.Integer(string="Total Cost", compute='_compute_total_cost')

    @api.depends('sub_term_ids')
    def _compute_total_cost(self):
        for rec in self:
            rec.total_cost = sum(rec.sub_term_ids.mapped('cost'))