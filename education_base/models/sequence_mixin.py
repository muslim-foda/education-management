from odoo import api, fields, models


class SequenceMixin(models.AbstractModel):
    _name = "sequence.mixin"

    reference = fields.Char(
        readonly=True,
        copy=False,
        index=True,
    )

    _sequence_code = None

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("reference", "New") == "New":
                vals["reference"] = self.env["ir.sequence"].next_by_code(
                    self._sequence_code
                )

        return super().create(vals_list)
