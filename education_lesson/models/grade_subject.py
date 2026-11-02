from odoo import fields, models


class GradeSubject(models.Model):
    _inherit = "grade.subject"

    lesson_plan_ids = fields.One2many(
        comodel_name="lesson.plans",
        inverse_name="subject_id",
        string="Lesson Plans",
    )
