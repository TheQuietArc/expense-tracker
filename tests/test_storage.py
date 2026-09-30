import os
import tempfile
import unittest

from expense_tracker.storage import JsonStorage


class TestStorage(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.tmp.name, "data.json")
        self.storage = JsonStorage(self.path)

    def tearDown(self):
        self.tmp.cleanup()

    def test_missing_file_gives_empty_data(self):
        self.assertEqual(self.storage.load(), {"budget": None, "expenses": []})

    def test_save_and_load_roundtrip(self):
        data = {"budget": 100.0, "expenses": [{"id": 1}]}
        self.storage.save(data)
        self.assertEqual(self.storage.load(), data)

    def test_corrupt_file_is_backed_up(self):
        with open(self.path, "w") as f:
            f.write("{not valid json")
        self.assertEqual(self.storage.load(), {"budget": None, "expenses": []})
        self.assertTrue(os.path.exists(self.path + ".corrupt"))
        self.assertFalse(os.path.exists(self.path))


if __name__ == "__main__":
    unittest.main()
