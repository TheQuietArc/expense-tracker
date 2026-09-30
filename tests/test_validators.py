import unittest

from expense_tracker.validators import (
    ValidationError,
    validate_amount,
    validate_category,
    validate_date,
    validate_month,
    validate_note,
)


class TestValidators(unittest.TestCase):
    def test_amount_valid_and_rounded(self):
        self.assertEqual(validate_amount("120.456"), 120.46)
        self.assertEqual(validate_amount(50), 50.0)

    def test_amount_invalid(self):
        for bad in ["abc", "0", "-5", "nan", "inf", "99999999999", None]:
            with self.subTest(value=bad):
                with self.assertRaises(ValidationError):
                    validate_amount(bad)

    def test_category_is_normalised(self):
        self.assertEqual(validate_category("  Food "), "food")

    def test_category_invalid(self):
        with self.assertRaises(ValidationError):
            validate_category("gadgets")

    def test_date(self):
        self.assertEqual(validate_date("2026-09-15"), "2026-09-15")
        for bad in ["2026-13-01", "15-09-2026", "yesterday"]:
            with self.subTest(value=bad):
                with self.assertRaises(ValidationError):
                    validate_date(bad)

    def test_month(self):
        self.assertEqual(validate_month("2026-09"), "2026-09")
        with self.assertRaises(ValidationError):
            validate_month("09-2026")

    def test_note_too_long(self):
        self.assertEqual(validate_note(None), "")
        with self.assertRaises(ValidationError):
            validate_note("x" * 101)


if __name__ == "__main__":
    unittest.main()
