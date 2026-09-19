from odoo import fields, models


class Class(models.Model):
    _name = "class"
    _description = "Class"

    name_class = fields.Char(
        string="class",
        required=True,
    )
