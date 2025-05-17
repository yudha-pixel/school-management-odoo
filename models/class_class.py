from odoo import models, fields

class SchoolClass(models.Model):
    _name = 'school.class'
    _description = 'Class'

    name = fields.Char(string='Class Name', required=True)
    teacher_id = fields.Many2one('school.teacher', string='Teacher')
    student_ids = fields.One2many('school.student', 'class_id', string='Students')
