from odoo import api, fields, models


class Project(models.Model):
    """
    Model representing a real estate project.
    """
    _name = 'pm.project'
    _description = 'Real Estate Project'

    name = fields.Char(string='Name')  # Name of the project

    contract_id = fields.Many2one(
        comodel_name='pm.contract', string="Contract", readonly=False
    )  # Contract associated with the project

    customer = fields.Many2one(
        comodel_name='res.partner', string="Customer", related='contract_id.partner_id',
        readonly=True
    )  # Customer associated with the contract

    term_ids = fields.One2many(
        comodel_name='pm.term', inverse_name='project_id', string="Terms", readonly=False
    )  # Terms associated with the project

    total_cost = fields.Integer(
        compute='_compute_total_cost', string='Total Cost', store=True
    )  # Total cost of the project

    @api.depends('term_ids')
    def _compute_total_cost(self):
        """
        Compute the total cost of the project.
        """
        for rec in self:
            rec.total_cost = sum(rec.term_ids.mapped('total_cost'))

