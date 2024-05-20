from odoo import models, fields, api

class PurchaseRequest(models.Model):
    _name = 'pm.purchase.request'

    name = fields.Char(string='Name', required=True)
    term_id = fields.Many2one(comodel_name='pm.term', string="Selected Term")

    vendor_id = fields.Many2one(comodel_name='res.partner', string="Vendor", ondelete='restrict')
    
    purchase_request_line_ids = fields.Many2many(comodel_name='pm.purchase.request.line', 
                                                compute = '_compute_purchase_request_line_ids',
                                                string="Products", ondelete='restrict',store=True, readonly=False)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('confirm', 'Confirm'),
        ('cancel', 'Cancel'),
    ], default='draft', string='State')

    def action_draft(self):
        self.state = 'draft'

    def action_sent(self):
        self.state = 'sent'

    def action_confirm(self):
        self.state = 'confirm'
        order = self.env['purchase.order'].create({
            'partner_id': self.vendor_id.id,
            'name': self.name,
        })


        for line in self.purchase_request_line_ids:
            curr = self.env['purchase.order.line'].create({
                'name': line.product_id.name,
                'product_id': line.product_id.id,
                'product_qty': line.quantity,
                'order_id': order.id
            })
            order.order_line |= curr
            

    def action_cancel(self):
        self.state = 'cancel'

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