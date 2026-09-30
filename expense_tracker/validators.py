"""Input validation helpers. Every function returns a cleaned value or
raises ValidationError with a user-friendly message."""
import math
from datetime import datetime

CATEGORIES = ["food", "travel", "study", "rent", "entertainment", "other"]
MAX_AMOUNT = 10_000_000
MAX_NOTE_LENGTH = 100


class ValidationError(ValueError):
    """Raised when user input is invalid."""


def validate_amount(value):
    try:
        amount = float(value)
    except (TypeError, ValueError):
        raise ValidationError("Amount must be a number.")
    if not math.isfinite(amount):
        raise ValidationError("Amount must be a finite number.")
    if amount <= 0:
        raise ValidationError("Amount must be greater than 0.")
    if amount > MAX_AMOUNT:
        raise ValidationError(f"Amount must not exceed {MAX_AMOUNT}.")
    return round(amount, 2)


def validate_category(value):
    category = str(value).strip().lower()
    if category not in CATEGORIES:
        raise ValidationError(
            f"Unknown category '{value}'. Choose from: {', '.join(CATEGORIES)}."
        )
    return category


def validate_date(value):
    try:
        return datetime.strptime(str(value).strip(), "%Y-%m-%d").strftime("%Y-%m-%d")
    except ValueError:
        raise ValidationError("Date must be a valid date in YYYY-MM-DD format.")


def validate_month(value):
    try:
        return datetime.strptime(str(value).strip(), "%Y-%m").strftime("%Y-%m")
    except ValueError:
        raise ValidationError("Month must be in YYYY-MM format.")


def validate_note(value):
    note = "" if value is None else str(value).strip()
    if len(note) > MAX_NOTE_LENGTH:
        raise ValidationError(f"Note must be at most {MAX_NOTE_LENGTH} characters.")
    return note
