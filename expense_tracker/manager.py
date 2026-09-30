"""Business logic: add, list, search, delete expenses and manage the budget."""
import logging
from datetime import datetime

from .models import Expense
from .validators import (
    ValidationError,
    validate_amount,
    validate_category,
    validate_date,
    validate_note,
)

log = logging.getLogger(__name__)


class ExpenseNotFoundError(ValidationError):
    """Raised when an expense ID does not exist."""


class ExpenseManager:
    def __init__(self, storage):
        self._storage = storage
        data = storage.load()
        self._expenses = []
        for record in data["expenses"]:
            try:
                self._expenses.append(Expense.from_dict(record))
            except (KeyError, ValueError, TypeError):
                log.warning("Skipping malformed record: %r", record)
        self.budget = data["budget"]

    def _save(self):
        self._storage.save({
            "budget": self.budget,
            "expenses": [e.to_dict() for e in self._expenses],
        })

    def _next_id(self):
        return max((e.id for e in self._expenses), default=0) + 1

    def add(self, amount, category, note="", date=None):
        expense = Expense(
            id=self._next_id(),
            date=validate_date(date) if date else datetime.now().strftime("%Y-%m-%d"),
            amount=validate_amount(amount),
            category=validate_category(category),
            note=validate_note(note),
        )
        self._expenses.append(expense)
        self._save()
        log.info("Added expense #%d", expense.id)
        return expense

    def list(self, category=None, month=None, sort="date"):
        rows = list(self._expenses)
        if category:
            category = validate_category(category)
            rows = [e for e in rows if e.category == category]
        if month:
            rows = [e for e in rows if e.date.startswith(month)]
        if sort == "amount":
            return sorted(rows, key=lambda e: e.amount, reverse=True)
        return sorted(rows, key=lambda e: (e.date, e.id))

    def search(self, keyword):
        keyword = keyword.strip().lower()
        return [e for e in self._expenses if keyword in e.note.lower()]

    def delete(self, expense_id):
        for expense in self._expenses:
            if expense.id == expense_id:
                self._expenses.remove(expense)
                self._save()
                log.info("Deleted expense #%d", expense_id)
                return expense
        raise ExpenseNotFoundError(f"No expense with ID {expense_id}.")

    def set_budget(self, amount):
        self.budget = validate_amount(amount)
        self._save()
        log.info("Budget set to %.2f", self.budget)
        return self.budget
