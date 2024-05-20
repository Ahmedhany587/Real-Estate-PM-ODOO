from odoo import models, fields, api

class SubTerm(models.Model):
    _name = 'pm.subterm'
    _description = 'Real Estate Project Sub Term'

    name = fields.Char(string='Name', required=True)
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)
    
    term_id = fields.Many2one(comodel_name='pm.term', string="Term", ondelete='restrict')

    product_ids = fields.Many2many(comodel_name='product.template', string="Products", ondelete='restrict')

    cost  = fields.Integer(string='Cost', default=0, compute='_compute_cost')

    @api.depends('product_ids')
    def _compute_cost(self):
        for rec in self:
            rec.cost = sum(rec.product_ids.mapped('standard_price'))
