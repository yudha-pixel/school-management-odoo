from odoo import models, fields, api
from odoo.exceptions import ValidationError

class TeacherTeacher(models.Model):
    _name = 'teacher.teacher'
    _description = 'Teacher'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _inherits = {"res.partner": "partner_id"}
    _parent_name = False

    partner_id = fields.Many2one('res.partner', 'Partner', required=True, ondelete="cascade")
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
    emergency_contact_id = fields.Many2one('res.partner', 'Emergency Contact')
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

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            # Ensure partner name is passed for _inherits (res.partner)
            if not vals.get('name'):
                fname = vals.get('first_name', '')
                mname = vals.get('middle_name', '')
                lname = vals.get('last_name', '')
                full_name = f"{fname} {mname} {lname}".strip()
                vals['name'] = full_name or 'Unnamed Teacher'
        res = super().create(vals_list)
        for teacher in res:
            # Ensure partner name is passed
            if not teacher.name:
                teacher.name = f"{teacher.first_name or ''} {teacher.middle_name or ''} {teacher.last_name or ''}".strip() or "Unnamed Teacher"

            # Create a related user if not yet linked
            if not teacher.user_id:
                login = teacher.partner_id.email or f"{teacher.first_name.lower()}.{teacher.last_name.lower()}"
                existing_user = self.env['res.users'].search([('login', '=', login)], limit=1)
                if existing_user:
                    raise ValidationError(f"A user already exists with login: {login}")

                new_user = self.env['res.users'].create([{
                    'name': teacher.name,
                    'login': login,
                    'partner_id': teacher.partner_id.id,
                    'groups_id': [(6, 0, [self.env.ref('base.group_user').id])],
                    # You can use portal group or a custom one
                }])
                teacher.user_id = new_user
        return res

    @api.onchange('first_name', 'middle_name', 'last_name')
    def _onchange_name(self):
        for teacher in self:
            teacher.name = f"{teacher.first_name or ''} {teacher.middle_name or ''} {teacher.last_name or ''}".strip()

    def action_create_emergency_contact(self):
        self.ensure_one()
        emergency_category = self.env.ref('erpquick_school_management.res_partner_category_teacher_ec')
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
                'default_teacher_emergency_contact_of_ids': [(6, 0, [self.id])]
            }
        }