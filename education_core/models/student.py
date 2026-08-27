import secrets

from odoo import api, fields, models


class Student(models.Model):
    _name = "student"
    _inherit = ["mail.thread", "mail.activity.mixin", "sequence.mixin"]
    _rec_name = "name"
    _inherits = {"res.partner": "partner_id"}
    _sequence_code = "student"

    category_ids = fields.Many2many("res.partner.category", string="Tags")
    partner_id = fields.Many2one(
        "res.partner",
        required=True,
        ondelete="cascade",
    )
    student_code = fields.Char(
        readonly=True,
        copy=False,
        index=True,
    )
    student_active = fields.Boolean(
        string="Portal Access",
        default=False,
    )

    father_name = fields.Char(string="Father's Name")
    father_phone = fields.Char(string="Father's Phone")
    father_occupation = fields.Char(string="Father's Occupation")
    mother_name = fields.Char(string="Mother's Name")
    mother_phone = fields.Char(string="Mother's Phone")
    mother_occupation = fields.Char(string="Mother's Occupation")

    birth_date = fields.Date(string="Date of Birth")
    gender = fields.Selection(
        [
            ("male", "Male"),
            ("female", "Female"),
        ],
    )
    _student_name_unique = models.Constraint(
        "unique(name)",
        "Student name must be unique!",
    )
    sequence_id = fields.Many2one("ir.sequence")
    bio = fields.Text()
    profile_completed = fields.Boolean(
        default=False,
    )

    def _generate_student_code(self):
        """Generate a unique 8-digit student code."""

        while True:
            code = "".join(str(secrets.randbelow(10)) for _ in range(8))
            if not self.search([("student_code", "=", code)], limit=1):
                return code

    @api.model_create_multi
    def create(self, vals_list):
        """Create students and generate a unique 8-digit code when not provided."""

        for vals in vals_list:
            if not vals.get("student_code"):
                vals["student_code"] = self._generate_student_code()

        return super().create(vals_list)
