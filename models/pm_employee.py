from odoo import models, fields, api

class Employee(models.Model):
    _name = 'pm.employee'
    _description = 'Real Estate Project Employee'

    name = fields.Char(string='Name', required=True)
    phone = fields.Char(string='Mobile Number')

    working_days = fields.Integer(string='Worked days')
    daily_rate = fields.Integer(string='Daily Rate')

    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date')

    term_ids = fields.Many2many(comodel_name='pm.term', string="Work on", ondelete='restrict')