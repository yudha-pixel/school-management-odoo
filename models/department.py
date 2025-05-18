from odoo import fields, models

class Department(models.Model):
    _name = 'department.department'
    _description = 'Department'

    name = fields.Char()