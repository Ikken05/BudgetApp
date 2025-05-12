from dataclasses import dataclass, field
from datetime import date
from enum import Enum, auto
from typing import Optional

class ExpenseCategory(Enum):
    FOOD = "Food"
    TRANSPORTATION = "Transportation"
    ENTERTAINMENT = "Entertainment"
    UTILITIES = "Utilities"
    MISCELLANEOUS = "Miscellaneous"

@dataclass
class Expense:
    date: date
    category: ExpenseCategory
    amount: float
    description: str = ''
    id: Optional[str] = field(default_factory=lambda: str(hash(date.today())))

    def to_dict(self):
        """Convert expense to dictionary for serialization"""
        return {
            'id': self.id,
            'date': self.date.isoformat(),
            'category': self.category.value,
            'amount': self.amount,
            'description': self.description
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Create Expense from dictionary"""
        return cls(
            date=date.fromisoformat(data['date']),
            category=ExpenseCategory(data['category']),
            amount=float(data['amount']),
            description=data.get('description', ''),
            id=data.get('id')
        )