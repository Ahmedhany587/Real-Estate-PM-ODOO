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

    contractor_subterm_ids = fields.One2many(comodel_name='pm.contractor.subterm', inverse_name='sub_term_id', 
                                             string="Contractor Sub-Term", ondelete='restrict')

    #### Compute ####
    @api.depends('product_ids')
    def _compute_cost(self):
        for rec in self:
            prices = rec.product_ids.mapped('standard_price')
            qties = rec.product_ids.mapped('needed_qty')
            rec.cost = sum(qties[i] * prices[i] for i in range(len(prices)))

    #### Constraints ####
    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for rec in self:
            if not rec.term_id:
                raise models.ValidationError('Sub-Term must be within a Term')
            
            if rec.end_date < rec.start_date:
                raise models.ValidationError('End Date must be greater than Start Date')
            
            if rec.start_date < rec.term_id.start_date or rec.end_date > rec.term_id.end_date:
                raise models.ValidationError('Start Date and End Date must be within the Term')
            
        return True
    
class ContractorSubTerm(models.Model):
    _name = 'pm.contractor.subterm'
    _description = 'Contractor Sub Term'

    name = fields.Char(string='Name', compute = "_compute_name")

    sub_term_id = fields.Many2one(comodel_name='pm.subterm', string="Sub-Term", ondelete='restrict')
    contractor_id = fields.Many2one(comodel_name='res.partner', string="Contractor", ondelete='restrict')
    qty = fields.Integer(string="Quantity")


    #### Compute ####
    @api.depends('sub_term_id','contractor_id')
    def _compute_name(self):
        for rec in self:
            rec.name = f'{rec.sub_term_id.name} - {rec.contractor_id.name}'