# # import requests
# # import streamlit as st
# # from datetime import date
# # import pandas as pd
# # import matplotlib.pyplot as plt
# # from datetime import datetime
# #
# #
# # #setting the page configuration as wide
# #
# # st.set_page_config(layout="wide")
# #
# # #Heading
# # st.markdown(
# #     """
# #     <style>
# #     .centered-title {
# #         text-align: center;
# #         font-size: 40px;
# #         font-family: Times New Roman;
# #     }
# #     </style>
# #     """,
# #     unsafe_allow_html=True,
# # )
# #
# # st.markdown('<div class="centered-title">Expense Tracker</div>', unsafe_allow_html=True)
# #
# # #local host url
# # API_URL = "http://127.0.0.1:8000"
# #
# #
# # tab1,tab2 = st.tabs(["add","whatever"])
# # categories = {
# #         "Food": "🍔",
# #         "Healthcare": "💊",
# #         "Housing": "🏠",
# #         "Income": "💵",
# #         "Personal Care": "🧴",
# #         "Travel": "✈️",
# #     }
# #
# # with tab1:
# #
# #     # Date input
# #     selected_date = st.date_input(
# #         "Add the date:",
# #         min_value=date(2020, 1, 1),
# #         max_value=date(2030, 1, 1),
# #         label_visibility="collapsed",
# #     )
# #
# #     # Fetch existing expenses
# #     response = requests.get(f"{API_URL}/expenses/{selected_date}")
# #     if response.status_code == 200:
# #         existing_expenses = response.json()
# #     else:
# #         st.error("Failed to fetch expenses")
# #         existing_expenses = []
# #
# #     # Initialize session state for rows and expenses
# #     if f"expenses_{selected_date}" not in st.session_state:
# #         st.session_state[f"expenses_{selected_date}"] = existing_expenses
# #
# #     expenses = st.session_state[f"expenses_{selected_date}"]
# #
# #     # Toggle button for showing/hiding the add expense form
# #     if "show_add_expense" not in st.session_state:
# #         st.session_state["show_add_expense"] = False
# #
# #     # Toggle button to show/hide the form
# #     if st.button("Add New Expense" if not st.session_state["show_add_expense"] else "Hide Form"):
# #         st.session_state["show_add_expense"] = not st.session_state["show_add_expense"]
# #
# #     # Show form only when toggled
# #     if st.session_state["show_add_expense"]:
# #         st.markdown("### Add New Expense")
# #         col1, col2, col3, col4, col5, col6 = st.columns([1.5, 2, 2, 1.5, 2, 2])
# #
# #         with col1:
# #             new_name = st.selectbox("Name 👤", ['Alice', 'Bob', 'Emily', 'Mark'], key="new_name")
# #         with col2:
# #             new_category = st.selectbox("Category 📦", list(categories.keys()), key="new_category")
# #         with col3:
# #             new_subcategory = st.text_input("Subcategory 📦", key="new_subcategory")
# #         with col4:
# #             new_amount = st.number_input("Amount 💰", min_value=0.0, step=1.0, key="new_amount")
# #         with col5:
# #             new_type = st.selectbox("Type 🔄", ["Credit", "Debit"], key="new_type")
# #         with col6:
# #             new_notes = st.text_input("Notes 📝", key="new_notes")
# #
# #         if st.button("Insert Row"):
# #             # Validate inputs
# #             if new_name and new_category and new_amount > 0:
# #                 new_expense = {
# #                     'user_name': new_name,
# #                     'category': new_category,
# #                     'subcategory': new_subcategory,
# #                     'amount': new_amount,
# #                     'transaction_type': new_type,
# #                     'notes': new_notes,
# #                 }
# #                 st.session_state[f"expenses_{selected_date}"].append(new_expense)
# #                 st.success("New expense added successfully!")
# #                 st.rerun()  # Re-render to reflect the new row
# #             else:
# #                 st.warning("Please fill in all required fields.")
# #
# #     # Display existing expenses
# #     st.markdown("### Existing Expenses")
# #     col1, col2, col3, col4, col5, col6, col7 = st.columns([1.5, 2, 2, 1.5, 2, 2, 1])
# #
# #     with col1:
# #         st.markdown("**Name 👤**")
# #     with col2:
# #         st.markdown("**Category 📦**")
# #     with col3:
# #         st.markdown("**Subcategory 📦**")
# #     with col4:
# #         st.markdown("**Amount 💰**")
# #     with col5:
# #         st.markdown("**Type 🔄**")
# #     with col6:
# #         st.markdown("**Note 📝**")
# #     with col7:
# #         st.markdown("**Delete**")
# #
# #     # Iterate over rows
# #     rows_to_delete = []
# #     for i, expense in enumerate(expenses):
# #         col1, col2, col3, col4, col5, col6, col7 = st.columns([1.5, 2, 2, 1.5, 2, 2, 1])
# #
# #         with col1:
# #             name_options = ['Alice', 'Bob', 'Emily', 'Mark']
# #             name = st.selectbox(
# #                 "Name",
# #                 name_options,
# #                 index=name_options.index(expense['user_name']) if expense['user_name'] in name_options else 0,
# #                 key=f"name_{i}",
# #                 label_visibility="collapsed",
# #             )
# #
# #         with col2:
# #             category = st.selectbox(
# #                 "Category",
# #                 list(categories.keys()),
# #                 index=list(categories.keys()).index(expense['category']) if expense['category'] in categories else 0,
# #                 key=f"category_{i}",
# #                 label_visibility="collapsed",
# #             )
# #
# #         with col3:
# #             subcategory = st.text_input(
# #                 "Subcategory",
# #                 expense.get('subcategory', ''),
# #                 key=f"subcategory_{i}",
# #                 label_visibility="collapsed",
# #             )
# #         with col4:
# #             amount = st.number_input(
# #                 "Amount",
# #                 min_value=0.0,
# #                 step=1.0,
# #                 value=expense['amount'],
# #                 key=f"amount_{i}",
# #                 label_visibility="collapsed",
# #             )
# #         with col5:
# #             transaction_type = st.selectbox(
# #                 "Type",
# #                 ["Credit", "Debit"],
# #                 index=["Credit", "Debit"].index(expense['transaction_type']),
# #                 key=f"type_{i}",
# #                 label_visibility="collapsed",
# #             )
# #         with col6:
# #             notes = st.text_input(
# #                 "Notes",
# #                 expense.get('notes', ''),
# #                 key=f"notes_{i}",
# #                 label_visibility="collapsed",
# #             )
# #         with col7:
# #             # Delete button to remove the row
# #             delete_checkbox = st.checkbox(f"Delete Row {i}", key=f"delete_{i}")
# #
# #             if delete_checkbox:
# #                 rows_to_delete.append(i)
# #                 st.write("for delete",rows_to_delete)
# #
# #
# #         if rows_to_delete:
# #             for i in sorted(rows_to_delete, reverse=True):
# #                 expense_to_delete = st.session_state[f"expenses_{selected_date}"][i]
# #
# #                 # Send the whole data for deletion (without transaction_id explicitly)
# #                 response = requests.delete(f"{API_URL}/expenses/{selected_date}/delete", json=expense_to_delete)
# #
# #                 # Check if the request was successful
# #                 if response.status_code == 200:
# #                     st.success(f"Expense deleted successfully!")
# #                     # Remove the expense from session state only after successful deletion
# #                     del st.session_state[f"expenses_{selected_date}"][i]
# #                 else:
# #                     st.error(f"Failed to delete expense. Error: {response.text}")
# #
# #             # After deleting, re-render the page to reflect updated list
# #             st.session_state[f"expenses_{selected_date}"] = [
# #                 expense for i, expense in enumerate(st.session_state[f"expenses_{selected_date}"])
# #                 if i not in rows_to_delete
# #             ]
# #             st.rerun()  # Re-render the page to show updated list after deletion
# #
# #             # After deletion, re-render the page to reflect updated data
# #         st.session_state[f"expenses_{selected_date}"] = [
# #             expense for i, expense in enumerate(st.session_state[f"expenses_{selected_date}"])
# #             if i not in rows_to_delete]
# #         # Re-render the page to show updated list after deletion
# #
# #         # Define the function to check for duplicates
# #     def is_duplicate(expense, existing_expenses):
# #         for existing_expense in existing_expenses:
# #             if (expense['user_name'] == existing_expense['user_name'] and
# #                     expense['category'] == existing_expense['category'] and
# #                     expense['subcategory'] == existing_expense['subcategory'] and
# #                     expense['amount'] == existing_expense['amount'] and
# #                     expense['transaction_type'] == existing_expense['transaction_type'] and
# #                     expense['notes'] == existing_expense['notes']):
# #                 return True
# #         return False
# #
# #
# #     # Filter new expenses to remove duplicates
# #     new_expenses = [expense for expense in expenses if not is_duplicate(expense, existing_expenses)]
# #     submit_button = st.button("Submit")
# #     if submit_button:
# #         # Filter out rows with invalid amounts (e.g., zero or negative)
# #         filtered_expenses = [expense for expense in new_expenses if expense['amount'] > 0]
# #         st.write("Filtered Expenses:", filtered_expenses)
# #
# #         # Send the data to the backend API if there are valid expenses
# #         if filtered_expenses:
# #             data_to_send = filtered_expenses
# #             response = requests.post(f"{API_URL}/expenses/{selected_date}", json=data_to_send)
# #
# #             # Check the response status
# #             if response.status_code == 200:
# #                 st.success("Expenses submitted successfully!")
# #             else:
# #                 st.error(f"Failed to submit expenses. Error: {response.text}")
# #         else:
# #             st.warning("No valid expenses to submit.")
# #
# #     # Handle deletion of rows from session state and backend
# #
# #     # Update the session state after deletion
# #
# #     # Handle the submission of filtered expenses
# import requests
# import streamlit as st
# from datetime import date
#
# # API URL for the backend
# API_URL = "http://127.0.0.1:8000"
#
# # Define categories
# categories = {
#     "Food": "🍔",
#     "Healthcare": "💊",
#     "Housing": "🏠",
#     "Income": "💵",
#     "Personal Care": "🧴",
#     "Travel": "✈️",
# }
#
# # Initialize the tab for the page
# tab = st.selectbox("Choose a Tab", ["Add/Update Expense", "Analytics by category", "Dashboard"], label_visibility="collapsed")
#
# # Add/Update Expense tab functionality
# if tab == "Add/Update Expense":
#     # Date input for selecting date
#     st.markdown("**Choose the date**")
#     selected_date = st.date_input("Choose the date:", min_value=date(2020, 1, 1), max_value=date(2030, 1, 1), label_visibility="collapsed")
#
#     # Fetch existing expenses for the selected date
#     response = requests.get(f"{API_URL}/expenses/{selected_date}")
#     if response.status_code == 200:
#         existing_expenses = response.json()
#     else:
#         st.error("Failed to fetch expenses")
#         existing_expenses = []
#
#     # Initialize session state for rows and expenses
#     if f"expenses_{selected_date}" not in st.session_state:
#         st.session_state[f"expenses_{selected_date}"] = existing_expenses
#
#     expenses = st.session_state[f"expenses_{selected_date}"]
#
#     # Toggle button to show/hide the add expense form
#     if "show_add_expense" not in st.session_state:
#         st.session_state["show_add_expense"] = False
#
#     toggle_button_label = "Hide Form" if st.session_state["show_add_expense"] else "Add New Expense"
#     if st.button(toggle_button_label):
#         st.session_state["show_add_expense"] = not st.session_state["show_add_expense"]
#
#     # Show form only when toggled
#     if st.session_state["show_add_expense"]:
#         # Initialize rows to add
#         if "rows_to_add" not in st.session_state:
#             st.session_state["rows_to_add"] = [{
#                 'user_name': '',
#                 'category': '',
#                 'subcategory': '',
#                 'amount': 0.0,
#                 'transaction_type': '',
#                 'notes': ''
#             }]
#
#         # Function to add a new row
#         def add_row():
#             new_row = {
#                 'user_name': '',
#                 'category': '',
#                 'subcategory': '',
#                 'amount': 0.0,
#                 'transaction_type': '',
#                 'notes': ''
#             }
#             st.session_state["rows_to_add"].append(new_row)
#
#         # Function to delete a row
#         def delete_row(index):
#             del st.session_state["rows_to_add"][index]
#
#         # Display all rows dynamically
#         for i, row in enumerate(st.session_state["rows_to_add"]):
#             col1, col2, col3, col4, col5, col6, col7 = st.columns([1.5, 2, 2, 1.5, 2, 2, 1])
#
#             with col1:
#                 row['user_name'] = st.selectbox(f"Name_{i}", [''] + ['Alice', 'Bob', 'Emily', 'Mark'], index=0 if row['user_name'] == '' else ['Alice', 'Bob', 'Emily', 'Mark'].index(row['user_name']), key=f"user_name_{i}")
#             with col2:
#                 row['category'] = st.selectbox(f"Category_{i}", list(categories.keys()), index=0 if row['category'] == '' else list(categories.keys()).index(row['category']), key=f"category_{i}")
#             with col3:
#                 row['subcategory'] = st.text_input(f"Subcategory_{i}", value=row['subcategory'], key=f"subcategory_{i}")
#             with col4:
#                 row['amount'] = st.number_input(f"Amount_{i}", value=row['amount'], min_value=0.0, step=1.0, key=f"amount_{i}")
#             with col5:
#                 row['transaction_type'] = st.selectbox(f"Type_{i}", ["", "Credit", "Debit"], index=0 if row['transaction_type'] == '' else ["", "Credit", "Debit"].index(row['transaction_type']), key=f"type_{i}")
#             with col6:
#                 row['notes'] = st.text_input(f"Notes_{i}", value=row['notes'], key=f"notes_{i}")
#
#             with col7:
#                 # Delete Button for the row
#                 if st.button(f"Delete Row_{i}", key=f"delete_{i}"):
#                     delete_row(i)
#
#         # Add Row Button
#         if st.button("Add Row"):
#             add_row()
#
#         # Submit All Data
#         if st.button("Submit All Expenses"):
#             # Validate inputs (ensure all rows have valid data)
#             if all(row['user_name'] and row['category'] and row['amount'] > 0 for row in st.session_state["rows_to_add"]):
#                 response = requests.post(f"{API_URL}/expenses/{selected_date}", json=st.session_state["rows_to_add"])
#                 if response.status_code == 200:
#                     st.success("Expenses submitted successfully!")
#                     st.session_state[f"expenses_{selected_date}"].extend(st.session_state["rows_to_add"])  # Add to existing data
#                     st.session_state["rows_to_add"] = []  # Clear rows after submission
#                     st.rerun()  # Refresh the page
#                 else:
#                     st.error("Failed to submit expenses.")
#             else:
#                 st.error("Please fill in all rows properly before submitting.")
import streamlit as st
import requests
from datetime import date

# Add custom CSS for background image and styling
st.markdown(
    """
    <style>
    .container {
        position: relative;
        text-align: center;
        color: black;
    }
    .centered-title {
        font-size: 60px;
        font-family: 'Times New Roman', serif;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
    }
    .background-image {
        width: 100%;
        height: 100vh;  /* This ensures the image takes full height of the viewport */
        object-fit: cover;  /* Ensures the image covers the entire area without distortion */
        opacity: 0.1;  /* Optional: make the image semi-transparent */
        position: absolute;
        top: 0;
        left: 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Add background image
st.markdown('<div class="container"><img src="https://happay.com/blog/wp-content/uploads/sites/12/2022/08/non-operating-expenses.png" alt="Expense Tracker Background" class="background-image"><div class="centered-title">Expense Tracker</div></div>', unsafe_allow_html=True)

# Localhost URL for API
API_URL = "http://127.0.0.1:8000"

# Tab selection
st.markdown("*Current tab*")
tab = st.selectbox("Choose a Tab", ["Add/Update Expense", "Analytics by category", "Dashboard"], label_visibility="collapsed")

categories = {
    "Food": "🍔",
    "Healthcare": "💊",
    "Housing": "🏠",
    "Income": "💵",
    "Personal Care": "🧴",
    "Travel": "✈️",
}

if tab == "Add/Update Expense":
    # Date input
    st.markdown("**Choose the date**")
    selected_date = st.date_input(
        "Choose the date:",
        min_value=date(2020, 1, 1),
        max_value=date(2030, 1, 1),
        label_visibility="collapsed"
    )

    # Fetch existing expenses
    response = requests.get(f"{API_URL}/expenses/{selected_date}")
    if response.status_code == 200:
        existing_expenses = response.json()
    else:
        st.error("Failed to fetch expenses")
        existing_expenses = []

    # Initialize session state for rows and expenses
    if f"expenses_{selected_date}" not in st.session_state:
        st.session_state[f"expenses_{selected_date}"] = existing_expenses

    expenses = st.session_state[f"expenses_{selected_date}"]

    # Toggle button for showing/hiding the add expense form
    if "show_add_expense" not in st.session_state:
        st.session_state["show_add_expense"] = False

    toggle_button_label = "Hide Form" if st.session_state["show_add_expense"] else "Add New Expense"
    if st.button(toggle_button_label):
        st.session_state["show_add_expense"] = not st.session_state["show_add_expense"]

    # Show form only when toggled
    if st.session_state["show_add_expense"]:
        # Initialize a list of expenses to be added (if not already)
        if "new_expenses" not in st.session_state:
            st.session_state["new_expenses"] = []

        # Add row button
        if st.button("Add Row"):
            st.session_state["new_expenses"].append({
                'user_name': '',
                'category': '',
                'subcategory': '',
                'amount': 0.0,
                'transaction_type': '',
                'notes': '',
            })

        # Display the expenses form dynamically
        for i, expense in enumerate(st.session_state["new_expenses"]):
            col1, col2, col3, col4, col5, col6, col7 = st.columns([1.5, 2, 2, 1.5, 2, 2, 1])

            with col1:
                new_name = st.selectbox("", [''] + ['Alice', 'Bob', 'Emily', 'Mark'], index=0, key=f"name_{i}")
            with col2:
                new_category = st.selectbox("", [''] + list(categories.keys()), index=0, key=f"category_{i}")
            with col3:
                new_subcategory = st.text_input("", key=f"subcategory_{i}")
            with col4:
                new_amount = st.number_input("", min_value=0.0, step=1.0, value=expense['amount'], key=f"amount_{i}")
            with col5:
                new_type = st.selectbox("", [''] + ["Credit", "Debit"], index=0, key=f"type_{i}")
            with col6:
                new_notes = st.text_input("", key=f"notes_{i}")
            with col7:
                delete_button = st.button(f"Delete Row {i+1}", key=f"delete_{i}")
                if delete_button:
                    st.session_state["new_expenses"].pop(i)
                    st.experimental_rerun()  # Refresh after deletion

        # Submit button
        if st.button("Submit All"):
            # Collect all new expenses to send to the API
            new_expenses = []
            for i, expense in enumerate(st.session_state["new_expenses"]):
                if expense['user_name'] and expense['category'] and expense['amount'] > 0:
                    new_expenses.append(expense)

            if new_expenses:
                # Send the new expenses to the API
                response = requests.post(f"{API_URL}/expenses/{selected_date}", json=new_expenses)

                if response.status_code == 200:
                    st.success("Expenses submitted successfully!")
                    # Update session state with the new expenses
                    st.session_state[f"expenses_{selected_date}"].extend(new_expenses)
                    st.session_state["new_expenses"] = []  # Clear the list after submission
                    st.experimental_rerun()  # Refresh the page to reflect new expenses
                else:
                    st.error(f"Failed to submit expenses. Error: {response.text}")
            else:
                st.warning("No valid expenses to submit.")

    # Display existing expenses
    col1, col2, col3, col4, col5, col6, col7 = st.columns([1.5, 2, 2, 1.5, 2, 2, 1])

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

    # Iterate over rows for displaying existing expenses
    rows_to_delete = []
    for i, expense in enumerate(expenses):
        col1, col2, col3, col4, col5, col6, col7 = st.columns([1.5, 2, 2, 1.5, 2, 2, 1])

        with col1:
            name_options = ['Alice', 'Bob', 'Emily', 'Mark']
            name = st.selectbox(
                "Name",
                name_options,
                index=name_options.index(expense['user_name']) if expense['user_name'] in name_options else 0,
                key=f"name_{i}",
                label_visibility="collapsed",
            )

        with col2:
            category = st.selectbox(
                "Category",
                list(categories.keys()),
                index=list(categories.keys()).index(expense['category']) if expense['category'] in categories else 0,
                key=f"category_{i}",
                label_visibility="collapsed",
            )

        with col3:
            subcategory = st.text_input(
                "Subcategory",
                expense.get('subcategory', ''),
                key=f"subcategory_{i}",
                label_visibility="collapsed",
            )
        with col4:
            amount = st.number_input(
                "Amount",
                min_value=0.0,
                step=1.0,
                value=expense['amount'],
                key=f"amount_{i}",
                label_visibility="collapsed",
            )
        with col5:
            transaction_type = st.selectbox(
                "Type",
                ["Credit", "Debit"],
                index=["Credit", "Debit"].index(expense['transaction_type']),
                key=f"type_{i}",
                label_visibility="collapsed",
            )
        with col6:
            notes = st.text_input(
                "Notes",
                expense.get('notes', ''),
                key=f"notes_{i}",
                label_visibility="collapsed",
            )
        with col7:
            delete_checkbox = st.checkbox(f"", key=f"delete_{i}")
            if delete_checkbox:
                rows_to_delete.append(expense['transaction_id'])

    # Delete selected expenses
    if rows_to_delete and st.button("Delete Selected Rows"):
        response = requests.delete(f"{API_URL}/expenses/{selected_date}/delete", json={"transaction_id": rows_to_delete})
        if response.status_code == 200:
            st.success("Selected expenses deleted successfully!")
            # Remove deleted rows from session state
            st.session_state[f"expenses_{selected_date}"] = [
                expense for expense in st.session_state[f"expenses_{selected_date}"]
                if expense['transaction_id'] not in rows_to_delete
            ]
            st.rerun()  # Refresh the page to reflect changes
        else:
            st.error(f"Failed to delete expenses. Error: {response.text}")
