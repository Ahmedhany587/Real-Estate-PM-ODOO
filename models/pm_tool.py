from odoo import _, models, fields, api


class Tool(models.Model):
    """
    Model to represent the tools used in the real estate project.
    """

    _name = 'pm.tool'
    _description = 'Real Estate Project Tools'

    name = fields.Char(string='Name', required=True)
    seq = fields.Char(
        'Reference',  default=lambda self: _('New'),
        copy=False, readonly=True, required=True)
    
    working_days = fields.Integer(string='Worked days')
    daily_rate = fields.Integer(string='Daily Rate')
    cost = fields.Integer(string='Tool cost on company', compute='_compute_cost')

    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date')

    # List of terms the tool is used on
    term_ids = fields.Many2many(comodel_name='pm.term', string="Work on", ondelete='restrict')

    #### Compute ####

    @api.depends('working_days', 'daily_rate')
    def _compute_cost(self):
        """
        Computes the total cost of the tool.
        """
        for rec in self:
            rec.cost = rec.working_days * rec.daily_rate

    @api.model
    def create(self, vals):
        """
        Create a new tool and set the reference.
        """
        new = super().create(vals)
        new.seq = self.env['ir.sequence'].next_by_code('pm.tool') or _('New')
        
        return new
