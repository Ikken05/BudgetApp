import PySimpleGUI as sg
from datetime import datetime
from ..services.expense_service import ExpenseService
from ..models.expense import Expense, ExpenseCategory
from ..utils.validators import ExpenseValidator
from ..utils.data_analysis import ExpenseAnalyzer
from ..utils.data_export import DataExporter

class BudgetViewModel:
    def __init__(self, expense_service: ExpenseService):
        self.expense_service = expense_service
    
    def add_expense(self, date_str: str, category_str: str, amount_str: str, description: str):
        """Add a new expense with validation"""
        try:
            # Convert inputs
            expense_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            category = ExpenseCategory(category_str)
            amount = float(amount_str)
            
            # Validate inputs
            if not ExpenseValidator.validate_date(expense_date):
                raise ValueError("Date cannot be in the future")
            if not ExpenseValidator.validate_amount(amount):
                raise ValueError("Amount must be positive")
            
            # Create and add expense
            expense = Expense(
                date=expense_date,
                category=category,
                amount=amount,
                description=description
            )
            self.expense_service.add_expense(expense)
            return True, "Expense added successfully"
        
        except ValueError as e:
            return False, str(e)
    
    def get_expenses_summary(self):
        """Generate expenses summary"""
        total_expenses = self.expense_service.get_total_expenses()
        category_totals = self.expense_service.get_expenses_by_category()
        
        summary = "Expenses Summary:\n"
        for category, total in category_totals.items():
            summary += f"{category.value}: ${total:.2f}\n"
        summary += f"\nTotal Expenses: ${total_expenses:.2f}"
        
        return summary
    
    def generate_expense_chart(self):
        """Generate expense category pie chart"""
        category_totals = self.expense_service.get_expenses_by_category()
        ExpenseAnalyzer.generate_category_pie_chart(category_totals)
    
    def reset_expenses(self):
        """Reset all expenses"""
        self.expense_service.reset_expenses()
        return "All expenses have been reset."
    
    def reset_budget_limits(self):
        """Reset all budget limits"""
        self.expense_service.reset_budget_limits()
        return "All budget limits have been reset to zero."
    
    def generate_comprehensive_report(self):
        """
        Generate comprehensive report with CSV exports and chart
        
        Returns:
            Dict[str, str]: Paths to generated report files
        """
        # Get current expenses and budget
        expenses = self.expense_service.expenses
        budget = self.expense_service.budget
        
        # Generate report
        report_files = DataExporter.generate_comprehensive_report(
            expenses, 
            budget
        )
        
        # Prepare report message
        report_message = "Report Generated:\n"
        report_message += f"Expenses CSV: {report_files['expenses_csv']}\n"
        report_message += f"Budget CSV: {report_files['budget_csv']}\n"
        report_message += f"Expense Chart: {report_files['chart_path']}"
        
        return report_message