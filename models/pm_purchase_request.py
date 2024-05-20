from odoo import models, fields, api

class PurchaseRequest(models.Model):
    _name = 'pm.purchase.request'

    name = fields.Char(string='Name', required=True)
    term_id = fields.Many2one(comodel_name='pm.term', string="Selected Term")
    
    purchase_request_line_ids = fields.Many2many(comodel_name='pm.purchase.request.line', 
                                                compute = '_compute_purchase_request_line_ids',
                                                string="Products", ondelete='restrict',store=True, readonly=False)


    @api.depends('term_id')
    def _compute_purchase_request_line_ids(self):
        for rec in self:
            pros = rec.term_id.sub_term_ids.mapped('product_ids')
            pros = pros.filtered(lambda p: p.detailed_type == 'product')
            for pro in pros:
                line = self.env['pm.purchase.request.line'].create({
                    'purchase_request_id': rec.id,
                    'product_id': pro.id,
                    'quantity': 0
                })
                rec.purchase_request_line_ids |= line
            


class PurchaseRequestLine(models.Model):
    _name = 'pm.purchase.request.line'

    purchase_request_id = fields.Many2one(comodel_name='pm.purchase.request', string="Purchase Request", ondelete='restrict')
    
    product_id = fields.Many2one(comodel_name='product.product', string="Product", required=True)
    quantity = fields.Integer(string='Quantity', required=True)