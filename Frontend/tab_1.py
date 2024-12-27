
API_URL = "http://127.0.0.1:8000"
import requests
import streamlit as st
from datetime import date
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# selected_date = st.date_input(
#         "Choose the date:",
#         min_value=date(2020, 1, 1),
#         max_value=date(2030, 1, 1),
#         label_visibility="collapsed",
#     )


def tab_1():

    import requests
    import streamlit as st
    from datetime import date
    import pandas as pd
    import matplotlib.pyplot as plt
    from datetime import datetime

    categories = {
        "Food": "🍔",
        "Healthcare": "💊",
        "Housing": "🏠",
        "Income": "💵",
        "Personal Care": "🧴",
        "Travel": "✈️",
    }

    st.markdown("**Choose the date**")
    selected_date = st.date_input(
        "Choose the date:",
        min_value=date(2020, 1, 1),
        max_value=date(2030, 1, 1),
        label_visibility="collapsed",
    )
    

    # Fetch existing expense

    def load_data():
        response = requests.get(f"{API_URL}/expenses/{selected_date}")
        if response.status_code == 200:
            
            existing_expenses = response.json()
                # If the response is None, return an empty list
            if existing_expenses is None:
                st.warning("No expenses data found.")
                return []
            return existing_expenses
            
            
        else:
            # Handle failed response
            st.error(f"Failed to fetch expenses. Status code: {response.status_code}")
            return []

    if f"expenses_{selected_date}" not in st.session_state:
        st.session_state[f"expenses_{selected_date}"] = load_data()

    # Initialize session state for rows and expenses
    expenses = st.session_state.get(f"expenses_{selected_date}", [])
    # st.write(expenses)
    # Display existing expenses
    #st.markdown("### Existing Expenses")
    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(
        [1.5, 2, 2, 1.5, 2, 2, 2, 2]
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
        st.markdown("**Note 📝**")
    with col7:
        st.markdown("**Delete**")
    with col8:
        st.markdown("**Update**")

    # Iterate over rows
    rows_to_delete = []
    rows_to_update = []
    for i, expense in enumerate(expenses):
        col1, col2, col3, col4, col5, col6, col7 = st.columns([1.5, 2, 2, 1.5, 2, 2, 2])

        with col1:
            name_options = ["Alice", "Bob", "Emily", "Mark"]
            name = st.selectbox(
                "Name",
                name_options,
                index=name_options.index(expense["user_name"]),
                key=f"name_{i}",
                label_visibility="collapsed",
            )

        with col2:
            category = st.selectbox(
                "Category",
                list(categories.values()),
                index=list(categories.keys()).index(expense["category"]),
                key=f"category_{i}",
                label_visibility="collapsed",
            )

        with col3:
            subcategory = st.text_input(
                "Subcategory",
                expense.get("subcategory", ""),
                key=f"subcategory_{i}",
                label_visibility="collapsed",
            )
        with col4:
            amount = st.number_input(
                "Amount",
                min_value=0.0,
                step=1.0,
                value=expense["amount"],
                key=f"amount_{i}",
                label_visibility="collapsed",
            )
        with col5:
            transaction_type = st.selectbox(
                "Type",
                ["Credit", "Debit"],
                index=["Credit", "Debit"].index(expense["transaction_type"]),
                key=f"type_{i}",
                label_visibility="collapsed",
            )
        with col6:
            notes = st.text_input(
                "Notes",
                expense.get("notes", ""),
                key=f"notes_{i}",
                label_visibility="collapsed",
            )
        with col7:
            delete_checkbox = st.checkbox(
                "Delete", key=f"delete_{i}", label_visibility="collapsed"
            )
            if delete_checkbox:
                rows_to_delete.append(expense["transaction_id"])

        with col8:
         
         button = st.button(f"Update {expense['transaction_id']}", key=f"update_{expense['transaction_id']}")

        # Check if the button is clicked
         if st.button(f"Update {expense['transaction_id']}"):
             updated_expense = {
                    "transaction_id": expense['transaction_id'],
                    "user_name": name,
                    "category": category,
                    "subcategory": subcategory,
                    "amount": amount,
                    "transaction_type": transaction_type,
                    "transaction_date": selected_date,
                    "notes": notes,
                }
             rows_to_update.append(updated_expense)
             st.write(f"Updated expense added: {updated_expense}")
    #st.write("Rows to update:", rows_to_update)


#


submit = st.toggle('Add new expense')
if submit:
    st.session_state["show_add_expense"] = True


# # Columns for inputs
col1, col2, col3, col4, col5, col6 = st.columns([1.5, 2, 2, 1.5, 2, 2])

# Input fields for new expense
with col1:
    new_name = st.selectbox("Name", [''] + ['Alice', 'Bob', 'Emily', 'Mark'], key="new_name")
with col2:
    new_category = st.selectbox("Category", [''] +  list(categories.keys()), key="new_category")
with col3:
    new_subcategory = st.text_input("Subcategory", key="new_subcategory")
with col4:
    new_amount = st.number_input("Amount", min_value=0.0, step=1.0, value=None, key="new_amount")
with col5:
    new_type = st.selectbox("Transaction Type", [''] + ["Credit", "Debit"], key="new_type")
with col6:
    new_notes = st.text_input("Notes", key="new_notes")

# Add new expense to the list when "Add Row" is pressed
    if st.button("Insert Row"):
        if new_name and new_category and new_amount > 0:  # Basic validation
             new_expense = {
            'user_name': new_name,
            'category': new_category,
            'subcategory': new_subcategory,
            'amount': new_amount,
            'transaction_type': new_type,
            'notes': new_notes,
        }
        # st.session_state["expenses"].append(new_expense)
        # st.success(f"Added expense: {new_expense}")
        # st.write(st.session_state["expenses"])
    if st.button("Add Another Row"):
    # Keep the form visible and reset the inputs for a new row
      st.session_state["show_add_expense"] = True

# Submit all expenses once the user is done adding rows
if st.button("Submit All Expenses"):
    if st.session_state["expenses"]:
        # Call your API or processing function here to submit all expenses
        response = requests.post("YOUR_API_URL", json=st.session_state["expenses"])
        if response.status_code == 200:
            st.success("All expenses submitted successfully!")
            st.session_state["expenses"] = []  # Clear the list after submission
        else:
            st.error(f"Failed to submit expenses: {response.text}")
    else:
        st.warning("No expenses to submit.")


# # Button to add multiple rows


#         # Clear inputs after adding


# # Display the temporary list of added expenses

# # Button to submit all added rows


#     # Validate inputs


    rows_to_delete = []
    if rows_to_delete and st.button("Delete Selected Rows"):
        response = requests.delete(
            f"{API_URL}/expenses/", json={"transaction_ids": rows_to_delete}
        )
        if response.status_code == 200:
            st.success("Selected expenses deleted successfully!")
            # Remove deleted rows from session state
            st.session_state[f"expenses_{selected_date}"] = [
                expense
                for expense in st.session_state[f"expenses_{selected_date}"]
                if expense["transaction_id"] not in rows_to_delete
            ]
            st.rerun()  # Refresh the page to reflect changes
        else:
            st.error(f"Failed to delete expenses. Error: {response.text}")

        # After deletion, re-render the page to reflect updated data
        st.session_state[f"expenses_{selected_date}"] = [
            expense
            for i, expense in enumerate(st.session_state[f"expenses_{selected_date}"])
            if i not in rows_to_delete
        ]


# if rows_to_update and st.button("Update Selected Rows"):

#     edit = requests.put(f"{API_URL}/expenses/update",json = rows_to_update)
#     if edit.status_code == 200:
#                 st.success(f"Expense {updated_expense['transaction_id']} updated successfully!")
#                 st.session_state[f"expenses_{selected_date}"] = [
#                     updated_expense if expense['transaction_id'] == updated_expense['transaction_id']
#                     else expense
#                     for expense in st.session_state[f"expenses_{selected_date}"]
#                 ]
#     else:
#                 st.error(f"Failed to update expense {updated_expense['transaction_id']}. Error: {response.text}")

#     st.session_state[f"expenses_{selected_date}"] = load_data()
#     st.rerun()
#     rows_to_update.clear()


# for edited in rows_to_update:


# # Clear the rows_to_update list after the update operation
#


# # Re-render the page to reflect the updated data
# st.rerun()  # Refresh the page to reflect changes

#         # Send delete request with transaction_ids in the request body



    






