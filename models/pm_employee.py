from odoo import _, models, fields, api



class Employee(models.Model):
    """
    Real Estate Project Employee
    """
    _name = 'pm.employee'
    _description = 'Real Estate Project Employee'

    name = fields.Char(string='Name', required=True)
    seq = fields.Char(
        'Reference',  default=lambda self: _('New'),
        copy=False, readonly=True, required=True)

    # Employee Mobile Number
    phone = fields.Char(string='Mobile Number')

    working_days = fields.Integer(string='Worked day')
    daily_rate = fields.Integer(string='Daily Rate')

    # Total cost of the employee
    cost = fields.Integer(string='Emp cost on company', compute='_compute_cost')

    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date')

    # List of terms the employee is working on
    term_ids = fields.Many2many(comodel_name='pm.term', string="Work on", ondelete='restrict')

    ######################################################################
    # Computed Fields
    @api.depends('working_days', 'daily_rate')
    def _compute_cost(self):
        """
        Computes the total cost of the employee
        """
        for rec in self:
            rec.cost = rec.working_days * rec.daily_rate

    ######################################################################
    # Override Methods
    @api.model
    def create(self, vals):
        """
        Create a new employee and set the reference
        """
        new = super().create(vals)
        new.seq = self.env['ir.sequence'].next_by_code('pm.employee') or _('New')
        
        return new
