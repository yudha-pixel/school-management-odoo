from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    student_emergency_contact_of_ids = fields.One2many(
        'student.student',
        'emergency_contact_id',
        string='Emergency Contact Of Students'
    )
    teacher_emergency_contact_of_ids = fields.One2many(
        'teacher.teacher',
        'emergency_contact_id',
        string='Emergency Contact Of Teachers'
    )
    is_student_emergency_contact = fields.Boolean(compute="_compute_emergency_type")
    is_teacher_emergency_contact = fields.Boolean(compute="_compute_emergency_type")

    @api.depends('category_id')
    def _compute_emergency_type(self):
        student_emergency_category = self.env.ref('erpquick_school_management.res_partner_category_student_ec')
        teacher_emergency_category = self.env.ref('erpquick_school_management.res_partner_category_teacher_ec')

        for partner in self:
            student_tag = partner.category_id.filtered(lambda c: c == student_emergency_category)
            teacher_tag = partner.category_id.filtered(lambda c: c == teacher_emergency_category)
            partner.is_student_emergency_contact = bool(student_tag)
            partner.is_teacher_emergency_contact = bool(teacher_tag)
