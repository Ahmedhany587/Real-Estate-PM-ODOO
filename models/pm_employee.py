from odoo import _, models, fields, api

class Employee(models.Model):
    _name = 'pm.employee'
    _description = 'Real Estate Project Employee'

    name = fields.Char(string='Name', required=True)
    seq = fields.Char(
        'Reference',  default=lambda self: _('New'),
        copy=False, readonly=True, required=True)
    
    phone = fields.Char(string='Mobile Number')

    working_days = fields.Integer(string='Worked days')
    daily_rate = fields.Integer(string='Daily Rate')

    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date')

    term_ids = fields.Many2many(comodel_name='pm.term', string="Work on", ondelete='restrict')

    @api.model
    def create(self, vals):
        new = super().create(vals)
        new.seq = self.env['ir.sequence'].next_by_code('pm.employee') or _('New')
        
        return new