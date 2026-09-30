"""File-based logging so the terminal output stays clean."""
import logging
from logging.handlers import RotatingFileHandler


def setup_logging(log_file="expense_tracker.log", level=logging.INFO):
    root = logging.getLogger()
    if any(getattr(h, "_expense_tracker", False) for h in root.handlers):
        return
    handler = RotatingFileHandler(log_file, maxBytes=100_000, backupCount=2, encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
    handler._expense_tracker = True
    root.setLevel(level)
    root.addHandler(handler)
