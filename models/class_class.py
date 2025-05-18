from odoo import models, fields

class SchoolClass(models.Model):
    _name = 'class.class'
    _description = 'School Class'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Class Name', required=True)
    code = fields.Char('Code', required=True)
    academic_year_id = fields.Many2one( 'academic.year', string='Academic Year', required=True)
    homeroom_teacher_id = fields.Many2one('teacher.teacher', string='Homeroom Teacher')
    student_ids = fields.One2many('student.student', 'class_id', string='Students')
    note = fields.Text('Note')
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('unique_class_code', 'unique(code)', 'Class Code must be unique!')
    ]