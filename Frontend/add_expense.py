import requests
import streamlit as st
from datetime import date

API_URL = "http://127.0.0.1:8000"

class AddExpense:
    def __init__(self):
        self.categories = {
            "Food": "🍔",
            "Healthcare": "💊",
            "Housing": "🏠",
            "Income": "💵",
            "Personal Care": "🧴",
            "Travel": "✈️",
        }
        self.selected_date = date.today()
        self.expenses = []

    def load_data(self):
        response = requests.get(f"{API_URL}/expenses/{self.selected_date}")
        if response.status_code == 200:
            data = response.json()
            if data is None:
                st.warning("No expenses data found.")
                return []
            return data
        else:
            st.error(f"Failed to fetch expenses. Status code: {response.status_code}")
            return []

    def display_expenses(self):
        self.expenses = self.load_data()
        
        col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(
            [1.5, 2, 2, 1.5, 2, 2, 1, 1]
        )

        with col1:
            st.markdown("**Name 👤**")
        with col2:
            st.markdown("**Category 📦**")
        with col3:
            st.markdown("**Subcategory 📦**")
        with col4:
            st.markdown("**Amount 💰**")
        with col5:
            st.markdown("**Type 🔄**")
        with col6:
            st.markdown("**Note 🖍**")
        with col7:
            st.markdown("**Delete**")
        with col8:
            st.markdown("**Update**")

        rows_to_delete = []

        for i, expense in enumerate(self.expenses):
            col1, col2, col3, col4, col5, col6, col7, col8 = st.columns([1.5, 2, 2, 1.5, 2, 2, 1, 1])

            with col1:
                name = st.selectbox(
                    "Name",
                    ["Alice", "Bob", "Emily", "Mark"],
                    index=["Alice", "Bob", "Emily", "Mark"].index(expense["user_name"]),
                    key=f"name_{expense['transaction_id']}",
                    label_visibility="collapsed",
                )

            with col2:
                category = st.selectbox(
                    "Category",
                    list(self.categories.keys()),
                    index=list(self.categories.keys()).index(expense["category"]),
                    key=f"category_{expense['transaction_id']}",
                    label_visibility="collapsed",
                )

            with col3:
                subcategory = st.text_input(
                    "Subcategory",
                    expense.get("subcategory", ""),
                    key=f"subcategory_{expense['transaction_id']}",
                    label_visibility="collapsed",
                )

            with col4:
                amount = st.number_input(
                    "Amount",
                    min_value=0.0,
                    step=1.0,
                    value=expense["amount"],
                    key=f"amount_{expense['transaction_id']}",
                    label_visibility="collapsed",
                )

            with col5:
                transaction_type = st.selectbox(
                    "Type",
                    ["Credit", "Debit"],
                    index=["Credit", "Debit"].index(expense["transaction_type"]),
                    key=f"type_{expense['transaction_id']}",
                    label_visibility="collapsed",
                )

            with col6:
                notes = st.text_input(
                    "Notes",
                    expense.get("notes", ""),
                    key=f"notes_{expense['transaction_id']}",
                    label_visibility="collapsed",
                )

            with col7:
                delete_checkbox = st.checkbox("Delete", key=f"delete_{expense['transaction_id']}", label_visibility="collapsed")
                if delete_checkbox:
                    rows_to_delete.append(expense["transaction_id"])

            with col8:
                update_button = st.button(f"Update", key=f"update_{expense['transaction_id']}")
                updated_expense = {}
                if update_button:
                    updated_expense = {
                        "transaction_id": expense['transaction_id'],
                        "user_name": name,
                        "category": category,
                        "subcategory": subcategory,
                        "amount": amount,
                        "transaction_type": transaction_type,
                        "transaction_date": self.selected_date.strftime("%Y-%m-%d"),
                        "notes": notes,
                    }
                    self.handle_update(updated_expense)
                    #rows_to_update.append(updated_expense)
                    #st.write(rows_to_update)
                    #print(f"for update",rows_to_update)
        add_expense_button = st.button('Add new expense', key='add_expense')
        if("show_add_expense" not in st.session_state):
            st.session_state["show_add_expense"]=False
        if (add_expense_button or st.session_state["show_add_expense"]):
            st.session_state["show_add_expense"] = True
            self.add_select_box()
        self.handle_deletion(rows_to_delete)

    def add_select_box(self):
        # # Columns for inputs
        col1, col2, col3, col4, col5, col6 = st.columns([1.5, 2, 2, 1.5, 2, 2])

        # Input fields for new expense
        with col1:
            new_name = st.selectbox("Name", [''] + ['Alice', 'Bob', 'Emily', 'Mark'], key="new_name")
        with col2:
            new_category = st.selectbox("Category", [''] +  list(self.categories.keys()), key="new_category")
        with col3:
            new_subcategory = st.text_input("Subcategory", key="new_subcategory")
        with col4:
            new_amount = st.number_input("Amount", min_value=0.0, step=1.0, value=None, key="new_amount")
        with col5:
            new_type = st.selectbox("Transaction Type", [''] + ["Credit", "Debit"], key="new_type")
        with col6:
            new_notes = st.text_input("Notes", key="new_notes")
        insert_row_button = st.button("Insert Row")
        if insert_row_button and new_name and new_category and new_amount > 0:  # Basic validation
            new_expense = {
                'user_name': new_name,
                'category': new_category,
                'subcategory': new_subcategory,
                'amount': new_amount,
                'transaction_type': new_type,
                'notes': new_notes,
            }
            response = requests.post(f"{API_URL}/expenses/{self.selected_date}", json=new_expense)
            print(response)
            if response.status_code == 200:
                st.session_state["show_add_expense"] = False
                st.rerun()
            else:
                st.error("Failed to add new expense.")
                
    def handle_deletion(self, rows_to_delete):
        if rows_to_delete and st.button("Delete Selected Rows"):
            response = requests.delete(
                f"{API_URL}/expenses/", json={"transaction_ids": rows_to_delete}
            )
            if response.status_code == 200:
                st.success("Selected expenses deleted successfully!")
                st.session_state[f"expenses_{self.selected_date}"] = self.load_data()
                st.rerun()
            else:
                st.error(f"Failed to delete expenses. Error: {response.text}")

    def handle_update(self, data):
        if data:
            response = requests.put(f"{API_URL}/expenses/update", json=data)
            print(response)
            if response.status_code == 200:
                #st.success("Selected expenses updated successfully!")
                st.session_state[f"expenses_{self.selected_date}"] = self.load_data()
                st.rerun()
            else:
                st.error("Failed to update expenses.")

    def run(self):
        st.markdown("**Choose the date**")
        self.selected_date = st.date_input(
            "Choose the date:",
            min_value=date(2020, 1, 1),
            max_value=date.today(),
            label_visibility="collapsed",
        )
        self.display_expenses()

if __name__ == "__main__":
    app = AddExpense()
    app.run()
