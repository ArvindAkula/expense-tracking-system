from datetime import date, datetime, timedelta
from functools import reduce
from typing import Dict, List, Tuple
from collections import defaultdict

from app.models import Expense


def parse_date(date_str: str) -> date:
    """Parse a date string to a date object."""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError(f"Invalid date format: {date_str}. Expected format: YYYY-MM-DD")


def get_date_range(period: str) -> Tuple[date, date]:
    """Get start and end dates for a given period."""
    today = date.today()
    
    if period == "today":
        return today, today
    elif period == "yesterday":
        yesterday = today - timedelta(days=1)
        return yesterday, yesterday
    elif period == "this_week":
        start_of_week = today - timedelta(days=today.weekday())
        return start_of_week, today
    elif period == "last_week":
        end_of_last_week = today - timedelta(days=today.weekday() + 1)
        start_of_last_week = end_of_last_week - timedelta(days=6)
        return start_of_last_week, end_of_last_week
    elif period == "this_month":
        start_of_month = today.replace(day=1)
        return start_of_month, today
    elif period == "last_month":
        last_month_end = today.replace(day=1) - timedelta(days=1)
        last_month_start = last_month_end.replace(day=1)
        return last_month_start, last_month_end
    elif period == "this_year":
        start_of_year = today.replace(month=1, day=1)
        return start_of_year, today
    elif period == "last_year":
        last_year_end = today.replace(month=1, day=1) - timedelta(days=1)
        last_year_start = last_year_end.replace(month=1, day=1)
        return last_year_start, last_year_end
    else:
        raise ValueError(f"Invalid period: {period}")


def calculate_monthly_trend(expenses: List[Expense]) -> Dict[str, float]:
    """Calculate monthly expense trends."""
    monthly_totals = defaultdict(float)
    
    for expense in expenses:
        month_key = expense.date.strftime("%Y-%m")
        monthly_totals[month_key] += expense.amount
    
    # Sort by month
    return dict(sorted(monthly_totals.items()))


def calculate_category_percentages(expenses: List[Expense]) -> Dict[str, float]:
    """Calculate percentage of spending by category."""
    category_totals = defaultdict(float)
    total_spend = 0.0
    
    # Calculate total amount for each category
    for expense in expenses:
        category_totals[expense.category] += expense.amount
        total_spend += expense.amount
    
    # Calculate percentages
    if total_spend > 0:
        category_percentages = {category: (amount / total_spend) * 100 
                              for category, amount in category_totals.items()}
    else:
        category_percentages = {}
    
    return category_percentages


def export_expenses_to_dict(expenses: List[Expense]) -> List[Dict]:
    """Convert expense objects to dictionaries for export."""
    return [
        {
            "id": expense.id,
            "amount": expense.amount,
            "category": expense.category,
            "description": expense.description,
            "date": expense.date.isoformat() if expense.date else None,
            "created_at": expense.created_at.isoformat()
        }
        for expense in expenses
    ]
