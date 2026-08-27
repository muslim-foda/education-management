from odoo import api, fields, models
from odoo.exceptions import ValidationError


class GradeScale(models.Model):
    _name = "grade.scale"

    name = fields.Char(required=True)
    gpa_calculation = fields.Boolean(string="GPA Calculation", default=True)
    scale_line_ids = fields.One2many(
        comodel_name="grade.scale.line",
        inverse_name="scale_id",
        string="Scale Lines",
    )
    active = fields.Boolean(default=True)


class GradeScaleLine(models.Model):
    _name = "grade.scale.line"
    _order = "max_percent desc"

    scale_id = fields.Many2one(
        comodel_name="grade.scale",
        string="Grade Scale",
        required=True,
        ondelete="cascade",
    )
    symbol = fields.Char(required=True)
    max_percent = fields.Float(string="Max(%)")
    min_percent = fields.Float(string="Min(%)")
    points = fields.Float()
    symbol_condition = fields.Char(string="Symbol Con...")
    effort = fields.Char()
    short_summary = fields.Text()

    @api.constrains("max_percent", "min_percent")
    def _check_percent_range(self):
        for line in self:
            if line.min_percent > line.max_percent:
                raise ValidationError(
                    self.env._("Min(%) cannot be greater than Max(%).")
                )
