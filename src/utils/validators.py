from datetime import date
from ..models.expense import ExpenseCategory

class ExpenseValidator:
    @staticmethod
    def validate_date(input_date: date) -> bool:
        """Validate that date is not in the future"""
        return input_date <= date.today()
    
    @staticmethod
    def validate_amount(amount: float) -> bool:
        """Validate that amount is positive"""
        return amount > 0
    
    @staticmethod
    def validate_category(category: ExpenseCategory) -> bool:
        """Validate that category is a valid ExpenseCategory"""
        return isinstance(category, ExpenseCategory)