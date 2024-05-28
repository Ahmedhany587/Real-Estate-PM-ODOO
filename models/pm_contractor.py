from datetime import timedelta
from odoo import _, fields, models, Command,api

class Contractor(models.Model):
    _inherit = 'res.partner'

    contractor_subterm_ids = fields.One2many(
        comodel_name='pm.contractor.subterm', 
        inverse_name='contractor_id', 
        string="Contractor Sub-Term", 
        ondelete='restrict'
    )
    
    ### views ###
    @api.model
    # FIXME: Look into the 2 arg errors when make_bill is called
    def make_bill(self):
        """
        Create an invoice for each sub-term in `contractor_subterm_ids`
        that is in a finished or cancelled state.
        """
        
        # List to store the invoice line IDs
        invoice_line_ids =  []

        # Iterate over each sub-term in `contractor_subterm_ids`
        for subterm in self.contractor_subterm_ids:
            if subterm.state not in ('finished', 'cancelled'):
                continue

            # Create an invoice line for the sub-term
            invoice_line_ids.append(
                Command.create({'product_id': subterm.service_id.id, 'quantity': subterm.progress})
            )

        # Create a new invoice with the invoice line IDs
        new_bill = self.env['account.move'].create({
            'move_type': 'in_invoice',
            'partner_id': self.id,
            'invoice_date': fields.Date.today(),
            'invoice_date_due': fields.Date.today() + timedelta(days=30),
            'invoice_line_ids': invoice_line_ids,
        })

        # Create an action to open the new invoice
        action = {
            'name': _("Vendor Bills"),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'views': [(self.env.ref("account.view_move_form").id, 'form')],
            'target': 'new',
            'context': {'default_move_type': 'in_invoice'},
            'res_id': new_bill.id
        }

        # Return the action to open the invoice
        return action