from odoo import api, fields, models


class GradeSubject(models.Model):
    _name = "grade.subject"
    _description = "Grade Subject"

    name = fields.Char(
        required=True,
    )

    optional_choice = fields.Boolean()

    company_id = fields.Many2one(
        comodel_name="res.company",
        default=lambda self: self.env.company,
        required=True,
    )

    grade_id = fields.Many2one(
        comodel_name="grade",
        required=True,
    )

    credit_value = fields.Integer()

    subject_code = fields.Char()

    scale_id = fields.Many2one(
        comodel_name="grade.scale",
    )

    section_visibility = fields.Boolean(
        compute="_compute_section_visibility",
    )

    @api.depends("grade_id")
    def _compute_section_visibility(self):
        for subject in self:
            subject.section_visibility = bool(subject.grade_id)

    is_single_company = fields.Boolean(
        compute="_compute_is_single_company",
    )

    @api.depends_context("allowed_company_ids")
    def _compute_is_single_company(self):
        is_single_company = len(self.env.companies) == 1
        for record in self:
            record.is_single_company = is_single_company
