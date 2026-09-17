# Copyright 2026 <muslimfoda1@gmail.com/ name = X >
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from psycopg2 import IntegrityError

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestGradeScale(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Scale = cls.env["grade.scale"]
        cls.Line = cls.env["grade.scale.line"]

    def _create_full_scale(self, name="Test Scale"):
        """Create a scale that continuously covers 0-100%."""
        scale = self.Scale.create({"name": name})
        self.Line.create(
            {
                "scale_id": scale.id,
                "symbol": "A",
                "max_percent": 100.00,
                "min_percent": 50.00,
                "points": 10.00,
                "symbol_condition": "Pass",
                "effort": "excellent",
            }
        )
        self.Line.create(
            {
                "scale_id": scale.id,
                "symbol": "F",
                "max_percent": 49.99,
                "min_percent": 0.00,
                "points": 0.00,
                "symbol_condition": "Fail",
                "effort": "unsatisfactory",
            }
        )
        return scale

    # -- action_confirm / _check_ranges ---------------------------------

    def test_confirm_full_coverage_succeeds(self):
        scale = self._create_full_scale()
        scale.action_confirm()
        self.assertEqual(scale.state, "confirmed")

    def test_confirm_without_lines_fails(self):
        scale = self.Scale.create({"name": "Empty Scale"})
        with self.assertRaises(ValidationError):
            scale.action_confirm()

    def test_confirm_not_starting_at_100_fails(self):
        scale = self.Scale.create({"name": "Bad Top Scale"})
        self.Line.create(
            {
                "scale_id": scale.id,
                "symbol": "A",
                "max_percent": 90.00,
                "min_percent": 0.00,
                "points": 10.00,
                "symbol_condition": "Pass",
                "effort": "excellent",
            }
        )
        with self.assertRaises(ValidationError):
            scale.action_confirm()

    def test_confirm_not_ending_at_0_fails(self):
        scale = self.Scale.create({"name": "Bad Bottom Scale"})
        self.Line.create(
            {
                "scale_id": scale.id,
                "symbol": "A",
                "max_percent": 100.00,
                "min_percent": 10.00,
                "points": 10.00,
                "symbol_condition": "Pass",
                "effort": "excellent",
            }
        )
        with self.assertRaises(ValidationError):
            scale.action_confirm()

    def test_confirm_with_gap_fails(self):
        """A gap between line ranges must be rejected."""
        scale = self.Scale.create({"name": "Gap Scale"})
        self.Line.create(
            {
                "scale_id": scale.id,
                "symbol": "A",
                "max_percent": 100.00,
                "min_percent": 60.00,
                "points": 10.00,
                "symbol_condition": "Pass",
                "effort": "excellent",
            }
        )
        self.Line.create(
            {
                "scale_id": scale.id,
                "symbol": "F",
                "max_percent": 50.00,
                "min_percent": 0.00,
                "points": 0.00,
                "symbol_condition": "Fail",
                "effort": "unsatisfactory",
            }
        )
        with self.assertRaises(ValidationError):
            scale.action_confirm()

    def test_reset_to_draft(self):
        scale = self._create_full_scale()
        scale.action_confirm()
        scale.action_reset_to_draft()
        self.assertEqual(scale.state, "draft")

    # -- SQL constraints -------------------------------------------------

    def test_duplicate_scale_name_fails(self):
        self.Scale.create({"name": "Unique Scale"})
        with self.assertRaises(IntegrityError):
            with self.env.cr.savepoint():
                self.Scale.create({"name": "Unique Scale"})

    def test_duplicate_symbol_in_scale_fails(self):
        scale = self.Scale.create({"name": "Symbol Scale"})
        self.Line.create(
            {
                "scale_id": scale.id,
                "symbol": "A",
                "max_percent": 100.00,
                "min_percent": 50.00,
                "points": 10.00,
                "symbol_condition": "Pass",
                "effort": "excellent",
            }
        )
        with self.assertRaises(IntegrityError):
            with self.env.cr.savepoint():
                self.Line.create(
                    {
                        "scale_id": scale.id,
                        "symbol": "A",
                        "max_percent": 49.99,
                        "min_percent": 0.00,
                        "points": 0.00,
                        "symbol_condition": "Fail",
                        "effort": "unsatisfactory",
                    }
                )

    def test_duplicate_max_percent_in_scale_fails(self):
        """Duplicate max_percent values must be rejected."""
        scale = self.Scale.create({"name": "Max Percent Scale"})
        self.Line.create(
            {
                "scale_id": scale.id,
                "symbol": "A",
                "max_percent": 80.00,
                "min_percent": 50.00,
                "points": 10.00,
                "symbol_condition": "Pass",
                "effort": "excellent",
            }
        )
        with self.assertRaises(IntegrityError):
            with self.env.cr.savepoint():
                self.Line.create(
                    {
                        "scale_id": scale.id,
                        "symbol": "B",
                        "max_percent": 80.00,
                        "min_percent": 0.00,
                        "points": 5.00,
                        "symbol_condition": "Fair",
                        "effort": "satisfactory",
                    }
                )

    def test_min_greater_than_max_fails(self):
        scale = self.Scale.create({"name": "Order Scale"})
        with self.assertRaises(IntegrityError):
            with self.env.cr.savepoint():
                self.Line.create(
                    {
                        "scale_id": scale.id,
                        "symbol": "A",
                        "max_percent": 10.00,
                        "min_percent": 50.00,
                        "points": 10.00,
                        "symbol_condition": "Pass",
                        "effort": "excellent",
                    }
                )

    def test_percent_out_of_range_fails(self):
        scale = self.Scale.create({"name": "Range Scale"})
        with self.assertRaises(IntegrityError):
            with self.env.cr.savepoint():
                self.Line.create(
                    {
                        "scale_id": scale.id,
                        "symbol": "A",
                        "max_percent": 110.00,
                        "min_percent": 50.00,
                        "points": 10.00,
                        "symbol_condition": "Pass",
                        "effort": "excellent",
                    }
                )
