from dateutil.relativedelta import relativedelta
from odoo import models, fields, api
from datetime import datetime, timedelta


# class TaskDashboardLine(models.TransientModel):
#     name = 'task.dashboard.line'
#     _description = 'Task Dashboard Line'
#
#     dashboard_id = fields.Many2one('task.dashboard', string='Dashboard')
#     assignee_id = fields.Many2one('res.users', string='Assignee')


class TaskDashboard(models.TransientModel):
    _name = 'task.dashboard'
    _description = 'Task Dashboard'

    name = fields.Char('Name', default='Task Dashboard')
    task_count = fields.Integer('Total Tasks', compute='_compute_task_count')
    assignee_id = fields.Many2one('res.users', string='Assignee')
    task_list = fields.One2many('project.task', compute='_compute_task_count', string='Task List')

    date_filter = fields.Selection([
        ('this_week', 'This Week'),
        ('this_month', 'This Month'),
        ('prev_week', 'Previous Week'),
        ('prev_month', 'Previous Month')
    ], string='Date Filter', default='this_week')

    @api.depends('assignee_id', 'date_filter')
    def _compute_task_count(self):
        for record in self:
            domain = self._get_domain(record.assignee_id.id, record.date_filter)
            task_count = self.env['project.task'].search_count(domain)
            task_list = self.env['project.task'].search(domain)
            record.task_count = task_count
            record.task_list = task_list

    def _get_domain(self, assignee_id, date_filter):
        domain = []
        today = fields.Date.today()

        if date_filter == 'this_week':
            start_date = today - timedelta(days=today.weekday())
            end_date = start_date + timedelta(days=6)
            domain += [('create_date', '>=', start_date), ('create_date', '<=', end_date)]
        elif date_filter == 'this_month':
            start_date = today.replace(day=1)
            end_date = start_date + relativedelta(months=1, days=-1)
            domain += [('create_date', '>=', start_date), ('create_date', '<=', end_date)]
        elif date_filter == 'prev_week':
            start_date = today - timedelta(days=today.weekday() + 7)
            end_date = start_date + timedelta(days=6)
            domain += [('create_date', '>=', start_date), ('create_date', '<=', end_date)]
        elif date_filter == 'prev_month':
            start_date = today.replace(day=1) - relativedelta(months=1)
            end_date = start_date + relativedelta(months=1, days=-1)
            domain += [('create_date', '>=', start_date), ('create_date', '<=', end_date)]

        if assignee_id:
            domain += [('user_ids', 'in', [assignee_id])]

        return domain
