from odoo import fields, models

class OpStudentCourse(models.Model):
    _name = "student.course"
    _description = "Student Course Details"
    _inherit = "mail.thread"
    _rec_name = 'student_id'

    student_id = fields.Many2one('student.student', 'Student',
                                 ondelete="cascade", tracking=True)
    # course_id = fields.Many2one('op.course', 'Course', required=True, tracking=True)
    # batch_id = fields.Many2one('op.batch', 'Batch', tracking=True)
    # roll_number = fields.Char('Roll Number', tracking=True)
    # subject_ids = fields.Many2many('op.subject', string='Subjects')
    # academic_years_id = fields.Many2one('op.academic.year', 'Academic Year')
    # academic_term_id = fields.Many2one('op.academic.term', 'Terms')
    # state = fields.Selection([('running', 'Running'),
    #                           ('finished', 'Finished')],
    #                          string="Status", default="running")
    #
    # _sql_constraints = [
    #     ('unique_name_roll_number_id',
    #      'unique(roll_number,course_id,batch_id,student_id)',
    #      'Roll Number & Student must be unique per Batch!'),
    #     ('unique_name_roll_number_course_id',
    #      'unique(roll_number,course_id,batch_id)',
    #      'Roll Number must be unique per Batch!'),
    #     ('unique_name_roll_number_student_id',
    #      'unique(student_id,course_id,batch_id)',
    #      'Student must be unique per Batch!'),
    # ]
