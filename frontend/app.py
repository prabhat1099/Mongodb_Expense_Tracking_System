import streamlit as st
import requests
from datetime import date
import json

#BASE_URL = "http://localhost:8000"   # change to your deployed API

BASE_URL = "https://expense-tracking-app-33it.onrender.com"   # change to your deployed API


# ---------------------------------------------------------
# ADD EXPENSES TAB
# ---------------------------------------------------------
def add_expense_tab():
    st.header("Add Expenses")

    expense_date = st.date_input("Select Expense Date", max_value=date.today())

    # Dynamic list
    if "rows" not in st.session_state:
        st.session_state.rows = 1

    expenses = []
    invalid_inputs = False   # 🔥 Track errors

    for i in range(st.session_state.rows):
        st.subheader(f"Expense {i + 1}")

        amount = st.number_input(f"Amount {i+1}",min_value=0.0,key=f"amount_{i}"   )
        category = st.text_input(f"Category {i+1}",key=f"cat_{i}" )
        notes = st.text_input(f"Notes {i+1}", key=f"notes_{i}"   )  

        # 🔥 VALIDATION — if any empty → mark invalid
        if amount < 0 or category.strip() == "" or notes.strip() == "":
            invalid_inputs = True

        expenses.append({"amount": amount,"category": category,"notes": notes })
    
    if st.button("Add More Expense"):
        st.session_state.rows += 1
        st.rerun()

    # ---------------------------
    # SUBMIT WITH VALIDATION
    # ---------------------------
    if st.button("Submit"):
        if invalid_inputs:
            st.error("❌ All fields (Amount > 0, Category, Notes) are required.")
            return

        payload = expenses
        url = f"{BASE_URL}/expenses/{expense_date}"

        resp = requests.post(url, json=payload)

        if resp.status_code == 200:
            st.success(resp.text)
        else:
            st.error(resp.text)


# ---------------------------------------------------------
# VIEW EXPENSES TAB
# ---------------------------------------------------------
def view_expense_tab():
    st.header("View Expenses")

    expense_date = st.date_input("Select Date to Fetch", max_value=date.today())

    if st.button("Fetch Records"):
        url = f"{BASE_URL}/expenses/{expense_date}"
        resp = requests.get(url)

        data = resp.json()

        if isinstance(data, dict) and "message" in data:
            st.warning(data["message"])
            return

        st.table(data)



# ---------------------------------------------------------
# DELETE EXPENSES TAB
# ---------------------------------------------------------
def delete_expense_tab():
    st.header("Delete Expense")

    expense_date = st.date_input("Date",max_value=date.today())
    category = st.text_input("Category")
    amount = st.number_input("Amount", min_value=1)

    if st.button("Delete"):
        payload = {
            "expense_date": str(expense_date),
            "category": category,
            "amount": amount
        }

        resp = requests.delete(f"{BASE_URL}/expenses/delete", json=payload)

        if resp.status_code == 200:
            st.success(resp.json()["message"])
        else:
            st.error(resp.text)



# ---------------------------------------------------------
# MAIN APP
# ---------------------------------------------------------

st.title("Expense Tracking App")

tabs = st.tabs(["Add Expense", "View Expenses", "Delete Expense"])

with tabs[0]:
    add_expense_tab()

with tabs[1]:
    view_expense_tab()

with tabs[2]:
    delete_expense_tab()
