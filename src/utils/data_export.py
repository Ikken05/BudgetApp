import csv
import os
from typing import List, Dict
import matplotlib.pyplot as plt
import pandas as pd

from ..models.expense import Expense, ExpenseCategory
from ..models.budget import Budget

class DataExporter:
    @staticmethod
    def export_expenses_to_csv(
        expenses: List[Expense], 
        filename: str = 'expenses_report.csv'
    ):
        """
        Export expenses to a CSV file
        
        Args:
            expenses (List[Expense]): List of expenses to export
            filename (str, optional): Name of the CSV file. Defaults to 'expenses_report.csv'
        
        Returns:
            str: Path to the generated CSV file
        """
        # Ensure the 'reports' directory exists
        os.makedirs('reports', exist_ok=True)
        filepath = os.path.join('reports', filename)
        
        with open(filepath, 'w', newline='') as csvfile:
            # Define fieldnames
            fieldnames = ['Date', 'Category', 'Amount', 'Description']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Write header
            writer.writeheader()
            
            # Write expense rows
            for expense in expenses:
                writer.writerow({
                    'Date': expense.date.isoformat(),
                    'Category': expense.category.value,
                    'Amount': f'{expense.amount:.2f}',
                    'Description': expense.description
                })
        
        return filepath

    @staticmethod
    def export_budget_to_csv(
        budget: Budget, 
        expenses_by_category: Dict[ExpenseCategory, float],
        filename: str = 'budget_report.csv'
    ):
        """
        Export budget limits and actual expenses to a CSV file
        
        Args:
            budget (Budget): Budget limits
            expenses_by_category (Dict[ExpenseCategory, float]): Actual expenses by category
            filename (str, optional): Name of the CSV file. Defaults to 'budget_report.csv'
        
        Returns:
            str: Path to the generated CSV file
        """
        # Ensure the 'reports' directory exists
        os.makedirs('reports', exist_ok=True)
        filepath = os.path.join('reports', filename)
        
        with open(filepath, 'w', newline='') as csvfile:
            # Define fieldnames
            fieldnames = ['Category', 'Budget Limit', 'Actual Expenses', 'Difference', 'Status']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Write header
            writer.writeheader()
            
            # Write budget rows
            for category in ExpenseCategory:
                limit = budget.get_limit(category)
                actual_expense = expenses_by_category.get(category, 0)
                difference = limit - actual_expense
                status = 'Exceeded' if actual_expense > limit and limit > 0 else 'OK'
                
                writer.writerow({
                    'Category': category.value,
                    'Budget Limit': f'{limit:.2f}',
                    'Actual Expenses': f'{actual_expense:.2f}',
                    'Difference': f'{difference:.2f}',
                    'Status': status
                })
        
        return filepath

    @staticmethod
    def generate_comprehensive_report(
        expenses: List[Expense], 
        budget: Budget
    ):
        """
        Generate a comprehensive report with CSV exports and visualization
        
        Args:
            expenses (List[Expense]): List of expenses
            budget (Budget): Budget limits
        
        Returns:
            Dict[str, str]: Paths to generated files
        """
        # Calculate expenses by category
        expenses_by_category = {}
        for category in ExpenseCategory:
            expenses_by_category[category] = sum(
                exp.amount for exp in expenses if exp.category == category
            )
        
        # Export expenses CSV
        expenses_csv = DataExporter.export_expenses_to_csv(expenses)
        
        # Export budget CSV
        budget_csv = DataExporter.export_budget_to_csv(budget, expenses_by_category)
        
        # Generate pie chart
        chart_path = DataExporter.generate_expense_pie_chart(expenses_by_category)
        
        return {
            'expenses_csv': expenses_csv,
            'budget_csv': budget_csv,
            'chart_path': chart_path
        }

    @staticmethod
    def generate_expense_pie_chart(
        expenses_by_category: Dict[ExpenseCategory, float], 
        filename: str = 'expense_categories_chart.png'
    ):
        """
        Generate a pie chart of expenses by category
        
        Args:
            expenses_by_category (Dict[ExpenseCategory, float]): Expenses by category
            filename (str, optional): Name of the chart file. Defaults to 'expense_categories_chart.png'
        
        Returns:
            str: Path to the generated chart
        """
        # Ensure the 'reports' directory exists
        os.makedirs('reports', exist_ok=True)
        filepath = os.path.join('reports', filename)
        
        # Filter out categories with zero expenses
        filtered_expenses = {
            cat.value: amount 
            for cat, amount in expenses_by_category.items() 
            if amount > 0
        }
        
        # Create pie chart
        plt.figure(figsize=(10, 7))
        plt.pie(
            filtered_expenses.values(), 
            labels=[cat for cat in filtered_expenses.keys()], 
            autopct='%1.1f%%'
        )
        plt.title('Expenses by Category')
        plt.axis('equal')
        
        # Save the chart
        plt.savefig(filepath)
        plt.close()
        
        return filepath