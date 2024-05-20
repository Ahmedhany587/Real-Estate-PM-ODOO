from odoo import models, fields

class Term(models.Model):
    _name = 'pm.term'
    _description = 'Real Estate Project Term'

    name = fields.Char(string='Name', required=True)
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)

    project_id = fields.Many2one(comodel_name='pm.project', string="Project", ondelete='cascade')
    contractor_id = fields.Many2one(comodel_name='res.partner', string="Contractor", ondelete='restrict')
    employee_ids = fields.Many2many(comodel_name='res.users', string="Employees", ondelete='restrict')