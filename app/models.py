from datetime import date as date_type, datetime
from enum import Enum
from typing import Dict, List, Optional, Union
from pydantic import BaseModel, Field
from uuid import uuid4


class ExpenseCategory(str, Enum):
    """Enumeration of expense categories."""
    FOOD = "Food"
    TRANSPORTATION = "Transportation"
    UTILITIES = "Utilities"
    SHOPPING = "Shopping"
    EMI = "EMI"
    ENTERTAINMENT = "Entertainment"
    HEALTHCARE = "Healthcare"
    EDUCATION = "Education"
    OTHER = "Other"


class Expense(BaseModel):
    """Model for an expense record."""
    id: Optional[str] = Field(default_factory=lambda: str(uuid4()))
    amount: float = Field(gt=0, description="Expense amount")
    category: str = Field(description="Expense category")
    description: Optional[str] = Field(default=None, description="Expense description")
    date: Optional[date_type] = Field(default_factory=date_type.today, description="Expense date")
    created_at: datetime = Field(default_factory=datetime.now, description="Record creation timestamp")


class ExpenseCreate(BaseModel):
    """Model for creating a new expense."""
    amount: float = Field(gt=0, description="Expense amount")
    category: str = Field(description="Expense category")
    description: Optional[str] = Field(default=None, description="Expense description")
    date: Optional[date_type] = Field(default=None, description="Expense date")


class ExpenseUpdate(BaseModel):
    """Model for updating an existing expense."""
    amount: Optional[float] = Field(default=None, gt=0, description="Expense amount")
    category: Optional[str] = Field(default=None, description="Expense category")
    description: Optional[str] = Field(default=None, description="Expense description")
    date: Optional[date_type] = Field(default=None, description="Expense date")


class ExpenseSummary(BaseModel):
    """Model for expense summary by category."""
    category: str
    total_amount: float
    expense_count: int


class PeriodSummary(BaseModel):
    """Model for expense summary over a period."""
    start_date: date_type
    end_date: date_type
    total_amount: float
    total_expenses: int
    category_breakdown: Dict[str, float]
