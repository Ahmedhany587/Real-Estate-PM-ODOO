from odoo import models, fields, api

class SubTerm(models.Model):
    """
    Model representing a sub-term of a real estate project term.
    """
    _name = 'pm.subterm'
    _description = 'Real Estate Project Sub Term'

    # Fields
    name = fields.Char(string='Name', required=True)  
    start_date = fields.Date(string='Start Date', required=True)  
    end_date = fields.Date(string='End Date', required=True)
    
    term_id = fields.Many2one(comodel_name='pm.term', string="Term", ondelete='restrict')  # Reference to the parent term

    product_ids = fields.Many2many(comodel_name='product.template', string="Products", ondelete='restrict')  # List of products used in the sub-term

    cost  = fields.Integer(string='Cost', default=0, compute='_compute_cost')  # Total cost of the sub-term

    contractor_subterm_ids = fields.One2many(comodel_name='pm.contractor.subterm', inverse_name='sub_term_id', 
                                             string="Contractor Sub-Term", ondelete='restrict')  # List of contractor sub-terms

    #### Compute ####
    @api.depends('product_ids')
    def _compute_cost(self):
        """
        Calculate the total cost of the sub-term.
        """
        for rec in self:
            prices = rec.product_ids.mapped('standard_price')  # List of prices of the products
            qties = rec.product_ids.mapped('needed_qty')  # List of quantities of the products
            rec.cost = sum(qties[i] * prices[i] for i in range(len(prices)))  # Calculate the total cost

    #### Constraints ####
    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        """
        Check if the start and end dates of the sub-term are valid.
        """
        for rec in self:
            if not rec.term_id:
                raise models.ValidationError('Sub-Term must be within a Term')
            
            if rec.end_date < rec.start_date:
                raise models.ValidationError('End Date must be greater than Start Date')
            
            if rec.start_date < rec.term_id.start_date or rec.end_date > rec.term_id.end_date:
                raise models.ValidationError('Start Date and End Date must be within the Term')
            
        return True
    
class PmContractorSubTerm(models.Model):
    _name = 'pm.contractor.subterm'
    _description = 'Contractor Sub Term'

    # Name of the contractor sub-term composed of the sub-term name and the contractor name
    name = fields.Char(string='Name', compute = "_compute_name")

    # Reference to the parent sub-term
    sub_term_id = fields.Many2one(comodel_name='pm.subterm', string="Sub-Term", ondelete='restrict')

    # List of products used in the contractor sub-term
    product_ids = fields.Many2many(related='sub_term_id.product_ids', string="Products", ondelete='restrict')

    # Reference to the service product (service type)
    service_id = fields.Many2one(comodel_name='product.template', string="Service", 
                                 domain="[('id', 'in', product_ids), ('detailed_type', '=', 'service')]",
                                 ondelete='restrict')
    # Reference to the contractor partner
    contractor_id = fields.Many2one(comodel_name='res.partner', string="Contractor", ondelete='restrict')

    # Quantity of the service product assigned to the contractor sub-term
    qty = fields.Integer(string="Quantity", default=0)

    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)

    # Progress of the contractor sub-term
    progress = fields.Integer(string='Progress', default=0)

    # State of the contractor sub-term
    state = fields.Selection(string='State', selection=[
        ('assigned', 'Assigned'), 
        ('started', 'Started'),
        ('finished', 'Finished'),
        ('cancelled', 'Cancelled'),
        ], 
        default='assigned')

    # Quantity of products to br added to the progress by the contractor
    qty_in = fields.Integer(string='Quantity In', default=0)

   #### Actions ####
    def action_cancel(self):
        """
        Cancels the current contractor sub-term by updating its state to 'cancelled'. 
        It also adjusts the assigned quantity of the service by subtracting the remaining quantity to be made.
        """
        self.state = 'cancelled'
        to_make = self.qty - self.progress
        self.service_id.assigned_qty -= to_make

    def action_start(self):
        self.state = 'started'

    def action_finish(self):
        self.state = 'finished'

    def add_qty_in(self):
        """
        Adds the quantity in to the progress of the contractor sub-term.

        Raises:
            models.ValidationError: If the contractor sub-term is not started or if the quantity in is greater than the remaining quantity.
        """
        try:
            if self.state != 'started':
                raise models.ValidationError('Contractor SubTerm must be started')

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
        """
        Compute the name of the contractor sub-term.
        """
        for rec in self:
            rec.name = f'{rec.sub_term_id.name} - {rec.contractor_id.name}'

    #### Constraints ####
    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        """
        Check if the start and end dates of the contractor sub-term are valid.
        """
        for rec in self:
            if rec.end_date < rec.start_date:
                raise models.ValidationError('End Date must be greater than Start Date')
            
            if rec.start_date < rec.sub_term_id.start_date or rec.end_date > rec.sub_term_id.end_date:
                raise models.ValidationError('Start Date and End Date must be within the Sub-Term')
            
        return True
    
    @api.constrains('progress')
    def _check_progress(self):
        """
        Check if the progress of the contractor sub-term is valid.
        """
        for rec in self:
            if rec.progress < 0 or rec.progress > rec.qty:
                raise models.ValidationError(f'Progress must be between 0 and {rec.qty}')
            
        return True

    #### Onchange ####
    @api.onchange('qty')
    def _onchange_qty(self):
        """
        Event handler for the onchange event of the quantity field.
        """
        # Check if the quantity is valid.
        if self.qty < 0:
            raise models.ValidationError('Quantity must be greater than 0')
            
        # Calculate the old quantity.
        old_qty = self._origin.qty
        
        # Reduce the quantity of the service.
        self.service_id.assigned_qty -= old_qty
        
        # Calculate the remaining free quantity for the service.
        free_qty = self.service_id.needed_qty - self.service_id.assigned_qty
        
        # Check if the new quantity is within the free quantity.
        if self.qty > free_qty:
            raise models.ValidationError(f'Quantity must be at most {free_qty}')
        
        # Add the new quantity to the service.
        self.service_id.assigned_qty += self.qty

