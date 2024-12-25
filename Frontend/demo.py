# # # # # # import requests
# # # # # # import streamlit as st
# # # # # # from datetime import date
# # # # # # import pandas as pd
# # # # # # import matplotlib.pyplot as plt
# # # # # # from datetime import datetime
# # # # # # from functools import partial
# # # # # #
# # # # # # # Setting the page configuration as wide
# # # # # # st.set_page_config(layout="wide")
# # # # # #
# # # # # # # Heading
# # # # # # st.markdown(
# # # # # #     """
# # # # # #     <style>
# # # # # #     .centered-title {
# # # # # #         text-align: center;
# # # # # #         font-size: 40px;
# # # # # #         font-family: Times New Roman;
# # # # # #     }
# # # # # #     </style>
# # # # # #     """,
# # # # # #     unsafe_allow_html=True,
# # # # # # )
# # # # # # st.markdown('<div class="centered-title">Expense Tracker</div>', unsafe_allow_html=True)
# # # # # #
# # # # # # # API URL placeholder
# # # # # # API_URL = "http://127.0.0.1:8000"
# # # # # #
# # # # # # # Tabs
# # # # # # tab1, tab2, tab3 = st.tabs(["Add/Update", "Analytics by category", "Analytics by month"])
# # # # # #
# # # # # # with tab1:
# # # # # #     # Date input
# # # # # #     selected_date = st.date_input(
# # # # # #         "Add the date:",
# # # # # #         min_value=date(2020, 1, 1),
# # # # # #         max_value=date(2030, 1, 1),
# # # # # #         label_visibility="collapsed",
# # # # # #     )
# # # # # #
# # # # # #     # Fetch existing expenses
# # # # # #     response = requests.get(f"{API_URL}/expenses/{selected_date}")
# # # # # #     if response.status_code == 200:
# # # # # #         existing_expenses = response.json()
# # # # # #     else:
# # # # # #         st.error("Failed to fetch expenses")
# # # # # #         existing_expenses = []
# # # # # #
# # # # # #     # Define categories
# # # # # #     categories = {
# # # # # #         "Food": "🍔",
# # # # # #         "Healthcare": "💊",
# # # # # #         "Housing": "🏠",
# # # # # #         "Income": "💵",
# # # # # #         "Personal Care": "🧴",
# # # # # #         "Travel": "✈️",
# # # # # #     }
# # # # # #
# # # # # #     # Initialize session state for rows and expenses
# # # # # #     if f"expenses_{selected_date}" not in st.session_state:
# # # # # #         st.session_state[f"expenses_{selected_date}"] = existing_expenses
# # # # # #
# # # # # #     # Button to add a new row
# # # # # #     if st.button("Insert Row"):
# # # # # #         st.session_state[f"expenses_{selected_date}"].append({
# # # # # #             'user_name': "",
# # # # # #             'category': "",
# # # # # #             'subcategory': "",
# # # # # #             'transaction_type': "",
# # # # # #             'amount': 0.0,
# # # # # #             'notes': "",
# # # # # #         })
# # # # # #
# # # # # #     # Expenses management
# # # # # #     expenses = st.session_state[f"expenses_{selected_date}"]
# # # # # #     # List to store indices of rows to delete
# # # # # #     # List to store indices of rows to delete
# # # # # #     rows_to_delete = []
# # # # # #     col1, col2, col3, col4, col5, col6, col7 = st.columns([1.5, 2, 2, 1.5, 2, 2, 1])
# # # # # #     with col1:
# # # # # #         st.markdown("**Name** 👤")
# # # # # #     with col2:
# # # # # #         st.markdown("**Category** 📦")
# # # # # #     with col3:
# # # # # #         st.markdown("**Subcategory** 📦")
# # # # # #     with col4:
# # # # # #         st.markdown("**Amount** 💰")
# # # # # #     with col5:
# # # # # #         st.markdown("**Type** 🔄")
# # # # # #     with col6:
# # # # # #         st.markdown("**Note** 📝")
# # # # # #     with col7:
# # # # # #         st.markdown("**Delete**")
# # # # # #
# # # # # #     # Generate dynamic rows
# # # # # #     for i, expense in enumerate(expenses):
# # # # # #
# # # # # #
# # # # # #         col1, col2, col3, col4, col5, col6, col7 = st.columns([1.5, 2, 2, 1.5, 2, 2, 1])
# # # # # #
# # # # # #         with col1:
# # # # # #             name_options = ['Alice', 'Bob', 'Emily', 'Mark']
# # # # # #             name = st.selectbox(
# # # # # #                 "Name",
# # # # # #                 name_options,
# # # # # #                 index=name_options.index(expense['user_name']) if expense['user_name'] in name_options else 0,
# # # # # #                 key=f"name_{i}",
# # # # # #                 label_visibility="collapsed",
# # # # # #             )
# # # # # #
# # # # # #         with col2:
# # # # # #             category = st.selectbox(
# # # # # #                 "Category",
# # # # # #                 list(categories.keys()),
# # # # # #                 index=list(categories.keys()).index(expense['category']) if expense['category'] in categories else 0,
# # # # # #                 key=f"category_{i}",
# # # # # #                 label_visibility="collapsed",
# # # # # #             )
# # # # # #
# # # # # #         with col3:
# # # # # #             subcategory = st.text_input(
# # # # # #                 "Subcategory",
# # # # # #                 value=expense['subcategory'],
# # # # # #                 key=f"subcategory_{i}",
# # # # # #                 label_visibility="collapsed",
# # # # # #             )
# # # # # #         with col4:
# # # # # #             amount = st.number_input(
# # # # # #                 "Amount",
# # # # # #                 min_value=0.0,
# # # # # #                 step=1.0,
# # # # # #                 value=expense['amount'],
# # # # # #                 key=f"amount_{i}",
# # # # # #                 label_visibility="collapsed",
# # # # # #             )
# # # # # #
# # # # # #
# # # # # #         with col5:
# # # # # #             expense_type = st.selectbox(
# # # # # #                 "Type",
# # # # # #                 ["Credit", "Debit"],
# # # # # #                 index=["Credit", "Debit"].index(expense['transaction_type'])
# # # # # #                 if expense['transaction_type'] in ["Credit", "Debit"] else 0,
# # # # # #                 key=f"type_{i}",
# # # # # #                 label_visibility="collapsed",
# # # # # #             )
# # # # # #
# # # # # #
# # # # # #
# # # # # #         with col6:
# # # # # #             note = st.text_input(
# # # # # #                 "Notes",
# # # # # #                 value=expense['notes'],
# # # # # #                 key=f"note_{i}",
# # # # # #                 label_visibility="collapsed",
# # # # # #             )
# # # # # #
# # # # # #         with col7:
# # # # # #             # Delete button to remove the row
# # # # # #             delete_button = st.button(f"Delete Row {i}", key=f"delete_{i}")
# # # # # #
# # # # # #             if delete_button:
# # # # # #                 rows_to_delete.append(i)
# # # # # #     if rows_to_delete:
# # # # # #     # # Filter out the rows that need to be deleted
# # # # # #         expenses = [expense for i, expense in enumerate(expenses) if i not in rows_to_delete]
# # # # # #         st.session_state[f"expenses_{selected_date}"] = expenses
# # # # # #         st.success("Selected rows have been removed!")
# # # # # #
# # # # # #         # Re-render the table after deletion
# # # # # #         st.rerun()   # This forces a re-render to immediately reflect changes
# # # # # #
# # # # # #
# # # # # #     # Get the transaction details from the session state
# # # # # #     expenses = st.session_state[f"expenses_{selected_date}"]
# # # # # #
# # # # # #
# # # # # #     # Function to check if an expense is already in the existing expenses list
# # # # # #     def is_duplicate(expense, existing_expenses):
# # # # # #         for existing_expense in existing_expenses:
# # # # # #             if (expense['user_name'] == existing_expense['user_name'] and
# # # # # #                     expense['category'] == existing_expense['category'] and
# # # # # #                     expense['subcategory'] == existing_expense['subcategory'] and
# # # # # #                     expense['amount'] == existing_expense['amount'] and
# # # # # #                     expense['transaction_type'] == existing_expense['transaction_type'] and
# # # # # #                     expense['notes'] == existing_expense['notes']):
# # # # # #                 return True
# # # # # #         return False
# # # # # #
# # # # # #
# # # # # #     # Filter out the expenses that have already been added (duplicates)
# # # # # #     new_expenses = [expense for expense in expenses if not is_duplicate(expense, existing_expenses)]
# # # # # #
# # # # # #     submit_button = st.button("Submit")
# # # # # #
# # # # # #     if submit_button:
# # # # # #         # Filter out rows with invalid amounts (e.g., zero or negative)
# # # # # #         filtered_expenses = [expense for expense in new_expenses if expense['amount'] > 0]
# # # # # #
# # # # # #         # Send the data to the backend API if there are valid expenses
# # # # # #         if filtered_expenses:
# # # # # #             data_to_send = filtered_expenses
# # # # # #             response = requests.post(f"{API_URL}/expenses/{selected_date}", json=data_to_send)
# # # # # #
# # # # # #             # Check the response status
# # # # # #             if response.status_code == 200:
# # # # # #                 st.success("Expenses submitted successfully!")
# # # # # #             else:
# # # # # #                 st.error(f"Failed to submit expenses. Error: {response.text}")
# # # # # #         else:
# # # # # #             st.warning("No valid expenses to submit.")
# # # # # #
# # # # # #     # After pressing delete buttons, update session state to remove selected rows
# # # # # #     # if rows_to_delete:
# # # # # #     #     # Filter out the rows that need to be deleted
# # # # # #     #     expenses = [expense for i, expense in enumerate(expenses) if i not in rows_to_delete]
# # # # # #     #     st.session_state[f"expenses_{selected_date}"] = expenses
# # # # # #     #     st.success("Selected rows have been removed!")
# # # # # #     #
# # # # # #     #     # Re-render the table after deletion
# # # # # #     #     st.rerun()   # This forces a re-render to immediately reflect changes
# # # # # #     # submit_button = st.button("Submit")
# # # # # #     #
# # # # # #     # if submit_button:
# # # # # #     #     # Filter out rows with invalid amounts (e.g., zero or negative)
# # # # # #     #     filtered_expenses = [expense for expense in expenses if expense['amount'] > 0]
# # # # # #     #
# # # # # #     #     # Send the data to the backend API
# # # # # #     #     if filtered_expenses:
# # # # # #     #         data_to_send = filtered_expenses
# # # # # #     #         response = requests.post(f"{API_URL}/expenses/{selected_date}", json=data_to_send)
# # # # # #     #
# # # # # #     #         # Check the response status
# # # # # #     #         if response.status_code == 200:
# # # # # #     #             st.success("Expenses submitted successfully!")
# # # # # #     #         else:
# # # # # #     #             st.error(f"Failed to submit expenses. Error: {response.text}")
# # # # # #     #     else:
# # # # # #     #         st.warning("No valid expenses to submit.")
# # # # # #     #
# # # # # import requests
# # # # # import streamlit as st
# # # # # from datetime import date
# # # # # import pandas as pd
# # # # # import matplotlib.pyplot as plt
# # # # # from datetime import datetime
# # # # # from functools import partial
# # # # #
# # # # # # Setting the page configuration as wide
# # # # # st.set_page_config(layout="wide")
# # # # #
# # # # # # Heading
# # # # # st.markdown(
# # # # #     """
# # # # #     <style>
# # # # #     .centered-title {
# # # # #         text-align: center;
# # # # #         font-size: 40px;
# # # # #         font-family: Times New Roman;
# # # # #     }
# # # # #     </style>
# # # # #     """,
# # # # #     unsafe_allow_html=True,
# # # # # )
# # # # # st.markdown('<div class="centered-title">Expense Tracker</div>', unsafe_allow_html=True)
# # # # #
# # # # # # API URL placeholder
# # # # # API_URL = "http://127.0.0.1:8000"
# # # # #
# # # # # # Tabs
# # # # # tab1, tab2, tab3 = st.tabs(["Add/Update", "Analytics by category", "Analytics by month"])
# # # # #
# # # # # with tab1:
# # # # #     # Date input
# # # # #     selected_date = st.date_input(
# # # # #         "Add the date:",
# # # # #         min_value=date(2020, 1, 1),
# # # # #         max_value=date(2030, 1, 1),
# # # # #         label_visibility="collapsed",
# # # # #     )
# # # # #
# # # # #     # Fetch existing expenses
# # # # #     response = requests.get(f"{API_URL}/expenses/{selected_date}")
# # # # #     if response.status_code == 200:
# # # # #         existing_expenses = response.json()
# # # # #     else:
# # # # #         st.error("Failed to fetch expenses")
# # # # #         existing_expenses = []
# # # # #
# # # # #     # Define categories
# # # # #     categories = {
# # # # #         "Food": "🍔",
# # # # #         "Healthcare": "💊",
# # # # #         "Housing": "🏠",
# # # # #         "Income": "💵",
# # # # #         "Personal Care": "🧴",
# # # # #         "Travel": "✈️",
# # # # #     }
# # # # #
# # # # #     # Initialize session state for rows and expenses
# # # # #     if f"expenses_{selected_date}" not in st.session_state:
# # # # #         st.session_state[f"expenses_{selected_date}"] = existing_expenses
# # # # #
# # # # #     # Button to add a new row
# # # # #     if st.button("Insert Row"):
# # # # #         st.session_state[f"expenses_{selected_date}"].append({
# # # # #             'user_name': "",
# # # # #             'category': "",
# # # # #             'subcategory': "",
# # # # #             'transaction_type': "",
# # # # #             'amount': 0.0,
# # # # #             'notes': "",
# # # # #         })
# # # # #         st.rerun()
# # # # #
# # # # #     # Expenses management
# # # # #     expenses = st.session_state[f"expenses_{selected_date}"]
# # # # #     st.write("Expenses:", expenses)
# # # # #     st.write("Existing Expenses:", existing_expenses)
# # # # #
# # # # #     # List to store indices of rows to delete
# # # # #     rows_to_delete = []
# # # # #     col1, col2, col3, col4, col5, col6, col7 = st.columns([1.5, 2, 2, 1.5, 2, 2, 1])
# # # # #     with col1:
# # # # #         st.markdown("**Name** 👤")
# # # # #     with col2:
# # # # #         st.markdown("**Category** 📦")
# # # # #     with col3:
# # # # #         st.markdown("**Subcategory** 📦")
# # # # #     with col4:
# # # # #         st.markdown("**Amount** 💰")
# # # # #     with col5:
# # # # #         st.markdown("**Type** 🔄")
# # # # #     with col6:
# # # # #         st.markdown("**Note** 📝")
# # # # #     with col7:
# # # # #         st.markdown("**Delete**")
# # # # #
# # # # #     # Generate dynamic rows
# # # # #     for i, expense in enumerate(expenses):
# # # # #         col1, col2, col3, col4, col5, col6, col7 = st.columns([1.5, 2, 2, 1.5, 2, 2, 1])
# # # # #
# # # # #         with col1:
# # # # #             name_options = ['Alice', 'Bob', 'Emily', 'Mark']
# # # # #             name = st.selectbox(
# # # # #                 "Name",
# # # # #                 name_options,
# # # # #                 index=name_options.index(expense['user_name']) if expense['user_name'] in name_options else 0,
# # # # #                 key=f"name_{i}",
# # # # #                 label_visibility="collapsed",
# # # # #             )
# # # # #
# # # # #         with col2:
# # # # #             category = st.selectbox(
# # # # #                 "Category",
# # # # #                 list(categories.keys()),
# # # # #                 index=list(categories.keys()).index(expense['category']) if expense['category'] in categories else 0,
# # # # #                 key=f"category_{i}",
# # # # #                 label_visibility="collapsed",
# # # # #             )
# # # # #
# # # # #         with col3:
# # # # #             subcategory = st.text_input(
# # # # #                 "Subcategory",
# # # # #                 value=expense['subcategory'],
# # # # #                 key=f"subcategory_{i}",
# # # # #                 label_visibility="collapsed",
# # # # #             )
# # # # #         with col4:
# # # # #             amount = st.number_input(
# # # # #                 "Amount",
# # # # #                 min_value=0.0,
# # # # #                 step=1.0,
# # # # #                 value=expense['amount'],
# # # # #                 key=f"amount_{i}",
# # # # #                 label_visibility="collapsed",
# # # # #             )
# # # # #
# # # # #         with col5:
# # # # #             expense_type = st.selectbox(
# # # # #                 "Type",
# # # # #                 ["Credit", "Debit"],
# # # # #                 index=["Credit", "Debit"].index(expense['transaction_type'])
# # # # #                 if expense['transaction_type'] in ["Credit", "Debit"] else 0,
# # # # #                 key=f"type_{i}",
# # # # #                 label_visibility="collapsed",
# # # # #             )
# # # # #
# # # # #         with col6:
# # # # #             note = st.text_input(
# # # # #                 "Notes",
# # # # #                 value=expense['notes'],
# # # # #                 key=f"note_{i}",
# # # # #                 label_visibility="collapsed",
# # # # #             )
# # # # #
# # # # #         with col7:
# # # # #             # Delete button to remove the row
# # # # #             delete_button = st.button(f"Delete Row {i}", key=f"delete_{i}")
# # # # #
# # # # #             if delete_button:
# # # # #                 rows_to_delete.append(i)
# # # # #
# # # # #     if rows_to_delete:
# # # # #         # Filter out the rows that need to be deleted
# # # # #         expenses = [expense for i, expense in enumerate(expenses) if i not in rows_to_delete]
# # # # #         st.session_state[f"expenses_{selected_date}"] = expenses
# # # # #         st.success("Selected rows have been removed!")
# # # # #
# # # # #         # Re-render the table after deletion
# # # # #         st.experimental_rerun()  # This forces a re-render to immediately reflect changes
# # # # #
# # # # #     # Function to check if an expense is already in the existing expenses list
# # # # #     def is_duplicate(expense, existing_expenses):
# # # # #         for existing_expense in existing_expenses:
# # # # #             if (expense['user_name'] == existing_expense['user_name'] and
# # # # #                     expense['category'] == existing_expense['category'] and
# # # # #                     expense['subcategory'] == existing_expense['subcategory'] and
# # # # #                     expense['amount'] == existing_expense['amount'] and
# # # # #                     expense['transaction_type'] == existing_expense['transaction_type'] and
# # # # #                     expense['notes'] == existing_expense['notes']):
# # # # #                 return True
# # # # #         return False
# # # # #
# # # # #     # Filter out the expenses that have already been added (duplicates)
# # # # #     new_expenses = [expense for expense in expenses if not is_duplicate(expense, existing_expenses)]
# # # # #     st.write("New Expenses:", new_expenses)
# # # # #
# # # # #     submit_button = st.button("Submit")
# # # # #     if submit_button:
# # # # #         # Filter out rows with invalid amounts (e.g., zero or negative)
# # # # #         filtered_expenses = [expense for expense in new_expenses if expense['amount'] > 0]
# # # # #         st.write("Filtered Expenses:", filtered_expenses)
# # # # #
# # # # #         # Send the data to the backend API if there are valid expenses
# # # # #         if filtered_expenses:
# # # # #             data_to_send = filtered_expenses
# # # # #             response = requests.post(f"{API_URL}/expenses/{selected_date}", json=data_to_send)
# # # # #
# # # # #             # Check the response status
# # # # #             if response.status_code == 200:
# # # # #                 st.success("Expenses submitted successfully!")
# # # # #             else:
# # # # #                 st.error(f"Failed to submit expenses. Error: {response.text}")
# # # # #         else:
# # # # #             st.warning("No valid expenses to submit.")
# # # # import requests
# # # # import streamlit as st
# # # # from datetime import date
# # # # import pandas as pd
# # # # import matplotlib.pyplot as plt
# # # # from datetime import datetime
# # # # from functools import partial
# # # #
# # # # # Setting the page configuration as wide
# # # # st.set_page_config(layout="wide")
# # # #
# # # # # Heading
# # # # st.markdown(
# # # #     """
# # # #     <style>
# # # #     .centered-title {
# # # #         text-align: center;
# # # #         font-size: 40px;
# # # #         font-family: Times New Roman;
# # # #     }
# # # #     </style>
# # # #     """,
# # # #     unsafe_allow_html=True,
# # # # )
# # # # st.markdown('<div class="centered-title">Expense Tracker</div>', unsafe_allow_html=True)
# # # #
# # # # # API URL placeholder
# # # # API_URL = "http://127.0.0.1:8000"
# # # #
# # # # # Tabs
# # # # tab1, tab2, tab3 = st.tabs(["Add/Update", "Analytics by category", "Analytics by month"])
# # # #
# # # # with tab1:
# # # #     # Date input
# # # #     selected_date = st.date_input(
# # # #         "Add the date:",
# # # #         min_value=date(2020, 1, 1),
# # # #         max_value=date(2030, 1, 1),
# # # #         label_visibility="collapsed",
# # # #     )
# # # #
# # # #     # Fetch existing expenses
# # # #     response = requests.get(f"{API_URL}/expenses/{selected_date}")
# # # #     if response.status_code == 200:
# # # #         existing_expenses = response.json()
# # # #     else:
# # # #         st.error("Failed to fetch expenses")
# # # #         existing_expenses = []
# # # #
# # # #     # Define categories
# # # #     categories = {
# # # #         "Food": "🍔",
# # # #         "Healthcare": "💊",
# # # #         "Housing": "🏠",
# # # #         "Income": "💵",
# # # #         "Personal Care": "🧴",
# # # #         "Travel": "✈️",
# # # #     }
# # # #
# # # #     # Initialize session state for rows and expenses
# # # #     if f"expenses_{selected_date}" not in st.session_state:
# # # #         st.session_state[f"expenses_{selected_date}"] = existing_expenses
# # # #
# # # #     # Button to add a new row
# # # #     if st.button("Insert Row"):
# # # #         st.session_state[f"expenses_{selected_date}"].append({
# # # #             'user_name': "",
# # # #             'category': "",
# # # #             'subcategory': "",
# # # #             'transaction_type': "",
# # # #             'amount': 0.0,
# # # #             'notes': "",
# # # #         })
# # # #
# # # #     # Expenses management
# # # #     expenses = st.session_state[f"expenses_{selected_date}"]
# # # #     st.write("Expenses:", expenses)
# # # #     st.write("Existing Expenses:", existing_expenses)
# # # #
# # # #     # List to store indices of rows to delete
# # # #     rows_to_delete = []
# # # #     col1, col2, col3, col4, col5, col6, col7 = st.columns([1.5, 2, 2, 1.5, 2, 2, 1])
# # # #     with col1:
# # # #         st.markdown("**Name** 👤")
# # # #     with col2:
# # # #         st.markdown("**Category** 📦")
# # # #     with col3:
# # # #         st.markdown("**Subcategory** 📦")
# # # #     with col4:
# # # #         st.markdown("**Amount** 💰")
# # # #     with col5:
# # # #         st.markdown("**Type** 🔄")
# # # #     with col6:
# # # #         st.markdown("**Note** 📝")
# # # #     with col7:
# # # #         st.markdown("**Delete**")
# # # #
# # # #     # Generate dynamic rows
# # # #     for i, expense in enumerate(expenses):
# # # #         col1, col2, col3, col4, col5, col6, col7 = st.columns([1.5, 2, 2, 1.5, 2, 2, 1])
# # # #
# # # #         with col1:
# # # #             name_options = ['Alice', 'Bob', 'Emily', 'Mark']
# # # #             name = st.selectbox(
# # # #                 "Name",
# # # #                 name_options,
# # # #                 index=name_options.index(expense['user_name']) if expense['user_name'] in name_options else 0,
# # # #                 key=f"name_{i}",
# # # #                 label_visibility="collapsed",
# # # #             )
# # # #
# # # #         with col2:
# # # #             category = st.selectbox(
# # # #                 "Category",
# # # #                 list(categories.keys()),
# # # #                 index=list(categories.keys()).index(expense['category']) if expense['category'] in categories else 0,
# # # #                 key=f"category_{i}",
# # # #                 label_visibility="collapsed",
# # # #             )
# # # #
# # # #         with col3:
# # # #             subcategory = st.text_input(
# # # #                 "Subcategory",
# # # #                 value=expense['subcategory'],
# # # #                 key=f"subcategory_{i}",
# # # #                 label_visibility="collapsed",
# # # #             )
# # # #         with col4:
# # # #             amount = st.number_input(
# # # #                 "Amount",
# # # #                 min_value=0.0,
# # # #                 step=1.0,
# # # #                 value=expense['amount'],
# # # #                 key=f"amount_{i}",
# # # #                 label_visibility="collapsed",
# # # #             )
# # # #
# # # #         with col5:
# # # #             expense_type = st.selectbox(
# # # #                 "Type",
# # # #                 ["Credit", "Debit"],
# # # #                 index=["Credit", "Debit"].index(expense['transaction_type'])
# # # #                 if expense['transaction_type'] in ["Credit", "Debit"] else 0,
# # # #                 key=f"type_{i}",
# # # #                 label_visibility="collapsed",
# # # #             )
# # # #
# # # #         with col6:
# # # #             note = st.text_input(
# # # #                 "Notes",
# # # #                 value=expense['notes'],
# # # #                 key=f"note_{i}",
# # # #                 label_visibility="collapsed",
# # # #             )
# # # #
# # # #         with col7:
# # # #             # Delete button to remove the row
# # # #             delete_button = st.button(f"Delete Row {i}", key=f"delete_{i}")
# # # #
# # # #             if delete_button:
# # # #                 rows_to_delete.append(i)
# # # #
# # # #     if rows_to_delete:
# # # #         # Filter out the rows that need to be deleted
# # # #         expenses = [expense for i, expense in enumerate(expenses) if i not in rows_to_delete]
# # # #         st.session_state[f"expenses_{selected_date}"] = expenses
# # # #         st.success("Selected rows have been removed!")
# # # #
# # # #         # Re-render the table after deletion
# # # #         st.experimental_rerun()  # This forces a re-render to immediately reflect changes
# # # #
# # # #     # Function to check if an expense is already in the existing expenses list
# # # #     def is_duplicate(expense, existing_expenses):
# # # #         for existing_expense in existing_expenses:
# # # #             if (expense['user_name'] == existing_expense['user_name'] and
# # # #                     expense['category'] == existing_expense['category'] and
# # # #                     expense['subcategory'] == existing_expense['subcategory'] and
# # # #                     expense['amount'] == existing_expense['amount'] and
# # # #                     expense['transaction_type'] == existing_expense['transaction_type'] and
# # # #                     expense['notes'] == existing_expense['notes']):
# # # #                 return True
# # # #         return False
# # # #
# # # #     # Filter out the expenses that have already been added (duplicates)
# # # #     new_expenses = [expense for expense in expenses if not is_duplicate(expense, existing_expenses)]
# # # #     st.write("New Expenses:", new_expenses)
# # # #
# # # #     submit_button = st.button("Submit")
# # # #     if submit_button:
# # # #         # Filter out rows with invalid amounts (e.g., zero or negative)
# # # #         filtered_expenses = [expense for expense in new_expenses if expense['amount'] > 0]
# # # #         st.write("Filtered Expenses:", filtered_expenses)
# # # #
# # # #         # Send the data to the backend API if there are valid expenses
# # # #         if filtered_expenses:
# # # #             data_to_send = filtered_expenses
# # # #             response = requests.post(f"{API_URL}/expenses/{selected_date}", json=data_to_send)
# # # #
# # # #             # Check the response status
# # # #             if response.status_code == 200:
# # # #                 st.success("Expenses submitted successfully!")
# # # #             else:
# # # #                 st.error(f"Failed to submit expenses. Error: {response.text}")
# # # #         else:
# # # #             st.warning("No valid expenses to submit.")
# # # import requests
# # # import streamlit as st
# # # from datetime import date
# # # import pandas as pd
# # # import matplotlib.pyplot as plt
# # # from datetime import datetime
# # # from functools import partial
# # #
# # # # Setting the page configuration as wide
# # # st.set_page_config(layout="wide")
# # #
# # # # Heading
# # # st.markdown(
# # #     """
# # #     <style>
# # #     .centered-title {
# # #         text-align: center;
# # #         font-size: 40px;
# # #         font-family: Times New Roman;
# # #     }
# # #     </style>
# # #     """,
# # #     unsafe_allow_html=True,
# # # )
# # # st.markdown('<div class="centered-title">Expense Tracker</div>', unsafe_allow_html=True)
# # #
# # # # API URL placeholder
# # # API_URL = "http://127.0.0.1:8000"
# # #
# # # # Tabs
# # # tab1, tab2, tab3 = st.tabs(["Add/Update", "Analytics by category", "Analytics by month"])
# # #
# # # with tab1:
# # #     # Date input
# # #     selected_date = st.date_input(
# # #         "Add the date:",
# # #         min_value=date(2020, 1, 1),
# # #         max_value=date(2030, 1, 1),
# # #         label_visibility="collapsed",
# # #     )
# # #
# # #     # Fetch existing expenses
# # #     response = requests.get(f"{API_URL}/expenses/{selected_date}")
# # #     if response.status_code == 200:
# # #         existing_expenses = response.json()
# # #     else:
# # #         st.error("Failed to fetch expenses")
# # #         existing_expenses = []
# # #
# # #     # Define categories
# # #     categories = {
# # #         "Food": "🍔",
# # #         "Healthcare": "💊",
# # #         "Housing": "🏠",
# # #         "Income": "💵",
# # #         "Personal Care": "🧴",
# # #         "Travel": "✈️",
# # #     }
# # #
# # #     # Initialize session state for rows and expenses
# # #     if f"expenses_{selected_date}" not in st.session_state:
# # #         st.session_state[f"expenses_{selected_date}"] = existing_expenses
# # #
# # #     # Button to add a new row
# # #     if st.button("Insert Row"):
# # #         st.session_state[f"expenses_{selected_date}"].append({
# # #             'user_name': "",
# # #             'category': "",
# # #             'subcategory': "",
# # #             'transaction_type': "",
# # #             'amount': 0.0,
# # #             'notes': "",
# # #         })
# # #         st.rerun()  # Re-render to reflect the new row
# # #
# # #     # Expenses management
# # #     expenses = st.session_state[f"expenses_{selected_date}"]
# # #     st.write("Expenses:", expenses)
# # #     st.write("Existing Expenses:", existing_expenses)
# # #
# # #     # List to store indices of rows to delete
# # #     rows_to_delete = []
# # #     col1, col2, col3, col4, col5, col6, col7 = st.columns([1.5, 2, 2, 1.5, 2, 2, 1])
# # #     with col1:
# # #         st.markdown("**Name** 👤")
# # #     with col2:
# # #         st.markdown("**Category** 📦")
# # #     with col3:
# # #         st.markdown("**Subcategory** 📦")
# # #     with col4:
# # #         st.markdown("**Amount** 💰")
# # #     with col5:
# # #         st.markdown("**Type** 🔄")
# # #     with col6:
# # #         st.markdown("**Note** 📝")
# # #     with col7:
# # #         st.markdown("**Delete**")
# # #
# # #     # Generate dynamic rows
# # #     for i, expense in enumerate(expenses):
# # #         col1, col2, col3, col4, col5, col6, col7 = st.columns([1.5, 2, 2, 1.5, 2, 2, 1])
# # #
# # #         with col1:
# # #             name_options = ['Alice', 'Bob', 'Emily', 'Mark']
# # #             name = st.selectbox(
# # #                 "Name",
# # #                 name_options,
# # #                 index=name_options.index(expense['user_name']) if expense['user_name'] in name_options else 0,
# # #                 key=f"name_{i}",
# # #                 label_visibility="collapsed",
# # #             )
# # #
# # #         with col2:
# # #             category = st.selectbox(
# # #                 "Category",
# # #                 list(categories.keys()),
# # #                 index=list(categories.keys()).index(expense['category']) if expense['category'] in categories else 0,
# # #                 key=f"category_{i}",
# # #                 label_visibility="collapsed",
# # #             )
# # #
# # #         with col3:
# # #             subcategory = st.text_input(
# # #                 "Subcategory",
# # #                 value=expense['subcategory'],
# # #                 key=f"subcategory_{i}",
# # #                 label_visibility="collapsed",
# # #             )
# # #         with col4:
# # #             amount = st.number_input(
# # #                 "Amount",
# # #                 min_value=0.0,
# # #                 step=1.0,
# # #                 value=expense['amount'],
# # #                 key=f"amount_{i}",
# # #                 label_visibility="collapsed",
# # #             )
# # #
# # #         with col5:
# # #             expense_type = st.selectbox(
# # #                 "Type",
# # #                 ["Credit", "Debit"],
# # #                 index=["Credit", "Debit"].index(expense['transaction_type'])
# # #                 if expense['transaction_type'] in ["Credit", "Debit"] else 0,
# # #                 key=f"type_{i}",
# # #                 label_visibility="collapsed",
# # #             )
# # #
# # #         with col6:
# # #             note = st.text_input(
# # #                 "Notes",
# # #                 value=expense['notes'],
# # #                 key=f"note_{i}",
# # #                 label_visibility="collapsed",
# # #             )
# # #
# # #         with col7:
# # #             # Delete button to remove the row
# # #             delete_button = st.button(f"Delete Row {i}", key=f"delete_{i}")
# # #
# # #             if delete_button:
# # #                 rows_to_delete.append(i)
# # #
# # #     if rows_to_delete:
# # #         # Filter out the rows that need to be deleted
# # #         expenses = [expense for i, expense in enumerate(expenses) if i not in rows_to_delete]
# # #         st.session_state[f"expenses_{selected_date}"] = expenses
# # #         st.success("Selected rows have been removed!")
# # #
# # #         # Re-render the table after deletion
# # #         st.experimental_rerun()  # This forces a re-render to immediately reflect changes
# # #
# # #     # Function to check if an expense is already in the existing expenses list
# # #     def is_duplicate(expense, existing_expenses):
# # #         for existing_expense in existing_expenses:
# # #             if (expense['user_name'] == existing_expense['user_name'] and
# # #                     expense['category'] == existing_expense['category'] and
# # #                     expense['subcategory'] == existing_expense['subcategory'] and
# # #                     expense['amount'] == existing_expense['amount'] and
# # #                     expense['transaction_type'] == existing_expense['transaction_type'] and
# # #                     expense['notes'] == existing_expense['notes']):
# # #                 return True
# # #         return False
# # #
# # #     # Filter out the expenses that have already been added (duplicates)
# # #     new_expenses = [expense for expense in expenses if not is_duplicate(expense, existing_expenses)]
# # #     st.write("New Expenses:", new_expenses)
# # #
# # #     submit_button = st.button("Submit")
# # #     if submit_button:
# # #         # Filter out rows with invalid amounts (e.g., zero or negative)
# # #         filtered_expenses = [expense for expense in new_expenses if expense['amount'] > 0]
# # #         st.write("Filtered Expenses:", filtered_expenses)
# # #
# # #         # Send the data to the backend API if there are valid expenses
# # #         if filtered_expenses:
# # #             data_to_send = filtered_expenses
# # #             response = requests.post(f"{API_URL}/expenses/{selected_date}", json=data_to_send)
# # #
# # #             # Check the response status
# # #             if response.status_code == 200:
# # #                 st.success("Expenses submitted successfully!")
# # #             else:
# # #                 st.error(f"Failed to submit expenses. Error: {response.text}")
# # #         else:
# # #             st.warning("No valid expenses to submit.")
# #
# # import requests
# # import streamlit as st
# # from datetime import date
# # import pandas as pd
# # import matplotlib.pyplot as plt
# # from datetime import datetime
# # from functools import partial
# #
# # # Setting the page configuration as wide
# # st.set_page_config(layout="wide")
# #
# # # Heading
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
# # st.markdown('<div class="centered-title">Expense Tracker</div>', unsafe_allow_html=True)
# #
# # # API URL placeholder
# # API_URL = "http://127.0.0.1:8000"
# #
# # # Tabs
# # tab1, tab2, tab3 = st.tabs(["Add/Update", "Analytics by category", "Analytics by month"])
# #
# # with tab1:
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
# #     # Define categories
# #     categories = {
# #         "Food": "🍔",
# #         "Healthcare": "💊",
# #         "Housing": "🏠",
# #         "Income": "💵",
# #         "Personal Care": "🧴",
# #         "Travel": "✈️",
# #     }
# #
# #     # Initialize session state for rows and expenses
# #     if f"expenses_{selected_date}" not in st.session_state:
# #         st.session_state[f"expenses_{selected_date}"] = existing_expenses
# #
# #     # Temporary dictionary to store new row data
# #     new_expense = {
# #         'user_name': "",
# #         'category': "",
# #         'subcategory': "",
# #         'transaction_type': "",
# #         'amount': 0.0,
# #         'notes': "",
# #     }
# #
# #     # Input fields for new row data
# #     st.write("Add a new expense:")
# #     new_expense['user_name'] = st.selectbox("Name", ['Alice', 'Bob', 'Emily', 'Mark'], key='new_user_name')
# #     new_expense['category'] = st.selectbox("Category", list(categories.keys()), key='new_category')
# #     new_expense['subcategory'] = st.text_input("Subcategory", key='new_subcategory')
# #     new_expense['amount'] = st.number_input("Amount", min_value=0.0, step=1.0, key='new_amount')
# #     new_expense['transaction_type'] = st.selectbox("Type", ["Credit", "Debit"], key='new_transaction_type')
# #     new_expense['notes'] = st.text_input("Notes", key='new_notes')
# #
# #     if st.button("Insert Row"):
# #         # Check if required fields are filled
# #         if new_expense['user_name'] and new_expense['category'] and new_expense['amount'] > 0:
# #             st.session_state[f"expenses_{selected_date}"].append(new_expense)
# #             st.rerun()  # Re-render to reflect the new row
# #         else:
# #             st.warning("Please fill in all required fields.")
# #
# #     # Expenses management
# #     expenses = st.session_state[f"expenses_{selected_date}"]
# #     st.write("Expenses:", expenses)
# #     st.write("Existing Expenses:", existing_expenses)
# #
# #     # List to store indices of rows to delete
# #     rows_to_delete = []
# #     col1, col2, col3, col4, col5, col6, col7 = st.columns([1.5, 2, 2, 1.5, 2, 2, 1])
# #     with col1:
# #         st.markdown("**Name** 👤")
# #     with col2:
# #         st.markdown("**Category** 📦")
# #     with col3:
# #         st.markdown("**Subcategory** 📦")
# #     with col4:
# #         st.markdown("**Amount** 💰")
# #     with col5:
# #         st.markdown("**Type** 🔄")
# #     with col6:
# #         st.markdown("**Note** 📝")
# #     with col7:
# #         st.markdown("**Delete**")
# #
# #     # Generate dynamic rows
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
# #                 value=expense['subcategory'],
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
# #
# #         with col5:
# #             expense_type = st.selectbox(
# #                 "Type",
# #                 ["Credit", "Debit"],
# #                 index=["Credit", "Debit"].index(expense['transaction_type'])
# #                 if expense['transaction_type'] in ["Credit", "Debit"] else 0,
# #                 key=f"type_{i}",
# #                 label_visibility="collapsed",
# #             )
# #
# #         with col6:
# #             note = st.text_input(
# #                 "Notes",
# #                 value=expense['notes'],
# #                 key=f"note_{i}",
# #                 label_visibility="collapsed",
# #             )
# #
# #         with col7:
# #             # Delete button to remove the row
# #             delete_button = st.button(f"Delete Row {i}", key=f"delete_{i}")
# #
# #             if delete_button:
# #                 rows_to_delete.append(i)
# #
# #     if rows_to_delete:
# #         # Filter out the rows that need to be deleted
# #         expenses = [expense for i, expense in enumerate(expenses) if i not in rows_to_delete]
# #         st.session_state[f"expenses_{selected_date}"] = expenses
# #         st.success("Selected rows have been removed!")
# #
# #         # Re-render the table after deletion
# #         st.rerun()  # This forces a re-render to immediately reflect changes
# #
# #     # Function to check if an expense is already in the existing expenses list
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
# #     # Filter out the expenses that have already been added (duplicates)
# #     new_expenses = [expense for expense in expenses if not is_duplicate(expense, existing_expenses)]
# #     st.write("New Expenses:", new_expenses)
# #
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
#
#
#
# import requests
# import streamlit as st
# from datetime import date
# import pandas as pd
# import matplotlib.pyplot as plt
# from datetime import datetime
# from functools import partial
#
# # Setting the page configuration as wide
# st.set_page_config(layout="wide")
#
# # Heading
# st.markdown(
#     """
#     <style>
#     .centered-title {
#         text-align: center;
#         font-size: 40px;
#         font-family: Times New Roman;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )
# st.markdown('<div class="centered-title">Expense Tracker</div>', unsafe_allow_html=True)
#
# # API URL placeholder
# API_URL = "http://127.0.0.1:8000"
#
# # Tabs
# tab1, tab2, tab3 = st.tabs(["Add/Update", "Analytics by category", "Analytics by month"])
#
# with tab1:
#     # Date input
#     selected_date = st.date_input(
#         "Add the date:",
#         min_value=date(2020, 1, 1),
#         max_value=date(2030, 1, 1),
#         label_visibility="collapsed",
#     )
#
#     # Fetch existing expenses
#     response = requests.get(f"{API_URL}/expenses/{selected_date}")
#     if response.status_code == 200:
#         existing_expenses = response.json()
#     else:
#         st.error("Failed to fetch expenses")
#         existing_expenses = []
#
#     # Define categories
#     categories = {
#         "Food": "🍔",
#         "Healthcare": "💊",
#         "Housing": "🏠",
#         "Income": "💵",
#         "Personal Care": "🧴",
#         "Travel": "✈️",
#     }
#
#     # Initialize session state for rows and expenses
#     if f"expenses_{selected_date}" not in st.session_state:
#         st.session_state[f"expenses_{selected_date}"] = existing_expenses
#
#     # Temporary dictionary to store new row data
#     new_expense = {
#         'user_name': ['Alice', 'Bob', 'Emily', 'Mark'],
#         'category': "",
#         'subcategory': "",
#         'transaction_type': "",
#         'amount': 0.0,
#         'notes': "",
#     }
#
#     # Button to add a new row
#     if st.button("Insert Row"):
#         # Add a placeholder row with empty values (will update once user interacts with it)
#         expenses.append({
#             'user_name': "",
#             'category': "",
#             'subcategory': "",
#             'transaction_type': "",
#             'amount': 0.0,
#             'notes': "",
#         })
#         st.session_state[f"expenses_{selected_date}"] = expenses
#         st.rerun()  # Re-render to reflect the new row
#     # Expenses management
#     expenses = st.session_state[f"expenses_{selected_date}"]
#     st.write("Expenses:", expenses)
#     st.write("Existing Expenses:", existing_expenses)
#
#     # List to store indices of rows to delete
#     rows_to_delete = []
#     col1, col2, col3, col4, col5, col6, col7 = st.columns([1.5, 2, 2, 1.5, 2, 2, 1])
#     with col1:
#         st.markdown("**Name** 👤")
#     with col2:
#         st.markdown("**Category** 📦")
#     with col3:
#         st.markdown("**Subcategory** 📦")
#     with col4:
#         st.markdown("**Amount** 💰")
#     with col5:
#         st.markdown("**Type** 🔄")
#     with col6:
#         st.markdown("**Note** 📝")
#     with col7:
#         st.markdown("**Delete**")
#
#     # Generate dynamic rows
#     for i, expense in enumerate(expenses):
#         col1, col2, col3, col4, col5, col6, col7 = st.columns([1.5, 2, 2, 1.5, 2, 2, 1])
#
#         with col1:
#             name_options = ['Alice', 'Bob', 'Emily', 'Mark']
#             name = st.selectbox(
#                 "Name",
#                 name_options,
#                 index=name_options.index(expense['user_name']) if expense['user_name'] in name_options else 0,
#                 key=f"name_{i}",
#                 label_visibility="collapsed",
#             )
#
#         with col2:
#             category = st.selectbox(
#                 "Category",
#                 list(categories.keys()),
#                 index=list(categories.keys()).index(expense['category']) if expense['category'] in categories else 0,
#                 key=f"category_{i}",
#                 label_visibility="collapsed",
#             )
#
#         with col3:
#             subcategory = st.text_input(
#                 "Subcategory",
#                 value=expense['subcategory'],
#                 key=f"subcategory_{i}",
#                 label_visibility="collapsed",
#             )
#         with col4:
#             amount = st.number_input(
#                 "Amount",
#                 min_value=0.0,
#                 step=1.0,
#                 value=expense['amount'],
#                 key=f"amount_{i}",
#                 label_visibility="collapsed",
#             )
#
#         with col5:
#             expense_type = st.selectbox(
#                 "Type",
#                 ["Credit", "Debit"],
#                 index=["Credit", "Debit"].index(expense['transaction_type'])
#                 if expense['transaction_type'] in ["Credit", "Debit"] else 0,
#                 key=f"type_{i}",
#                 label_visibility="collapsed",
#             )
#
#         with col6:
#             note = st.text_input(
#                 "Notes",
#                 value=expense['notes'],
#                 key=f"note_{i}",
#                 label_visibility="collapsed",
#             )
#
#         with col7:
#             # Delete button to remove the row
#             delete_button = st.button(f"Delete Row {i}", key=f"delete_{i}")
#
#             if delete_button:
#                 rows_to_delete.append(i)
#
#     if rows_to_delete:
#         # Filter out the rows that need to be deleted
#         expenses = [expense for i, expense in enumerate(expenses) if i not in rows_to_delete]
#         st.session_state[f"expenses_{selected_date}"] = expenses
#         st.success("Selected rows have been removed!")
#
#         # Re-render the table after deletion
#         st.rerun()  # This forces a re-render to immediately reflect changes
#
#     # Function to check if an expense is already in the existing expenses list
#     def is_duplicate(expense, existing_expenses):
#         for existing_expense in existing_expenses:
#             if (expense['user_name'] == existing_expense['user_name'] and
#                     expense['category'] == existing_expense['category'] and
#                     expense['subcategory'] == existing_expense['subcategory'] and
#                     expense['amount'] == existing_expense['amount'] and
#                     expense['transaction_type'] == existing_expense['transaction_type'] and
#                     expense['notes'] == existing_expense['notes']):
#                 return True
#         return False
#
#     # Filter out the expenses that have already been added (duplicates)
#     new_expenses = [expense for expense in expenses if not is_duplicate(expense, existing_expenses)]
#     st.write("New Expenses:", new_expenses)
#
#     submit_button = st.button("Submit")
#     if submit_button:
#         # Filter out rows with invalid amounts (e.g., zero or negative)
#         filtered_expenses = [expense for expense in new_expenses if expense['amount'] > 0]
#         st.write("Filtered Expenses:", filtered_expenses)
#
#         # Send the data to the backend API if there are valid expenses
#         if filtered_expenses:
#             data_to_send = filtered_expenses
#             response = requests.post(f"{API_URL}/expenses/{selected_date}", json=data_to_send)
#
#             # Check the response status
#             if response.status_code == 200:
#                 st.success("Expenses submitted successfully!")
#             else:
#                 st.error(f"Failed to submit expenses. Error: {response.text}")
#         else:
#             st.warning("No valid expenses to submit.")
import requests
import streamlit as st
from datetime import date



# Setting the page configuration as wide
st.set_page_config(layout="wide")

# Heading
st.markdown(
    """
    <style>
    .centered-title {
        text-align: center;
        font-size: 40px;
        font-family: Times New Roman;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
st.markdown('<div class="centered-title">Expense Tracker</div>', unsafe_allow_html=True)

# API URL placeholder
API_URL = "http://127.0.0.1:8000"

# Tabs
tab1, tab2, tab3 = st.tabs(["Add/Update", "Analytics by category", "Analytics by month"])

with tab1:
    # Date input
    selected_date = st.date_input(
        "Add the date:",
        min_value=date(2020, 1, 1),
        max_value=date(2030, 1, 1),
        label_visibility="collapsed",
    )

    # Fetch existing expenses
    response = requests.get(f"{API_URL}/expenses/{selected_date}")
    if response.status_code == 200:
        existing_expenses = response.json()
    else:
        st.error("Failed to fetch expenses")
        existing_expenses = []

    # Define categories
    categories = {
        "Food": "🍔",
        "Healthcare": "💊",
        "Housing": "🏠",
        "Income": "💵",
        "Personal Care": "🧴",
        "Travel": "✈️",
    }

    # Initialize session state for rows and expenses
    if f"expenses_{selected_date}" not in st.session_state:
        st.session_state[f"expenses_{selected_date}"] = existing_expenses

    # Expenses management
    expenses = st.session_state[f"expenses_{selected_date}"]

    # Button to add a new row




    # List to store indices of rows to delete
    rows_to_delete = []

    # Dynamically render rows
    col1, col2, col3, col4, col5, col6, col7 = st.columns([1.5, 2, 2, 1.5, 2, 2, 1])
    with col1:
        st.markdown("**Name** 👤")
    with col2:
        st.markdown("**Category** 📦")
    with col3:
        st.markdown("**Subcategory** 📦")
    with col4:
        st.markdown("**Amount** 💰")
    with col5:
        st.markdown("**Type** 🔄")
    with col6:
        st.markdown("**Note** 📝")
    with col7:
        st.markdown("**Delete**")

    # Create form inputs for each expense
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
                value=expense['subcategory'],
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
            expense_type = st.selectbox(
                "Type",
                ["Credit", "Debit"],
                index=["Credit", "Debit"].index(expense['transaction_type'])
                if expense['transaction_type'] in ["Credit", "Debit"] else 0,
                key=f"type_{i}",
                label_visibility="collapsed",
            )

        with col6:
            note = st.text_input(
                "Notes",
                value=expense['notes'],
                key=f"note_{i}",
                label_visibility="collapsed",
            )

        with col7:
            # Delete button to remove the row
            delete_button = st.button(f"Delete Row {i}", key=f"delete_{i}")

            if delete_button:
                rows_to_delete.append(i)





    if rows_to_delete:
        # Filter out the rows that need to be deleted
        expenses = [expense for i, expense in enumerate(expenses) if i not in rows_to_delete]
        st.session_state[f"expenses_{selected_date}"] = expenses
        st.success("Selected rows have been removed!")

        # Re-render the table after deletion
        st.rerun()  # This forces a re-render to immediately reflect changes

    # Function to check if an expense is already in the existing expenses list
    def is_duplicate(expense, existing_expenses):
        for existing_expense in existing_expenses:
            if (expense['user_name'] == existing_expense['user_name'] and
                    expense['category'] == existing_expense['category'] and
                    expense['subcategory'] == existing_expense['subcategory'] and
                    expense['amount'] == existing_expense['amount'] and
                    expense['transaction_type'] == existing_expense['transaction_type'] and
                    expense['notes'] == existing_expense['notes']):
                return True
        return False

    # Filter out the expenses that have already been added (duplicates)
    new_expenses = [expense for expense in expenses if not is_duplicate(expense, existing_expenses)]
    st.write("New Expenses:", new_expenses)

    submit_button = st.button("Submit")
    if submit_button:
        # Filter out rows with invalid amounts (e.g., zero or negative)
        filtered_expenses = [expense for expense in new_expenses if expense['amount'] > 0]
        st.write("Filtered Expenses:", filtered_expenses)

        # Send the data to the backend API if there are valid expenses
        if filtered_expenses:
            data_to_send = filtered_expenses
            response = requests.post(f"{API_URL}/expenses/{selected_date}", json=data_to_send)

            # Check the response status
            if response.status_code == 200:
                st.success("Expenses submitted successfully!")
            else:
                st.error(f"Failed to submit expenses. Error: {response.text}")
        else:
            st.warning("No valid expenses to submit.")
