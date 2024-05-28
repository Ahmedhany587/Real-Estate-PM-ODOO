from odoo import models, fields, api

class NeededProduct(models.Model):
    """
    Inherit product.template model to add needed_qty and assigned_qty fields.
    """
    _name = 'product.template'
    _inherit = 'product.template'

    needed_qty = fields.Integer(
        string='Needed Quantity', default=0, 
        help="The quantity of this product that is needed.")
    assigned_qty = fields.Integer(
        string='Assigned Quantity', default=0, 
        help="The quantity of this product that has been assigned to a contractor.")
    