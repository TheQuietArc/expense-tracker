"""Data model for a single expense record."""
from dataclasses import asdict, dataclass


@dataclass
class Expense:
    id: int
    date: str        # YYYY-MM-DD
    amount: float
    category: str
    note: str = ""

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        """Build an Expense from a stored dictionary.

        Raises KeyError / ValueError / TypeError if the record is malformed.
        """
        return cls(
            id=int(data["id"]),
            date=str(data["date"]),
            amount=float(data["amount"]),
            category=str(data["category"]),
            note=str(data.get("note", "")),
        )
