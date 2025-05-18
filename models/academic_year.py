from odoo import fields, models
from odoo.exceptions import ValidationError
from datetime import timedelta


def _split_range(start, end, parts):
    """Split a date range into N equal parts."""
    total_days = (end - start).days + 1
    per_part = total_days // parts
    current = start
    ranges = []
    for i in range(parts - 1):
        part_end = current + timedelta(days=per_part - 1)
        ranges.append((current, part_end))
        current = part_end + timedelta(days=1)
    ranges.append((current, end))
    return ranges

class AcademicYear(models.Model):
    _name = 'academic.year'
    _description = "Academic Year"

    name = fields.Char('Name', required=True)
    start_date = fields.Date('Start Date', required=True)
    end_date = fields.Date('End Date', required=True)
    term_structure = fields.Selection([('two_sem', 'Two Semesters'),
                                       ('two_sem_qua', 'Two Semesters subdivided by Quarters'),
                                       ('two_sem_final', 'Two Semesters subdivided by Quarters and Final Exams'),
                                       ('three_sem', 'Three Trimesters'),
                                       ('four_Quarter', 'Four Quarters'),
                                       ('final_year', 'Final Year Grades subdivided by Quarters'),
                                       ('others', 'Other(overlapping terms, custom schedules)')],
                                      string='Term Structure', default='two_sem',
                                      required=True)
    academic_term_ids = fields.One2many('academic.term', 'academic_year_id', string='Academic Terms')
    create_boolean = fields.Boolean()
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id)

    def _create_term(self, name, start, end, year_id, parent_id=None):
        academic_term_id = self.env['academic.term'].create([{
            'name': name,
            'term_start_date': start,
            'term_end_date': end,
            'academic_year_id': year_id,
            'parent_term': parent_id
        }])
        return academic_term_id

    def _generate_subterms(self, parent_term, count, prefix="Quarter", add_final_exam=False):
        ranges = _split_range(parent_term.term_start_date, parent_term.term_end_date, count)
        for idx, (start, end) in enumerate(ranges, start=1):
            self._create_term(f"{prefix} {idx}", start, end, parent_term.academic_year_id.id, parent_term.id)
        if add_final_exam:
            self._create_term(f"Final Exam {parent_term.name}", parent_term.term_end_date,
                              parent_term.term_end_date, parent_term.academic_year_id.id, parent_term.id)

    def term_create(self):
        if self.academic_term_ids:
            raise ValidationError("Terms already exist for this academic year. Please remove them first if you want to regenerate.")

        if not self.start_date or not self.end_date:
            raise ValidationError("Start Date and End Date must be set before generating academic terms.")

        start = self.start_date
        end = self.end_date

        if self.term_structure == 'two_sem':
            for i, (s, e) in enumerate(_split_range(start, end, 2), start=1):
                self._create_term(f"Semester {i}", s, e, self.id)

        elif self.term_structure == 'two_sem_qua':
            semesters = []
            for i, (s, e) in enumerate(_split_range(start, end, 2), start=1):
                sem = self._create_term(f"Semester {i}", s, e, self.id)
                semesters.append(sem)
            for sem in semesters:
                self._generate_subterms(sem, 2)

        elif self.term_structure == 'two_sem_final':
            semesters = []
            for i, (s, e) in enumerate(_split_range(start, end, 2), start=1):
                sem = self._create_term(f"Semester {i}", s, e, self.id)
                semesters.append(sem)
            for sem in semesters:
                self._generate_subterms(sem, 2, add_final_exam=True)

        elif self.term_structure == 'three_sem':
            for i, (s, e) in enumerate(_split_range(start, end, 3), start=1):
                self._create_term(f"Semester {i}", s, e, self.id)

        elif self.term_structure == 'four_Quarter':
            for i, (s, e) in enumerate(_split_range(start, end, 4), start=1):
                self._create_term(f"Semester {i}", s, e, self.id)

        elif self.term_structure == 'final_year':
            final_year = self._create_term("Final Year", start, end, self.id)
            if final_year:
                self._generate_subterms(final_year, 4)