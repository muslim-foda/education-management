from odoo import fields, models
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare

PERCENTAGE_DIGITS = (5, 2)


class GradeScale(models.Model):
    _name = "grade.scale"
    _description = "Grade Scale"
    _order = "name, id"

    name = fields.Char(
        required=True,
    )

    gpa_calculation = fields.Boolean(
        string="GPA Calculation",
        default=True,
    )

    scale_line_ids = fields.One2many(
        "grade.scale.line",
        "scale_id",
        string="Scale Lines",
        copy=True,
    )

    active = fields.Boolean(
        default=True,
    )

    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("confirmed", "Confirmed"),
        ],
        default="draft",
        required=True,
        copy=False,
    )

    _name_unique = models.Constraint(
        "UNIQUE(name)",
        "The grade scale name must be unique.",
    )

    def action_confirm(self):
        for scale in self:
            scale._check_ranges()

        self.write({"state": "confirmed"})

    def action_reset_to_draft(self):
        self.write({"state": "draft"})

    def _check_ranges(self):
        self.ensure_one()

        precision = PERCENTAGE_DIGITS[1]
        lines = self.scale_line_ids.sorted("max_percent", reverse=True)

        if not lines:
            raise ValidationError(
                self.env._("Add at least one grade line before confirming.")
            )

        if not self._starts_at_100(lines, precision):
            raise ValidationError(self.env._("The grade scale must end at 100.00%."))

        if not self._ends_at_0(lines, precision):
            raise ValidationError(self.env._("The grade scale must start at 0.00%."))

        for upper, lower in zip(lines, lines[1:], strict=False):
            if not self._is_continuous(upper, lower, precision):
                raise ValidationError(
                    self.env._(
                        "The ranges '%(upper)s' and '%(lower)s' are not continuous.",
                        upper=upper.symbol,
                        lower=lower.symbol,
                    )
                )

    @staticmethod
    def _starts_at_100(lines, precision):
        return (
            float_compare(
                lines[0].max_percent,
                100,
                precision_digits=precision,
            )
            == 0
        )

    @staticmethod
    def _ends_at_0(lines, precision):
        return (
            float_compare(
                lines[-1].min_percent,
                0,
                precision_digits=precision,
            )
            == 0
        )

    @staticmethod
    def _is_continuous(upper, lower, precision):
        step = 10**-precision

        return (
            float_compare(
                lower.max_percent,
                upper.min_percent - step,
                precision_digits=precision,
            )
            == 0
        )


class GradeScaleLine(models.Model):
    _name = "grade.scale.line"
    _description = "Grade Scale Line"
    _order = "max_percent desc, id"

    scale_id = fields.Many2one(
        "grade.scale",
        string="Grade Scale",
        required=True,
        ondelete="cascade",
    )

    symbol = fields.Char(
        required=True,
    )

    max_percent = fields.Float(
        string="Max (%)",
        required=True,
        digits=PERCENTAGE_DIGITS,
    )

    min_percent = fields.Float(
        string="Min (%)",
        required=True,
        digits=PERCENTAGE_DIGITS,
    )

    points = fields.Float(
        required=True,
        digits=(5, 2),
    )

    symbol_condition = fields.Char(
        required=True,
    )

    short_summary = fields.Text(
        required=False,
    )

    effort = fields.Selection(
        selection=[
            ("excellent", "Excellent"),
            ("good", "Good"),
            ("satisfactory", "Satisfactory"),
            ("poor", "Poor"),
            ("needs_improvement", "Needs Improvement"),
            ("unsatisfactory", "Unsatisfactory"),
        ],
        required=True,
    )

    _range_boundaries = models.Constraint(
        "CHECK(min_percent >= 0 AND max_percent <= 100)",
        "Grade percentages must be between 0.00 and 100.00.",
    )

    _range_order = models.Constraint(
        "CHECK(min_percent < max_percent)",
        "The minimum percentage must be lower than the maximum percentage.",
    )

    _symbol_unique = models.Constraint(
        "UNIQUE(scale_id, symbol)",
        "The grade symbol must be unique within a grade scale.",
    )

    _max_percent_unique = models.Constraint(
        "UNIQUE(scale_id, max_percent)",
        "Two grade lines in the same scale cannot share the same maximum percentage.",
    )
