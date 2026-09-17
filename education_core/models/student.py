import secrets

from odoo import api, fields, models


class Student(models.Model):
    _name = "student"
    _inherit = ["mail.thread", "mail.activity.mixin", "sequence.mixin"]
    _description = "Student"
    _rec_name = "name"
    _inherits = {"res.partner": "partner_id"}
    _sequence_code = "student"

    # Fields
    name = fields.Char()
    partner_id = fields.Many2one(
        "res.partner",
        required=True,
        ondelete="cascade",
    )
    category_ids = fields.Many2many("res.partner.category")
    student_code = fields.Char(
        readonly=True,
        copy=False,
        index=True,
    )
    student_active = fields.Boolean(
        default=False,
    )
    father_name = fields.Char()
    father_phone = fields.Char()
    father_occupation = fields.Char()
    mother_name = fields.Char()
    mother_phone = fields.Char()
    mother_occupation = fields.Char()
    birth_date = fields.Date()
    gender = fields.Selection(
        [
            ("male", "Male"),
            ("female", "Female"),
        ],
    )
    sequence_id = fields.Many2one("ir.sequence")
    bio = fields.Text()
    profile_completed = fields.Boolean(
        default=False,
    )

    # SQL constraints
    _student_name_unique = models.Constraint(
        "unique(name)",
        "Student name must be unique!",
    )

    # CRUD methods
    @api.model_create_multi
    def create(self, vals_list):
        """Create students and generate a student code when needed."""
        for vals in vals_list:
            if not vals.get("student_code"):
                vals["student_code"] = self._generate_student_code()

        return super().create(vals_list)

    # Business methods
    def _generate_student_code(self):
        """Generate a unique 8-digit student code."""
        while True:
            student_code = "".join(str(secrets.randbelow(10)) for _ in range(8))
            if not self.search(
                [("student_code", "=", student_code)],
                limit=1,
            ):
                return student_code
