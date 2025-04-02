# Python Expense Tracking System

A comprehensive expense tracking application built with Python, FastAPI, and Streamlit that allows users to track, categorize, and analyze their daily expenses.

## Features

- **Track Daily Expenses**: Record your expenses with details like amount, category, and description
- **Categorize Expenses**: Organize expenses into predefined categories (Food, Transportation, Utilities, Shopping, EMI, etc.)
- **In-Memory Database**: Fast access to expense records via an in-memory database
- **RESTful API**: Backend built with FastAPI for CRUD operations and analysis
- **Streamlit Dashboard**: User-friendly interface to view expenses and spending trends
- **Data Visualization**: Charts and graphs to analyze spending patterns
- **Export/Import**: Export expense data to CSV/JSON or import from files

## Project Structure

```
expense-tracking-system/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── database.py          # In-memory database implementation
│   ├── models.py            # Data models/schemas
│   ├── utils.py             # Utility functions
│   └── api/
│       ├── __init__.py
│       └── endpoints/
│           ├── __init__.py
│           └── expenses.py   # API endpoints for expense operations
├── frontend/
│   └── app.py               # Streamlit application
├── requirements.txt         # Project dependencies
└── README.md                # Project documentation
```

## Getting Started

### Prerequisites

- Python 3.9+
- pip (Python package installer)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ArvindAkula/expense-tracking-system.git
   cd expense-tracking-system
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. Start the FastAPI backend:
   ```bash
   uvicorn app.main:app --reload
   ```
   The API will be available at http://localhost:8000
   
   You can access the interactive API documentation at http://localhost:8000/docs

2. Start the Streamlit frontend in a new terminal:
   ```bash
   streamlit run frontend/app.py
   ```
   The Streamlit interface will open automatically in your browser at http://localhost:8501

## API Endpoints

- `GET /expenses`: Get all expenses
- `GET /expenses/{expense_id}`: Get a specific expense
- `POST /expenses`: Create a new expense
- `PUT /expenses/{expense_id}`: Update an existing expense
- `DELETE /expenses/{expense_id}`: Delete an expense
- `GET /expenses/summary/categories`: Get expense summary by category
- `GET /expenses/summary/period`: Get expense summary for a specific period

## Usage Examples

### Adding a New Expense via API

```bash
curl -X 'POST' \
  'http://localhost:8000/expenses/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "amount": 25.50,
  "category": "Food",
  "description": "Lunch at restaurant",
  "date": "2025-04-01"
}'
```

## Key Python Features Used

- **Variables**: For storing expense amounts, categories, dates
- **Control Structures**: For handling expense categorization and looping through data
- **Functions**: Modularized code for adding, updating, deleting expenses
- **Data Structures**:
  - Lists & Dictionaries: Store multiple expense entries and their details
  - Tuples & Sets: Represent fixed expense data and manage unique categories
- **Functional Programming**:
  - map/filter: Used to filter expenses by criteria
  - reduce: For computing totals over various periods
- **OOP**: Class-based design for Expense objects and tracking functionality
- **Exception Handling**: For robust error handling in API operations
- **FastAPI**: Modern, high-performance web framework for building APIs
- **Streamlit**: For creating the interactive data visualization dashboard

## License

This project is licensed under the MIT License.
