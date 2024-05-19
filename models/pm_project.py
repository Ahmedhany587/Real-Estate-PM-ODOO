from odoo import api, fields, models

class Project(models.Model):
    _name = 'pm.project'
    _description = 'Real Estate Project'

    name = fields.Char()

