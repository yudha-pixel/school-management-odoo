from odoo import fields, models

class AcademicTerm(models.Model):
    _name = 'academic.term'
    _description = "Academic Term"

    name = fields.Char('Name', required=True)
    term_start_date = fields.Date('Start Date', required=True)
    term_end_date = fields.Date('End Date', required=True)
    academic_year_id = fields.Many2one('academic.year', 'Academic Year', required=True)
    parent_term = fields.Many2one('academic.term', 'Parent Term')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id)
