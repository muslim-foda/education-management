from odoo import fields, models


class GradeSubject(models.Model):
    _name = "grade_subject"
    _description = "Grade Subject"

    name = fields.Char(
        required=True,
    )
