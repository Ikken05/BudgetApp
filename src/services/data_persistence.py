import json
from typing import List, Dict
import os

class JSONPersistence:
    def __init__(self, expenses_file: str = 'data/expenses.json', 
                 budget_file: str = 'data/budget_config.json'):
        self.expenses_file = expenses_file
        self.budget_file = budget_file
    
    def save_expenses(self, expenses: List[Dict]):
        """Save expenses to JSON file"""
        os.makedirs(os.path.dirname(self.expenses_file), exist_ok=True)
        with open(self.expenses_file, 'w') as f:
            json.dump(expenses, f, indent=4)
    
    def load_expenses(self) -> List[Dict]:
        """Load expenses from JSON file"""
        try:
            with open(self.expenses_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def save_budget(self, budget: Dict):
        """Save budget configuration to JSON file"""
        os.makedirs(os.path.dirname(self.budget_file), exist_ok=True)
        with open(self.budget_file, 'w') as f:
            json.dump(budget, f, indent=4)
    
    def load_budget(self) -> Dict:
        """Load budget configuration from JSON file"""
        try:
            with open(self.budget_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}