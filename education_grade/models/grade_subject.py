from odoo import fields, models


class GradeSubject(models.Model):
    _name = "grade.subject"
    _description = "Grade Subject"
    subject = fields.Char(
        required=True,
    )

    optional_choice = fields.Boolean()

    company_id = fields.Many2one(
        "res.company",
        required=True,
        default=lambda self: self.env.company,
        index=True,
        string="school",
    )

    grade_id = fields.Many2one(
        comodel_name="grade",
        required=True,
    )

    subject_code = fields.Char(
        string="code",
    )

    scale_id = fields.Many2one(
        comodel_name="grade.scale",
    )
    passing_percent = fields.Float(
        string="Min. Passing (%)",
        required=True,
    )
    credit_value = fields.Float(
        string="Credit",
    )
    teacher_ids = fields.Many2many(
        "hr.employee",
        string="Teachers",
    )

    section_visibility = fields.Boolean(
        compute="_compute_section_visibility",
    )
