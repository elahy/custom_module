from odoo import models, fields, api


class ProjectProject(models.Model):
    _inherit = 'project.project'

    team_id = fields.Many2one('project.team', string='Project Team')

