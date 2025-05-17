from odoo import models, fields

class SchoolStudent(models.Model):
    _name = 'school.student'
    _description = 'Student'

    name = fields.Char(string='Name', required=True)
    birth_date = fields.Date(string='Birth Date')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender')
    class_id = fields.Many2one('school.class', string='Class')
