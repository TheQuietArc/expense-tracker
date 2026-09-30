import os
import tempfile
import unittest

from expense_tracker.manager import ExpenseManager, ExpenseNotFoundError
from expense_tracker.storage import JsonStorage
from expense_tracker.validators import ValidationError


class TestManager(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.tmp.name, "data.json")
        self.manager = ExpenseManager(JsonStorage(self.path))

    def tearDown(self):
        self.tmp.cleanup()

    def test_add_assigns_incrementing_ids(self):
        a = self.manager.add(10, "food", "tea", "2026-09-01")
        b = self.manager.add(20, "travel", "bus", "2026-09-02")
        self.assertEqual((a.id, b.id), (1, 2))

    def test_add_rejects_bad_input(self):
        with self.assertRaises(ValidationError):
            self.manager.add(-1, "food")
        with self.assertRaises(ValidationError):
            self.manager.add(10, "nonsense")
        self.assertEqual(self.manager.list(), [])

    def test_data_persists_between_instances(self):
        self.manager.add(10, "food", "tea", "2026-09-01")
        self.manager.set_budget(500)
        again = ExpenseManager(JsonStorage(self.path))
        self.assertEqual(len(again.list()), 1)
        self.assertEqual(again.budget, 500.0)

    def test_list_filters_and_sorting(self):
        self.manager.add(10, "food", "tea", "2026-09-01")
        self.manager.add(300, "study", "book", "2026-09-10")
        self.manager.add(50, "food", "lunch", "2026-10-02")
        self.assertEqual(len(self.manager.list(category="food")), 2)
        self.assertEqual(len(self.manager.list(month="2026-09")), 2)
        self.assertEqual(self.manager.list(sort="amount")[0].amount, 300.0)

    def test_search_is_case_insensitive(self):
        self.manager.add(300, "study", "Algorithms Book", "2026-09-10")
        self.assertEqual(len(self.manager.search("BOOK")), 1)
        self.assertEqual(self.manager.search("movie"), [])

    def test_delete(self):
        first = self.manager.add(10, "food", "tea", "2026-09-01")
        self.manager.delete(first.id)
        self.assertEqual(self.manager.list(), [])
        with self.assertRaises(ExpenseNotFoundError):
            self.manager.delete(99)

    def test_budget_validation(self):
        with self.assertRaises(ValidationError):
            self.manager.set_budget(0)


if __name__ == "__main__":
    unittest.main()
