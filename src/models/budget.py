from dataclasses import dataclass, field
from typing import Dict
from .expense import ExpenseCategory

@dataclass
class Budget:
    limits: Dict[ExpenseCategory, float] = field(default_factory=dict)
    
    def set_limit(self, category: ExpenseCategory, amount: float):
        """Set budget limit for a specific category"""
        self.limits[category] = amount
    
    def get_limit(self, category: ExpenseCategory) -> float:
        """Get budget limit for a specific category"""
        return self.limits.get(category, 0.0)
    
    def to_dict(self):
        """Convert budget to dictionary for serialization"""
        return {
            category.value: limit 
            for category, limit in self.limits.items()
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create Budget from dictionary"""
        budget = cls()
        for category_str, limit in data.items():
            category = ExpenseCategory(category_str)
            budget.set_limit(category, float(limit))
        return budget