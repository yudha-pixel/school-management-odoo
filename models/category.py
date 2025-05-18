from odoo import models, fields

class StudentCategory(models.Model):
    _name = "category.category"
    _description = "Category"

    name = fields.Char('Name', size=256, required=True)
    code = fields.Char('Code', size=16, required=True)
    company_id = fields.Many2one(
        "res.company", string="Company", default=lambda self: self.env.company
    )

    _sql_constraints = [
        ('unique_category_code',
         'unique(code)', 'Code should be unique per category!')]