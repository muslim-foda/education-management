from odoo import fields, models


class ClassAttendanceTag(models.Model):
    _name = "class.attendance.tag"
    _description = "Class Attendance Tag"

    name = fields.Char(
        required=True,
    )

    color = fields.Integer()
