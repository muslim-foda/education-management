from odoo import fields, models


class LessonPlans(models.Model):
    _name = "lesson.plans"
    _inherit = ["mail.thread"]
    name = fields.Char(
        required=True,
    )
    description = fields.Text()
    grade_id = fields.Many2one("grade")
    subject_id = fields.Many2one("grade.subject")
    company_id = fields.Many2one(
        "res.company",
        required=True,
        default=lambda self: self.env.company,
        index=True,
        string="school",
    )
    responsible_id = fields.Many2one(
        "res.users",
        string="Prepared By",
        default=lambda self: self.env.user,
        readonly=True,
    )

    plan_visibility = fields.Selection(
        [("all", "All"), ("only_me", "Only Me")],
        string="Shared To",
        default="all",
        required=True,
    )
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("approve", "Approved"),
            ("cancel", "Cancelled"),
        ],
        default="draft",
        required=True,
        tracking=True,
    )

    def approve_lesson_plan(self):
        self.write({"state": "approve"})

    def cancel_lesson_plan(self):
        self.write({"state": "cancel"})

    def reset_lesson_plan(self):
        self.write({"state": "draft"})
