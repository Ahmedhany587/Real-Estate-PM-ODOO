from odoo import models, fields, api
from odoo.exceptions import ValidationError

class NeededProduct(models.Model):
    """
    Inherit product.template model to add needed_qty and assigned_qty fields.
    """
    _inherit = 'product.template'

    needed_qty = fields.Integer(
        string='Needed Quantity', default=0,
        help="The quantity of this product that is needed.")
    assigned_qty = fields.Integer(
        string='Assigned Quantity', default=0,
        help="The quantity of this product that has been assigned to a contractor.")

    @api.constrains('assigned_qty', 'needed_qty')
    def _check_assigned_qty(self):
        for record in self:
            if record.assigned_qty > record.needed_qty:
                raise ValidationError("Assigned quantity cannot exceed needed quantity.")
