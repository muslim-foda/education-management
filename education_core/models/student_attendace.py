from odoo import fields, models
from odoo.exceptions import UserError


class StudentAttendance(models.Model):
    _name = "student.attendance"
    _description = "Student Attendance"

    student_id = fields.Many2one(
        comodel_name="student",
        required=True,
        ondelete="restrict",
        index=True,
    )
    attendance_date = fields.Date(
        required=True,
        default=fields.Date.context_today,
        index=True,
    )
    check_in = fields.Datetime()
    # current_academic_year_id = fields.Many2one(
    #     comodel_name="education.academic.year",
    #     string="Current Academic Year",
    # )
    attendance_state = fields.Selection(
        selection=[
            ("present", "Present"),
            ("absent", "Absent"),
        ],
        string="Attendance Status",
        required=True,
        default="present",
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="School",
        required=True,
        default=lambda self: self.env.company,
        index=True,
    )

    total_hours_spent = fields.Float(
        compute="_compute_total_hours_spent",
        store=True,
    )
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("lock", "Locked"),
        ],
        required=True,
        default="new",
        copy=False,
    )
    # class_attendance_ids = fields.One2many(
    #     comodel_name="class.attendance",
    #     string="Class Attendance",
    # )

    def lock_attendance(self):
        for attendance in self:
            if attendance.state != "new":
                raise UserError(self.env._("Attendance is already locked."))
            attendance.state = "lock"
