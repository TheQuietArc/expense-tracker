import csv
import os
import tempfile
import unittest

from expense_tracker.models import Expense
from expense_tracker.reports import (
    category_totals,
    export_csv,
    format_summary,
    monthly_summary,
)


def sample():
    return [
        Expense(1, "2026-09-01", 100.0, "food", "lunch"),
        Expense(2, "2026-09-02", 50.0, "food", "tea"),
        Expense(3, "2026-09-03", 350.0, "study", "book"),
    ]


class TestReports(unittest.TestCase):
    def test_category_totals(self):
        self.assertEqual(category_totals(sample()), {"food": 150.0, "study": 350.0})

    def test_summary_without_budget(self):
        s = monthly_summary(sample(), "2026-09")
        self.assertEqual(s["total"], 500.0)
        self.assertEqual(s["top_category"], "study")
        self.assertIsNone(s["alert"])

    def test_budget_alert_levels(self):
        self.assertEqual(monthly_summary(sample(), "2026-09", 1000)["alert"], "OK")
        self.assertEqual(monthly_summary(sample(), "2026-09", 550)["alert"], "WARNING")
        s = monthly_summary(sample(), "2026-09", 400)
        self.assertEqual(s["alert"], "OVER")
        self.assertEqual(s["remaining"], -100.0)

    def test_empty_month_message(self):
        s = monthly_summary([], "2026-09")
        self.assertIn("No expenses", format_summary(s))

    def test_export_csv(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "out.csv")
            self.assertEqual(export_csv(sample(), path), 3)
            with open(path, newline="", encoding="utf-8") as f:
                rows = list(csv.reader(f))
        self.assertEqual(rows[0], ["id", "date", "category", "amount", "note"])
        self.assertEqual(len(rows), 4)


if __name__ == "__main__":
    unittest.main()
