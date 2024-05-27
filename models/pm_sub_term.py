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
    product_ids = fields.Many2many(related='sub_term_id.product_ids', string="Products", ondelete='restrict')

    service_id = fields.Many2one(comodel_name='product.template', string="Service", 
                                 domain="[('id', 'in', product_ids), ('detailed_type', '=', 'service')]",
                                 ondelete='restrict')
    contractor_id = fields.Many2one(comodel_name='res.partner', string="Contractor", ondelete='restrict')
    qty = fields.Integer(string="Quantity", default=0)

    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)
    progress = fields.Integer(string='Progress', default=0)

    state = fields.Selection(string='State', selection=[
        ('assigned', 'Assigned'), 
        ('started', 'Started'),
        ('finished', 'Finished'),
        ('cancelled', 'Cancelled'),
        ], 
        default='assigned')

    qty_in = fields.Integer(string='Quantity In', default=0)

    #### Actions ####
    def action_cancel(self):
        self.state = 'cancelled'
        to_make = self.qty - self.progress
        self.service_id.assigned_qty -= to_make

    def action_start(self):
        self.state = 'started'

    def action_finish(self):
        self.state = 'finished'

    def add_qty_in(self):
        try:
            if self.state != 'started':
                
                raise models.ValidationError('Contractor Sub-Term must be started')

            to_make = self.qty - self.progress
            if self.qty_in > to_make:
                
                raise models.ValidationError(f'Quantity In must be at most {to_make}')
            
            self.progress += self.qty_in
            
            if self.progress == self.qty:
                self.action_finish()
        finally:
            self.qty_in = 0

    #### Compute ####
    @api.depends('sub_term_id','contractor_id')
    def _compute_name(self):
        for rec in self:
            rec.name = f'{rec.sub_term_id.name} - {rec.contractor_id.name}'

    #### Constraints ####
    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for rec in self:
            if rec.end_date < rec.start_date:
                raise models.ValidationError('End Date must be greater than Start Date')
            
            if rec.start_date < rec.sub_term_id.start_date or rec.end_date > rec.sub_term_id.end_date:
                raise models.ValidationError('Start Date and End Date must be within the Sub-Term')
            
        return True
    
    @api.constrains('progress')
    def _check_progress(self):
        for rec in self:
            if rec.progress < 0 or rec.progress > rec.qty:
                raise models.ValidationError(f'Progress must be between 0 and {rec.qty}')
            
        return True

    #### Onchange ####
    @api.onchange('qty')
    def _onchange_qty(self):
        if self.qty < 0:
                raise models.ValidationError('Quantity must be greater than 0')
            
        old_qty = self._origin.qty
        self.service_id.assigned_qty -= old_qty

        free_qty = self.service_id.needed_qty - self.service_id.assigned_qty
        if self.qty > free_qty:
            raise models.ValidationError(f'Quantity must be at most {free_qty}')

        self.service_id.assigned_qty += self.qty