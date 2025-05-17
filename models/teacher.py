from odoo import models, fields

class SchoolTeacher(models.Model):
    _name = 'school.teacher'
    _description = 'Teacher'

    name = fields.Char(string='Name', required=True)
    subject = fields.Char(string='Subject')
    phone = fields.Char(string='Phone')
    class_ids = fields.One2many('school.class', 'teacher_id', string='Classes')
