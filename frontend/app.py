import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
import json
from datetime import datetime, timedelta, date
import requests

# API base URL
API_URL = "http://localhost:8888"  # Updated to the new port

# Set page config
st.set_page_config(page_title="Expense Tracker", page_icon="💰", layout="wide")

# Page title
st.title("💰 Expense Tracking System")

# Function to format currency
def format_currency(value):
    return f"${value:.2f}"

# Function to fetch data from API
def fetch_expenses():
    try:
        response = requests.get(f"{API_URL}/expenses/", timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error fetching expenses: {response.text}")
            return []
    except requests.exceptions.ConnectionError:
        st.error(f"Cannot connect to the backend server at {API_URL}. Please make sure it's running.")
        return []
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
        return []

# Function to fetch category summary
def fetch_category_summary():
    try:
        response = requests.get(f"{API_URL}/expenses/summary/categories", timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error fetching category summary: {response.text}")
            return []
    except requests.exceptions.ConnectionError:
        st.error(f"Cannot connect to the backend server at {API_URL}. Please make sure it's running.")
        return []
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
        return []

# Function to fetch period summary
def fetch_period_summary(period=None, start_date=None, end_date=None):
    params = {}
    if period:
        params["period"] = period
    if start_date:
        params["start_date"] = start_date.strftime("%Y-%m-%d")
    if end_date:
        params["end_date"] = end_date.strftime("%Y-%m-%d")
    
    try:
        response = requests.get(f"{API_URL}/expenses/summary/period", params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error fetching period summary: {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        st.error(f"Cannot connect to the backend server at {API_URL}. Please make sure it's running.")
        return None
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
        return None

# Function to add an expense
def add_expense(expense_data):
    try:
        response = requests.post(f"{API_URL}/expenses/", json=expense_data, timeout=10)
        if response.status_code == 201:
            st.success("Expense added successfully!")
            return response.json()
        else:
            st.error(f"Error adding expense: {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        st.error(f"Cannot connect to the backend server at {API_URL}. Please make sure it's running.")
        return None
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
        return None

# Function to delete an expense
def delete_expense(expense_id):
    try:
        response = requests.delete(f"{API_URL}/expenses/{expense_id}", timeout=10)
        if response.status_code == 204:
            st.success("Expense deleted successfully!")
            return True
        else:
            st.error(f"Error deleting expense: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        st.error(f"Cannot connect to the backend server at {API_URL}. Please make sure it's running.")
        return False
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
        return False

# Create tabs
tab1, tab2, tab3 = st.tabs(["📝 Expenses", "📊 Dashboard", "➕ Add Expense"])

# Tab 1: Expenses List
with tab1:
    st.subheader("Expense Records")
    
    # Fetch expenses and create DataFrame
    expenses = fetch_expenses()
    if expenses:
        df = pd.DataFrame(expenses)
        
        # Convert date strings to datetime
        df["date"] = pd.to_datetime(df["date"]).dt.date
        
        # Add formatted amount column
        df["formatted_amount"] = df["amount"].apply(format_currency)
        
        # Sort by date (newest first)
        df = df.sort_values(by="date", ascending=False)
        
        # Display expenses table
        st.dataframe(
            df[["date", "category", "description", "formatted_amount"]].rename(
                columns={"formatted_amount": "amount"}
            ),
            hide_index=True,
            column_config={
                "date": st.column_config.DateColumn("Date"),
                "category": st.column_config.TextColumn("Category"),
                "description": st.column_config.TextColumn("Description"),
                "amount": st.column_config.TextColumn("Amount")
            },
            use_container_width=True
        )
        
        # Create a form for deletion
        with st.form("delete_expense_form"):
            st.subheader("Delete an Expense")
            expense_id = st.selectbox(
                "Select Expense to Delete",
                options=df["id"].tolist(),
                format_func=lambda x: f"{df[df['id'] == x]['date'].iloc[0]} - {df[df['id'] == x]['category'].iloc[0]} - {df[df['id'] == x]['formatted_amount'].iloc[0]}"
            )
            
            submit_delete = st.form_submit_button("Delete Selected Expense")
            
            if submit_delete:
                if delete_expense(expense_id):
                    st.rerun()
    else:
        st.info("No expenses found. Add some expenses to get started!")

# Tab 2: Dashboard
with tab2:
    st.subheader("Expense Analytics Dashboard")
    
    # Date range selection
    col1, col2 = st.columns(2)
    with col1:
        period_options = {
            "today": "Today",
            "yesterday": "Yesterday",
            "this_week": "This Week",
            "last_week": "Last Week",
            "this_month": "This Month",
            "last_month": "Last Month",
            "this_year": "This Year",
            "last_year": "Last Year",
            "custom": "Custom Range"
        }
        selected_period = st.selectbox("Select Time Period", options=list(period_options.keys()), format_func=lambda x: period_options[x])
    
    # Show custom date inputs if custom period selected
    if selected_period == "custom":
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", value=date.today() - timedelta(days=30))
        with col2:
            end_date = st.date_input("End Date", value=date.today())
        
        # Fetch period summary with custom dates
        period_summary = fetch_period_summary(start_date=start_date, end_date=end_date)
    else:
        # Fetch period summary with predefined period
        period_summary = fetch_period_summary(period=selected_period)
    
    if period_summary:
        # Display summary cards
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Expenses", f"{period_summary['total_expenses']} items")
        with col2:
            st.metric("Total Amount", format_currency(period_summary['total_amount']))
        with col3:
            avg_per_expense = period_summary['total_amount'] / period_summary['total_expenses'] if period_summary['total_expenses'] > 0 else 0
            st.metric("Average per Expense", format_currency(avg_per_expense))
        
        # Category breakdown chart
        st.subheader("Expense Distribution by Category")
        
        if period_summary['category_breakdown']:
            # Prepare data for chart
            categories_df = pd.DataFrame({
                "Category": list(period_summary['category_breakdown'].keys()),
                "Amount": list(period_summary['category_breakdown'].values())
            })
            
            # Sort by amount (highest first)
            categories_df = categories_df.sort_values(by="Amount", ascending=False)
            
            # Calculate percentage
            total = categories_df["Amount"].sum()
            categories_df["Percentage"] = (categories_df["Amount"] / total * 100).round(1)
            categories_df["Label"] = categories_df.apply(lambda row: f"{row['Category']}: {format_currency(row['Amount'])} ({row['Percentage']}%)", axis=1)
            
            # Create pie chart
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.pie(categories_df["Amount"], labels=categories_df["Label"], autopct="", startangle=90)
            ax.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle
            plt.title("Expense Distribution by Category")
            st.pyplot(fig)
            
            # Display breakdown table
            st.subheader("Category Breakdown")
            categories_df["Amount"] = categories_df["Amount"].apply(format_currency)
            categories_df["Percentage"] = categories_df["Percentage"].apply(lambda x: f"{x}%")
            st.dataframe(
                categories_df[["Category", "Amount", "Percentage"]],
                hide_index=True,
                use_container_width=True
            )
        else:
            st.info("No expenses found in the selected period.")
    else:
        st.warning("Unable to load expense summary. Make sure the API is running.")
    
    # Fetch all expenses for trend analysis
    all_expenses = fetch_expenses()
    if all_expenses:
        df = pd.DataFrame(all_expenses)
        df["date"] = pd.to_datetime(df["date"])
        
        # Monthly trend chart
        st.subheader("Monthly Expense Trend")
        
        # Group by month and sum amounts
        df["month"] = df["date"].dt.to_period("M")
        monthly_data = df.groupby("month")["amount"].sum().reset_index()
        monthly_data["month_str"] = monthly_data["month"].astype(str)
        
        # Create bar chart
        monthly_chart = alt.Chart(monthly_data).mark_bar().encode(
            x=alt.X("month_str:O", title="Month", sort=None),
            y=alt.Y("amount:Q", title="Total Amount ($)"),
            tooltip=[alt.Tooltip("month_str:O", title="Month"), alt.Tooltip("amount:Q", title="Total", format="$.2f")]
        ).properties(
            title="Monthly Expense Trend",
            width="container"
        )
        
        st.altair_chart(monthly_chart, use_container_width=True)

# Tab 3: Add Expense
with tab3:
    st.subheader("Add New Expense")
    
    with st.form("add_expense_form"):
        # Date field
        expense_date = st.date_input("Date", value=date.today())
        
        # Category and amount in same row
        col1, col2 = st.columns(2)
        with col1:
            # Category dropdown
            category_options = [
                "Food", "Transportation", "Utilities", "Shopping", "EMI", 
                "Entertainment", "Healthcare", "Education", "Other"
            ]
            expense_category = st.selectbox("Category", options=category_options)
        
        with col2:
            # Amount field
            expense_amount = st.number_input("Amount ($)", min_value=0.01, step=0.01, format="%.2f")
        
        # Description field
        expense_description = st.text_area("Description (Optional)", height=100)
        
        # Submit button
        submit_button = st.form_submit_button("Add Expense")
        
        if submit_button:
            # Prepare expense data
            expense_data = {
                "amount": expense_amount,
                "category": expense_category,
                "description": expense_description,
                "date": expense_date.isoformat()
            }
            
            # Add expense
            if add_expense(expense_data):
                # Clear form (by forcing a rerun)
                st.rerun()

# Add info about the application
st.sidebar.title("About")
st.sidebar.info("This Expense Tracking System helps you track, categorize, and analyze your daily expenses.")

# Add export options
st.sidebar.title("Export Data")
if st.sidebar.button("Export to CSV"):
    expenses = fetch_expenses()
    if expenses:
        df = pd.DataFrame(expenses)
        # Convert to CSV
        csv = df.to_csv(index=False)
        # Create download button
        st.sidebar.download_button(
            label="Download CSV",
            data=csv,
            file_name="expenses.csv",
            mime="text/csv"
        )
    else:
        st.sidebar.error("No expenses to export.")

# Show API status
try:
    response = requests.get(f"{API_URL}/", timeout=5)
    if response.status_code == 200:
        st.sidebar.success("✅ API is running")
    else:
        st.sidebar.error("❌ API is not responding correctly")
except requests.exceptions.ConnectionError:
    st.sidebar.error("❌ API is not running. Start the backend server.")
except Exception as e:
    st.sidebar.error(f"Error checking API status: {str(e)}")
