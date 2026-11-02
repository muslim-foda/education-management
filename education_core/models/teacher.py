from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    is_teacher = fields.Boolean()
