from src.services.expense_service import ExpenseService
from src.services.data_persistence import JSONPersistence
from src.viewmodels.budget_viewmodel import BudgetViewModel
from src.views.main_window import MainWindow

def main():
    # Initialize dependencies
    persistence = JSONPersistence()
    expense_service = ExpenseService(persistence)
    view_model = BudgetViewModel(expense_service)
    main_window = MainWindow(view_model)
    
    # Run the application
    main_window.run()

if __name__ == '__main__':
    main()