from odoo import models, fields, api

class NeededProduct(models.Model):
    _name = 'product.template'
    _inherit = 'product.template'

    needed_qty = fields.Integer(string='Needed Quantity', default=0)
    assigned_qty = fields.Integer(string='Assigned Quantity', default=0)
    