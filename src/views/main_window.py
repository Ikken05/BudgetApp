import PySimpleGUI as sg
from datetime import date
from ..models.expense import ExpenseCategory
from ..viewmodels.budget_viewmodel import BudgetViewModel

class MainWindow:
    def __init__(self, view_model: BudgetViewModel):
        self.view_model = view_model
        self.layout = self._create_layout()
    
    def _create_layout(self):
        """Create PySimpleGUI layout"""
        categories = [category.value for category in ExpenseCategory]
        
        layout = [
            [sg.Text('Personal Budget Tracker', font=('Helvetica', 16))],
            
            # Expense Input Section
            [sg.Text('Add New Expense')],
            [
                sg.Text('Date:'), 
                sg.InputText(key='-DATE-', default_text=date.today().strftime('%Y-%m-%d'), size=(10,1)), 
                sg.CalendarButton('Choose Date', target='-DATE-', format='%Y-%m-%d')
            ],
            [
                sg.Text('Category:'), 
                sg.Combo(categories, key='-CATEGORY-', size=(15,1))
            ],
            [
                sg.Text('Amount:'), 
                sg.InputText(key='-AMOUNT-', size=(10,1))
            ],
            [
                sg.Text('Description:'), 
                sg.InputText(key='-DESCRIPTION-', size=(20,1))
            ],
            [sg.Button('Add Expense'), sg.Button('View Expenses')],
            
            # Budget Limits Section
            [sg.Text('Set Budget Limits')],
            *[
                [
                    sg.Text(f'{category} Limit:'), 
                    sg.InputText(key=f'-BUDGET-{category}-', size=(10,1))
                ] 
                for category in categories
            ],
            [sg.Button('Set Budget Limits')],
            
            # Reset Buttons
            [
                sg.Button('Reset Expenses', button_color=('white', 'red')), 
                sg.Button('Reset Budget Limits', button_color=('white', 'orange'))
            ],
            
            # Export and Analysis Section
            [
                sg.Button('Generate Pie Chart'),
                sg.Button('Generate Report', button_color=('white', 'green'))
            ],
            
            # Status Area
            [sg.Multiline(size=(50,5), key='-OUTPUT-', disabled=True)]
        ]
        
        return layout
    
    def run(self):
        """Run the main application window"""
        window = sg.Window('Budget Tracker', self.layout)
        
        while True:
            event, values = window.read()
            
            if event == sg.WINDOW_CLOSED:
                break
            
            try:
                if event == 'Add Expense':
                    success, message = self.view_model.add_expense(
                        values['-DATE-'],
                        values['-CATEGORY-'],
                        values['-AMOUNT-'],
                        values['-DESCRIPTION-']
                    )
                    window['-OUTPUT-'].update(message)
                
                elif event == 'View Expenses':
                    summary = self.view_model.get_expenses_summary()
                    window['-OUTPUT-'].update(summary)
                
                elif event == 'Set Budget Limits':
                    categories = list(ExpenseCategory)
                    for category in categories:
                        limit_key = f'-BUDGET-{category.value}-'
                        limit = values.get(limit_key, '0')
                        try:
                            self.view_model.expense_service.set_budget_limit(
                                category, 
                                float(limit) if limit else 0
                            )
                        except ValueError:
                            window['-OUTPUT-'].update(f'Invalid limit for {category.value}')
                    
                    # Check budget limits
                    budget_status = self.view_model.expense_service.check_budget_limits()
                    output = "Budget Limit Status:\n"
                    for category, exceeded in budget_status.items():
                        output += f"{category.value}: {'Exceeded' if exceeded else 'OK'}\n"
                    
                    window['-OUTPUT-'].update(output)
                
                elif event == 'Generate Pie Chart':
                    self.view_model.generate_expense_chart()
                    window['-OUTPUT-'].update('Pie chart generated as expense_categories_chart.png')
                
                elif event == 'Generate Report':
                    report_message = self.view_model.generate_comprehensive_report()
                    window['-OUTPUT-'].update(report_message)
                
                elif event == 'Reset Expenses':
                    message = self.view_model.reset_expenses()
                    window['-OUTPUT-'].update(message)
                
                elif event == 'Reset Budget Limits':
                    message = self.view_model.reset_budget_limits()
                    window['-OUTPUT-'].update(message)
            
            except Exception as e:
                window['-OUTPUT-'].update(f'Error: {str(e)}')
        
        window.close()