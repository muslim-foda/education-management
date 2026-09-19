from odoo import api, fields, models


class Grade(models.Model):
    _name = "grade"
    _description = "Grade"
    _order = "name"

    name = fields.Char(
        required=True,
    )
    grade_scale_id = fields.Many2one(
        comodel_name="grade.scale",
        string="Scale",
        required=True,
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        default=lambda self: self.env.company,
        required=True,
    )

    teacher_count = fields.Integer(
        compute="_compute_teacher_count",
    )

    is_single_company = fields.Boolean(
        compute="_compute_is_single_company",
    )

    @api.depends_context("allowed_company_ids")
    def _compute_is_single_company(self):
        is_single_company = len(self.env.companies) == 1
        for grade in self:
            grade.is_single_company = is_single_company
