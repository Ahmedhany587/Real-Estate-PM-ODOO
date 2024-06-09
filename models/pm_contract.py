from odoo import api, fields, models

class Contract(models.Model):
    """
    Model that represents a real estate contract with a customer.
    """
    _name = 'pm.contract'
    _description = 'Real Estate Contract with the Customer'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Contract Name", tracking=True)
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string="Customer",
        required=True,
        index=True,
        tracking=True
    )
    contract_date = fields.Date(
        string="Contract Date",
        required=False,
        default=lambda self: fields.Date.today(),
        tracking=True
    )
    project_id = fields.Many2one(
        comodel_name='pm.project',
        string="Project",
        ondelete='restrict',
        tracking=True,
        domain = "[('contract_id', '=', False)]"  
    )
    doc_ids = fields.One2many(
        'pm.document',
        'contract_id',  # Field in the pm.document model that references this contract
        string='Documents',
        tracking=True
    )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('signed', 'Signed'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, default='draft', tracking=True)

    @api.model
    def create(self, vals):
        vals['state'] = 'draft'
        return super(Contract, self).create(vals)

    def action_confirm(self):
        self.state = 'confirmed'

    def action_sign(self):
        self.state = 'signed'

    def action_cancel(self):
        self.state = 'cancel'

    def action_set_to_draft(self):
        self.state = 'draft'

    @api.onchange('state')
    def _onchange_state(self):
        if self.state == 'signed':
            for field in self._fields:
                if field != 'doc_ids':
                    self._fields[field].readonly = True
        else:
            for field in self._fields:
                self._fields[field].readonly = False

    @api.onchange('project_id')
    def _onchange_project_id(self):
        """
        Set the contract in the project model.
        """            
        self.project_id.contract_id = self._origin

class Document(models.Model):
    """
    Model that represents a document that is associated with a contract.
    """
    _name = 'pm.document'
    _description = 'PM Document'

    name = fields.Char(string='Name')
    document = fields.Binary(string='Document')
    contract_id = fields.Many2one(
        'pm.contract',
        string='Contract',
        help='The contract that this document is associated with.'
    )
