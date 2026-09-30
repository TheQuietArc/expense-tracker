"""JSON file storage with atomic writes and corrupt-file recovery."""
import json
import logging
import os

log = logging.getLogger(__name__)


def _empty():
    return {"budget": None, "expenses": []}


class JsonStorage:
    def __init__(self, path="expenses.json"):
        self.path = path

    def load(self):
        """Return stored data. A missing file gives empty data; a corrupt
        file is moved aside to '<path>.corrupt' and empty data is returned."""
        if not os.path.exists(self.path):
            return _empty()
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, dict) or not isinstance(data.get("expenses", []), list):
                raise ValueError("unexpected structure")
        except (json.JSONDecodeError, ValueError):
            backup = self.path + ".corrupt"
            os.replace(self.path, backup)
            log.error("Data file was corrupt; moved to %s", backup)
            print(f"Warning: data file was corrupt. Backup saved as {backup}.")
            return _empty()
        data.setdefault("budget", None)
        data.setdefault("expenses", [])
        return data

    def save(self, data):
        """Write data atomically so a crash cannot leave a half-written file."""
        tmp_path = self.path + ".tmp"
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        os.replace(tmp_path, self.path)
        log.info("Saved %d expenses", len(data.get("expenses", [])))
