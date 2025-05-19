from odoo import models, fields, api
from odoo.exceptions import ValidationError

class SchoolStudent(models.Model):
    _name = 'student.student'
    _description = "Student"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _inherits = {"res.partner": "partner_id"}

    first_name = fields.Char('First Name',  translate=True)
    middle_name = fields.Char('Middle Name', translate=True)
    last_name = fields.Char('Last Name', translate=True)
    birth_date = fields.Date('Birth Date')
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
        ('m', 'Male'),
        ('f', 'Female'),
        ('o', 'Other')
    ], 'Gender', required=True, default='m')
    nationality = fields.Many2one('res.country', 'Nationality')
    emergency_contact_id = fields.Many2one('res.partner', 'Emergency Contact')
    visa_info = fields.Char('Visa Info', size=64)
    id_number = fields.Char('ID Card Number', size=64)
    partner_id = fields.Many2one('res.partner', 'Partner', required=True, ondelete="cascade")
    user_id = fields.Many2one('res.users', 'User', ondelete="cascade")
    gr_no = fields.Char("Registration Number", size=20)
    category_id = fields.Many2one('category.category', 'Category',
                                  default=lambda self: self.env.ref('erpquick_school_management.category_regular').id)
    course_detail_ids = fields.One2many('student.course', 'student_id', 'Course Details', tracking=True)
    class_id = fields.Many2one('class.class', string='Class')
    active = fields.Boolean(default=True)

    _sql_constraints = [(
        'unique_gr_no',
        'unique(gr_no)',
        'Registration Number must be unique per student!'
    )]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            # Auto-generate student registration number
            if not vals.get('gr_no'):
                vals['gr_no'] = self.env['ir.sequence'].next_by_code('student.student') or 'NEW_STUDENT'

            # Ensure partner name is passed for _inherits (res.partner)
            if not vals.get('name'):
                fname = vals.get('first_name', '')
                mname = vals.get('middle_name', '')
                lname = vals.get('last_name', '')
                full_name = f"{fname} {mname} {lname}".strip()
                vals['name'] = full_name or 'Unnamed Student'
        return super().create(vals_list)

    @api.onchange('first_name', 'middle_name', 'last_name')
    def _onchange_name(self):
        for student in self:
            student.name = f"{student.first_name or ''} {student.middle_name or ''} {student.last_name or ''}".strip()

    def action_create_user(self):
        self.ensure_one()
        if self.user_id:
            raise ValidationError("User is already created")

        if not self.email:
            raise ValidationError("Please set an email address before creating a user.")

        if not self.user_id:
            user = self.env['res.users'].create([{
                'name': f"{self.first_name} {self.last_name}",
                'login': self.email,
                'email': self.email,
                'partner_id': self.partner_id.id,
                'groups_id': [(6, 0, [self.env.ref('base.group_portal').id])],
            }])
            self.user_id = user.id

    def action_create_emergency_contact(self):
        self.ensure_one()
        emergency_category = self.env.ref('erpquick_school_management.res_partner_category_student_ec')
        return {
            'name': 'Create Emergency Contact',
            'type': 'ir.actions.act_window',
            'res_model': 'res.partner',
            'view_mode': 'form',
            'view_id': self.env.ref('erpquick_school_management.emergency_contact_view_form').id,
            'target': 'new',
            'context': {
                'default_category_id': [(6, 0, [emergency_category.id])],
                'default_company_type': 'person',
                'default_student_emergency_contact_of_ids': [(6, 0, [self.id])]
            }
        }
