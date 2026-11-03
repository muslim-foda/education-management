from odoo import fields, models


class ClassAttendance(models.Model):
    _name = "class.attendance"
    _description = "Class Attendance"

    student_id = fields.Many2one(
        comodel_name="student",
        required=True,
    )

    class_id = fields.Many2one(
        comodel_name="class",
        required=True,
    )

    state = fields.Selection(
        selection=[
            ("present", "Present"),
            ("absent", "Absent"),
        ],
        default="present",
        required=True,
    )

    company_id = fields.Many2one(
        comodel_name="res.company",
        string="School",
        required=True,
        default=lambda self: self.env.company,
    )

    class_date = fields.Date(
        required=True,
        default=fields.Date.context_today,
    )

    attendance_tag_ids = fields.Many2many(
        comodel_name="class.attendance.tag",
    )

    # class_ids_domain = fields.Char(
    #     string="Class Domain",
    #     compute="_compute_class_ids_domain",
    # )

    # def _compute_class_ids_domain(self):
    #     for record in self:
    #         record.class_ids_domain = "[]"
