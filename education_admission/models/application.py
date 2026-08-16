from odoo import fields, models


class EducationApplication(models.Model):
    _name = "education.application"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = "student_name"

    student_name = fields.Char()
    birth_date = fields.Date()
    email = fields.Char()
    phone = fields.Char()
    parent_email = fields.Char()

    student_image = fields.Binary(
        attachment=True,
    )

    medical_disability = fields.Selection(
        selection=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        string="Any Identified Disability/Ailment",
        default="no",
        required=True,
    )
    known_medical_disability = fields.Text()

    # Parent information
    father_name = fields.Char(
        string="Father's Name",
    )
    father_phone = fields.Char(
        string="Father's Phone",
    )
    father_occupation = fields.Char(
        string="Father's Occupation",
    )
    mother_name = fields.Char(
        string="Mother's Name",
    )
    mother_phone = fields.Char(
        string="Mother's Phone",
    )
    mother_occupation = fields.Char(
        string="Mother's Occupation",
    )

    application_date = fields.Date(
        default=fields.Date.context_today,
        required=True,
    )

    company_id = fields.Many2one(
        "res.company",
        string="School",
        default=lambda self: self.env.company,
        required=True,
    )

    # grade_id = fields.Many2one(
    #     "education.grade",
    #     string="Grade",
    # )

    # student_id = fields.Many2one(
    #     "education.student",
    #     string="Student",
    # )

    queries = fields.Text(
        string="Admission Query",
    )

    attachment_ids = fields.Many2many(
        "ir.attachment",
        string="Documents",
    )

    street = fields.Char()
    street2 = fields.Char()
    city = fields.Char()

    state_id = fields.Many2one(
        "res.country.state",
    )
    zip = fields.Char()
    country_id = fields.Many2one(
        "res.country",
    )

    blood_group = fields.Selection(
        selection=[
            ("A+", "A+ve"),
            ("B+", "B+ve"),
            ("O+", "O+ve"),
            ("AB+", "AB+ve"),
            ("A-", "A-ve"),
            ("B-", "B-ve"),
            ("O-", "O-ve"),
            ("AB-", "AB-ve"),
        ],
    )

    gender = fields.Selection(
        selection=[
            ("m", "Male"),
            ("f", "Female"),
            ("o", "Other"),
        ],
        required=True,
        default="m",
    )

    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("confirm", "Confirmed"),
            ("enroll", "Enrolled"),
            ("cancel", "Cancelled"),
        ],
        default="new",
        required=True,
        tracking=True,
    )

    def confirm_application(self):
        self.ensure_one()
        self.state = "confirm"

    def enroll_application(self):
        self.ensure_one()
        self.state = "enroll"

    def action_cancel(self):
        self.ensure_one()
        self.state = "cancel"

    # def get_student_id(self):
    #     self.ensure_one()
    #
    #     return {
    #         "type": "ir.actions.act_window",
    #         "name": "Student",
    #         "res_model": "education.student",
    #         "view_mode": "form",
    #         "res_id": self.student_id.id,
    #         "target": "current",
    #     }
