from datetime import datetime, date
from typing import Dict, List, Optional, Union
from uuid import uuid4
from functools import reduce

from app.models import Expense, ExpenseSummary, PeriodSummary


class InMemoryDatabase:
    """In-memory database for storing expense records."""
    
    def __init__(self):
        self.expenses: Dict[str, Expense] = {}
        
    def get_all_expenses(self) -> List[Expense]:
        """Get all expenses from the database."""
        return list(self.expenses.values())
    
    def get_expense(self, expense_id: str) -> Optional[Expense]:
        """Get a specific expense by ID."""
        return self.expenses.get(expense_id)
    
    def create_expense(self, expense: Expense) -> Expense:
        """Create a new expense record."""
        # Generate a UUID if not provided
        if not expense.id:
            expense.id = str(uuid4())
        
        # Set the current date if not provided
        if not expense.date:
            expense.date = date.today()
        
        # Store the expense in the database
        self.expenses[expense.id] = expense
        return expense
    
    def update_expense(self, expense_id: str, expense_data: Expense) -> Optional[Expense]:
        """Update an existing expense record."""
        if expense_id not in self.expenses:
            return None
        
        # Update the expense with new data while preserving the ID
        updated_expense = expense_data.copy(update={"id": expense_id})
        self.expenses[expense_id] = updated_expense
        return updated_expense
    
    def delete_expense(self, expense_id: str) -> bool:
        """Delete an expense record."""
        if expense_id in self.expenses:
            del self.expenses[expense_id]
            return True
        return False
    
    def get_expense_summary(self) -> List[ExpenseSummary]:
        """Get a summary of expenses grouped by category."""
        # Group expenses by category
        categories = {}
        for expense in self.expenses.values():
            if expense.category not in categories:
                categories[expense.category] = {
                    "category": expense.category,
                    "total": 0,
                    "count": 0
                }
            categories[expense.category]["total"] += expense.amount
            categories[expense.category]["count"] += 1
        
        # Convert to list of ExpenseSummary objects
        return [
            ExpenseSummary(
                category=data["category"],
                total_amount=data["total"],
                expense_count=data["count"]
            ) for data in categories.values()
        ]
    
    def get_period_summary(self, start_date: date, end_date: date) -> PeriodSummary:
        """Get a summary of expenses for a specific period."""
        # Filter expenses by date range
        filtered_expenses = list(filter(
            lambda exp: start_date <= exp.date <= end_date,
            self.expenses.values()
        ))
        
        # Calculate total amount using reduce
        total_amount = reduce(
            lambda acc, exp: acc + exp.amount,
            filtered_expenses,
            0.0
        )
        
        # Group by category
        categories = {}
        for expense in filtered_expenses:
            if expense.category not in categories:
                categories[expense.category] = 0
            categories[expense.category] += expense.amount
        
        # Create and return the period summary
        return PeriodSummary(
            start_date=start_date,
            end_date=end_date,
            total_amount=total_amount,
            total_expenses=len(filtered_expenses),
            category_breakdown=categories
        )
    
    def filter_expenses_by_category(self, category: str) -> List[Expense]:
        """Filter expenses by category."""
        return list(filter(
            lambda exp: exp.category == category,
            self.expenses.values()
        ))
    
    def filter_expenses_by_date_range(self, start_date: date, end_date: date) -> List[Expense]:
        """Filter expenses by date range."""
        return list(filter(
            lambda exp: start_date <= exp.date <= end_date,
            self.expenses.values()
        ))
    
    def filter_expenses_by_amount_range(self, min_amount: float, max_amount: float) -> List[Expense]:
        """Filter expenses by amount range."""
        return list(filter(
            lambda exp: min_amount <= exp.amount <= max_amount,
            self.expenses.values()
        ))


# Create a singleton instance of the database
database = InMemoryDatabase()


# Add some sample expenses for testing
def add_sample_expenses():
    """Add sample expenses to the database for testing."""
    sample_expenses = [
        Expense(
            amount=25.50,
            category="Food",
            description="Lunch at restaurant",
            date=date(2025, 4, 1)
        ),
        Expense(
            amount=35.00,
            category="Transportation",
            description="Uber ride",
            date=date(2025, 4, 1)
        ),
        Expense(
            amount=120.00,
            category="Utilities",
            description="Electricity bill",
            date=date(2025, 3, 28)
        ),
        Expense(
            amount=500.00,
            category="Shopping",
            description="New clothes",
            date=date(2025, 3, 25)
        ),
        Expense(
            amount=1200.00,
            category="EMI",
            description="Car loan payment",
            date=date(2025, 4, 1)
        ),
    ]
    
    for expense in sample_expenses:
        database.create_expense(expense)


# Add sample expenses when the module is imported
add_sample_expenses()
