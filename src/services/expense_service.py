import os
from typing import List, Dict
from ..models.expense import Expense, ExpenseCategory
from ..models.budget import Budget
from .data_persistence import JSONPersistence

class ExpenseService:
    def __init__(self, persistence: JSONPersistence = None):
        self.persistence = persistence or JSONPersistence()
        self.expenses: List[Expense] = self._load_expenses()
        self.budget = self._load_budget()
    
    def _load_expenses(self) -> List[Expense]:
        """Load expenses from persistence"""
        expense_dicts = self.persistence.load_expenses()
        return [Expense.from_dict(exp_dict) for exp_dict in expense_dicts]
    
    def _load_budget(self) -> Budget:
        """Load budget from persistence"""
        budget_dict = self.persistence.load_budget()
        return Budget.from_dict(budget_dict) if budget_dict else Budget()
    
    def add_expense(self, expense: Expense):
        """Add a new expense"""
        self.expenses.append(expense)
        self._save_expenses()
    
    def _save_expenses(self):
        """Save expenses to persistence"""
        expense_dicts = [exp.to_dict() for exp in self.expenses]
        self.persistence.save_expenses(expense_dicts)
    
    def reset_expenses(self):
        """Reset all expenses"""
        self.expenses.clear()
        # Remove the expenses file
        try:
            os.remove(self.persistence.expenses_file)
        except FileNotFoundError:
            pass
    
    def reset_budget_limits(self):
        """Reset all budget limits to zero"""
        # Create a new empty budget
        self.budget = Budget()
        
        # Remove the budget configuration file
        try:
            os.remove(self.persistence.budget_file)
        except FileNotFoundError:
            pass
    
    def get_total_expenses(self) -> float:
        """Calculate total expenses"""
        return sum(expense.amount for expense in self.expenses)
    
    def get_expenses_by_category(self) -> Dict[ExpenseCategory, float]:
        """Calculate expenses by category"""
        category_totals = {}
        for category in ExpenseCategory:
            total = sum(
                expense.amount 
                for expense in self.expenses 
                if expense.category == category
            )
            category_totals[category] = total
        return category_totals
    
    def set_budget_limit(self, category: ExpenseCategory, limit: float):
        """Set budget limit for a category"""
        self.budget.set_limit(category, limit)
        self.persistence.save_budget(self.budget.to_dict())
    
    def check_budget_limits(self) -> Dict[ExpenseCategory, bool]:
        """Check if expenses exceed budget limits"""
        category_totals = self.get_expenses_by_category()
        return {
            category: (
                category_totals.get(category, 0) > self.budget.get_limit(category)
                if self.budget.get_limit(category) > 0 
                else False
            )
            for category in ExpenseCategory
        }