from datetime import date
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query, Path, Body, status
from app.database import database
from app.models import Expense, ExpenseCreate, ExpenseUpdate, ExpenseSummary, PeriodSummary
from app.utils import parse_date, get_date_range


router = APIRouter()


@router.get("/", response_model=List[Expense])
async def get_expenses(
    category: Optional[str] = Query(None, description="Filter by category"),
    start_date: Optional[str] = Query(None, description="Filter by start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="Filter by end date (YYYY-MM-DD)"),
    min_amount: Optional[float] = Query(None, description="Filter by minimum amount"),
    max_amount: Optional[float] = Query(None, description="Filter by maximum amount")
):
    """Get all expenses with optional filtering."""
    expenses = database.get_all_expenses()
    
    # Apply filters if provided
    if category:
        expenses = [exp for exp in expenses if exp.category == category]
    
    if start_date and end_date:
        try:
            start = parse_date(start_date)
            end = parse_date(end_date)
            expenses = [exp for exp in expenses if start <= exp.date <= end]
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    if min_amount is not None and max_amount is not None:
        expenses = [exp for exp in expenses if min_amount <= exp.amount <= max_amount]
    elif min_amount is not None:
        expenses = [exp for exp in expenses if exp.amount >= min_amount]
    elif max_amount is not None:
        expenses = [exp for exp in expenses if exp.amount <= max_amount]
    
    return expenses


@router.get("/{expense_id}", response_model=Expense)
async def get_expense(expense_id: str = Path(..., description="The ID of the expense to get")):
    """Get a specific expense by ID."""
    expense = database.get_expense(expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


@router.post("/", response_model=Expense, status_code=status.HTTP_201_CREATED)
async def create_expense(expense: ExpenseCreate):
    """Create a new expense."""
    new_expense = Expense(
        amount=expense.amount,
        category=expense.category,
        description=expense.description,
        date=expense.date
    )
    created_expense = database.create_expense(new_expense)
    return created_expense


@router.put("/{expense_id}", response_model=Expense)
async def update_expense(
    expense_id: str = Path(..., description="The ID of the expense to update"),
    expense_data: ExpenseUpdate = Body(...)
):
    """Update an existing expense."""
    # Get the existing expense
    existing_expense = database.get_expense(expense_id)
    if not existing_expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    # Update only the provided fields
    update_data = expense_data.model_dump(exclude_unset=True)
    updated_expense = existing_expense.model_copy(update=update_data)
    
    # Save the updated expense
    result = database.update_expense(expense_id, updated_expense)
    if not result:
        raise HTTPException(status_code=500, detail="Failed to update expense")
    
    return result


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_expense(expense_id: str = Path(..., description="The ID of the expense to delete")):
    """Delete an expense."""
    success = database.delete_expense(expense_id)
    if not success:
        raise HTTPException(status_code=404, detail="Expense not found")


@router.get("/summary/categories", response_model=List[ExpenseSummary])
async def get_expense_summary():
    """Get a summary of expenses grouped by category."""
    return database.get_expense_summary()


@router.get("/summary/period", response_model=PeriodSummary)
async def get_period_summary(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    period: Optional[str] = Query(None, description="Predefined period (today, this_week, this_month, etc.)")
):
    """Get a summary of expenses for a specific period."""
    try:
        if period:
            # Use predefined period
            start, end = get_date_range(period)
        elif start_date and end_date:
            # Use custom date range
            start = parse_date(start_date)
            end = parse_date(end_date)
        else:
            # Default to current month
            today = date.today()
            start = today.replace(day=1)
            end = today
        
        return database.get_period_summary(start, end)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
