from odoo import models, fields, api

class Term(models.Model):
    """
    This model represents a real estate project term.
    """
    _name = 'pm.term'
    _description = 'Real Estate Project Term'

    name = fields.Char(string='Name', required=True)
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)

    #: Project to which the term belongs.
    project_id = fields.Many2one(comodel_name='pm.project', string="Project", ondelete='cascade')
    #: Contractor who is performing the term.
    contractor_id = fields.Many2one(comodel_name='res.partner', string="Contractor", ondelete='restrict')
    #: Employees working on the term.
    employee_ids = fields.Many2many(comodel_name='pm.employee', string="Employees", ondelete='restrict')
    #: Tools used in the term.
    tool_ids = fields.Many2many(comodel_name='pm.tool', string="Tools", ondelete='restrict')

    #: Sub-terms that make up the term.
    sub_term_ids = fields.One2many(comodel_name='pm.subterm', inverse_name='term_id', string="Sub-Term", ondelete='restrict')
    total_cost = fields.Integer(string="Total Cost", compute='_compute_total_cost')

    @api.depends('sub_term_ids')
    def _compute_total_cost(self):
        """
        Compute the total cost of all sub-terms.
        """
        for rec in self:
            rec.total_cost = sum(rec.sub_term_ids.mapped('cost'))

    def show_wizard(self):
        """
        Open the purchase request wizard for the current term.
        """
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'pm.purchase.request',
            'view_id': self.env.ref('pm_real_estate.view_pm_purchase_request_wiz_form').id,
            'view_mode': 'form',
            'target': 'new',
            'context' : {
                'term_id' : self.id
            }
        }
