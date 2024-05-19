from odoo import api, fields, models


class Contract(models.Model):
    _name = 'pm.contract'
    _description = 'Real Estate Contract with the Customer'

    name = fields.Char()

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string="Customer",
        required=True, change_default=True, index=True,
        tracking=1)

    contract_date = fields.Date(string="Contract Date:", required=False, default=lambda self: fields.Date.today())

    project_id = fields.Many2one(comodel_name='pm.project', string="Project", ondelete='restrict')  # Restrict deletion

