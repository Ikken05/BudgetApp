import matplotlib.pyplot as plt
from typing import Dict
from ..models.expense import ExpenseCategory

class ExpenseAnalyzer:
    @staticmethod
    def generate_category_pie_chart(
        category_totals: Dict[ExpenseCategory, float], 
        output_path: str = 'expense_categories.png'
    ):
        """Generate pie chart of expenses by category"""
        # Filter out categories with zero expenses
        filtered_totals = {
            cat: total for cat, total in category_totals.items() if total > 0
        }
        
        plt.figure(figsize=(10, 7))
        plt.pie(
            filtered_totals.values(), 
            labels=[cat.value for cat in filtered_totals.keys()], 
            autopct='%1.1f%%'
        )
        plt.title('Expenses by Category')
        plt.axis('equal')
        plt.savefig(output_path)
        plt.close()