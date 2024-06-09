from odoo import api, fields, models


class Contract(models.Model):
    """
    Model that represents a real estate contract with a customer.
    """
    _name = 'pm.contract'
    _description = 'Real Estate Contract with the Customer'

    # Name of the contract
    name = fields.Char()

    # Customer associated with the contract
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string="Customer",  
        required=True,  
        index=True,  
    )

    # Date of the contract
    contract_date = fields.Date(
        string="Contract Date:",  
        required=False,  
        default=lambda self: fields.Date.today()  # Default value is today's date
    )

    # Project associated with the contract
    project_id = fields.Many2one(
        comodel_name='pm.project',
        string="Project",  
        ondelete='restrict',
        domain = "[('contract_id', '=', False)]"  
    )

    # Documents associated with the contract
    doc_ids = fields.One2many(
        'pm.document',  
        'contract_id',  # Field in the pm.document model that references this contract
        string='Documents'  
    )

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

    #: The actual binary content of the document.
    document = fields.Binary(string='Document')

    #: The property that the document belongs to.
    contract_id = fields.Many2one(
        'pm.contract', string='Contract',
        help='The contract that this document is associated with.')