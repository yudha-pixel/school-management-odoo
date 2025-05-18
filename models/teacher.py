from odoo import models, fields

class TeacherTeacher(models.Model):
    _name = 'teacher.teacher'
    _description = 'Teacher'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _inherits = {"res.partner": "partner_id"}
    _parent_name = False

    partner_id = fields.Many2one('res.partner', 'Partner',
                                 required=True, ondelete="cascade")
    first_name = fields.Char('First Name', translate=True, required=True)
    middle_name = fields.Char('Middle Name', size=128)
    last_name = fields.Char('Last Name', size=128, required=True)
    birth_date = fields.Date('Birth Date', required=True)
    blood_group = fields.Selection([
        ('A+', 'A+ve'),
        ('B+', 'B+ve'),
        ('O+', 'O+ve'),
        ('AB+', 'AB+ve'),
        ('A-', 'A-ve'),
        ('B-', 'B-ve'),
        ('O-', 'O-ve'),
        ('AB-', 'AB-ve')
    ], string='Blood Group')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], 'Gender', required=True)
    nationality = fields.Many2one('res.country', 'Nationality')
    emergency_contact = fields.Many2one('res.partner', 'Emergency Contact')
    visa_info = fields.Char('Visa Info', size=64)
    id_number = fields.Char('ID Card Number', size=64)
    login = fields.Char('Login', related='partner_id.user_id.login', readonly=True)
    last_login = fields.Datetime('Latest Connection', readonly=True, related='partner_id.user_id.login_date')
    subject_ids = fields.Many2many('subject.subject', string='Subject(s)', tracking=True)
    emp_id = fields.Many2one('hr.employee', 'HR Employee')
    main_department_id = fields.Many2one('department.department', 'Main Department',
        default=lambda self: self.env.user.dept_id and self.env.user.dept_id.id or False)
    allowed_department_ids = fields.Many2many('department.department', string='Allowed Department',
        default=lambda self: self.env.user.department_ids and self.env.user.department_ids.ids or False)
    active = fields.Boolean(default=True)
