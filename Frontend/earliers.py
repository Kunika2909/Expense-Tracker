# import requests
# import streamlit as st
# from datetime import date
# import pandas as pd
# import matplotlib.pyplot as plt
# from datetime import datetime
#
#
# #setting the page configuration as wide
#
# st.set_page_config(layout="wide")
#
# #Heading
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
#
# st.markdown('<div class="centered-title">Expense Tracker</div>', unsafe_allow_html=True)
#
# #local host url
# API_URL = "http://127.0.0.1:8000"
#
# # Define tabs more like 2 pages
# tab1, tab2,tab3= st.tabs(["Add/Update", "Analytics by category","Analytics by month"])
#
# with tab1:
#     # Date input
#     selected_date = st.date_input(
#         "Add the date:",
#         min_value=date(2020, 1, 1),
#         max_value=date(2030, 1, 1),
#         label_visibility="collapsed"
#     )
#
#     # Fetch existing expenses
#     response = requests.get(f"{API_URL}/expenses/{selected_date}")
#     if response.status_code == 200:
#         existing_expenses = response.json()
#         #st.write(existing_expenses)
#     else:
#         st.error("Failed to fetch expenses")
#         existing_expenses = []
#
#     # Define categories
#     Category = {
#         "Food": "🍔",
#         "Healthcare": "💊",
#         "Housing": "🏠",
#         "Income": "💵",
#         "Personal Care": "🧴",
#         "Travel": "✈️"
#     }
#     if f"num_rows_{selected_date}" not in st.session_state:
#         st.session_state[f"num_rows_{selected_date}"] = max(len(existing_expenses), 1)
#
#     if f"add_row_{selected_date}" not in st.session_state:
#         st.session_state[f"add_row_{selected_date}"] = False
#
#     if f"expenses_{selected_date}" not in st.session_state:
#         st.session_state[f"expenses_{selected_date}"] = existing_expenses
#
#     # Button to add a new row (outside the form)
#     if st.button("Insert Row"):
#         st.session_state[f"add_row_{selected_date}"] = True
#
#     # Define the number of rows based on existing_expenses
#
#     with st.form(key=f"expense_form_{selected_date}"):
#         expenses = st.session_state[f"expenses_{selected_date}"]
#         rows_to_delete = []
#
#         num_rows = st.session_state[f"num_rows_{selected_date}"]
#
#         if st.session_state[f"add_row_{selected_date}"]:
#             num_rows += 1
#             st.session_state[f"num_rows_{selected_date}"] = num_rows
#             st.session_state[f"add_row_{selected_date}"] = False
#             expenses.append({
#                 'user_name': "",
#                 'category': "",
#                 'subcategory': "",
#                 'transaction_type': "Credit",
#                 'amount': 0.0,
#                 'notes': ""
#             })
#
#         col1, col2, col3, col4, col5, col6,col7 = st.columns([1.5,2,2,1.5,2,2,1])
#         with col1:
#             st.markdown("**Name** 👤")
#         with col2:
#             st.markdown("**Category** 📦")
#         with col3:
#             st.markdown("**Subcategory** 📦")
#         with col4:
#             st.markdown("**Type** 🔄")
#         with col5:
#             st.markdown("**Amount** 💰")
#         with col6:
#             st.markdown("**Note** 📝")
#         with col7:
#             st.markdown("**Delete**")
#
#
#         # Insert Row button (outside the form)
#
#         # Inside the form
#             expenses = []  # To collect rows
#             rows_to_delete = []  # To track rows marked for deletion
#
#             # Use the date-specific num_rows value
#             num_rows = st.session_state.get(f'num_rows_{selected_date}', 1)
#
#             if st.session_state[f"add_row_{selected_date}"]:
#                 # Increment row count if "Insert Row" was clicked
#                 num_rows += 1
#                 st.session_state[f"num_rows_{selected_date}"] = num_rows
#                 st.session_state[f"add_row_{selected_date}"] = False
#
#
#
#
#
#
#                 # Generate dynamic input rows
#         for i in range(num_rows):
#             # Set default values for empty rows
#             if i < len(st.session_state.expenses):
#                 expense = st.session_state.expenses[i]
#                 name = expense.get('user_name', "")
#                 category = expense.get('category', "")
#                 subcategory = expense.get('subcategory', "")
#                 expense_type = expense.get('transaction_type', "Credit")
#                 amount = expense.get('amount', 0.0)
#                 note = expense.get('notes', "")
#             else:
#                 name = ""
#                 category = ""
#                 subcategory = ""
#                 expense_type = ""
#                 amount = 0.0
#                 note = ""
#
#             # Input fields for each row
#             col1, col2, col3, col4, col5, col6,col7= st.columns([1.5,2,2,1.5,2,2,1])
#             with col1:
#                 name_options = ['Alice', 'Bob', 'Emily', 'Mark']
#                 name_index = name_options.index(name) if name in name_options else 0  # Default to the first option
#                 name = st.selectbox(
#                     "Name",
#                     name_options,
#                     index=name_index,
#                     key=f"name_{i}",
#                     label_visibility="collapsed"
#                 )
#
#             with col2:
#                 category_index = list(Category.keys()).index(category) if category in Category else 0
#                 category = st.selectbox(
#                     "Category",
#                     list(Category.keys()),
#                     index=category_index,
#                     key=f"category_{i}",
#                     label_visibility="collapsed"
#                 )
#             with col3:
#                 subcategory = st.text_input(
#                     "Subcategory",
#                     value=subcategory,
#                     key=f"subcategory_{i}",
#                     label_visibility="collapsed"
#                 )
#             with col4:
#                 expense_type_index = ['Credit', 'Debit'].index(expense_type) if expense_type in ['Credit',
#                                                                                                  'Debit'] else 0
#                 expense_type = st.selectbox(
#                     "Type",
#                     ['Credit', 'Debit'],
#                     index=expense_type_index,
#                     key=f"type_{i}",
#                     label_visibility="collapsed"
#                 )
#             with col5:
#                 amount = st.number_input(
#                     "Amount",
#                     min_value=0.0,
#                     step=1.0,
#                     value=amount,
#                     key=f"amount_{i}",
#                     label_visibility="collapsed"
#                 )
#             with col6:
#                 note = st.text_input(
#                     "Notes",
#                     value=note,
#                     key=f"note_{i}",
#                     label_visibility="collapsed"
#                 )
#             with col7:
#                 delete_checkbox = st.checkbox(f"Delete {i}", key=f"delete_{i}", label_visibility="collapsed")
#                 if delete_checkbox:
#                     rows_to_delete.append(i)
#
#             expenses.append({
#                 'user_name': name,  # Ensure the API expects this key
#                 'category': category,
#                 'subcategory': subcategory,
#                 'transaction_type': expense_type,
#                 'amount': amount,
#                 'notes': note
#             })
#         if st.button("Insert Row"):
#             # Add a new row (add a dictionary with default values to the session state list)
#             st.session_state[f'expenses_{selected_date}'].append({
#                 'user_name': '',
#                 'category': '',
#                 'amount': 0.0,
#                 'notes': ''
#             })
#
#
#
#
#                 # Update the row count
#             submit_button = st.form_submit_button("Submit All")
#
#             # Handle form submission
#             if submit_button:
#                 expenses = [row for idx, row in enumerate(expenses) if idx not in rows_to_delete]
#                 st.session_state[f"expenses_{selected_date}"] = expenses
#                 st.session_state[f"num_rows_{selected_date}"] = len(expenses)
#                 st.success("Expenses updated!")
#
#         # Debugging: Display current rows
#         st.write("Current Expenses:", st.session_state[f"expenses_{selected_date}"])
#
# submit_button = st.form_submit_button("Submit")
#         if submit_button:
#             filtered_expenses = [expense for expense in expenses if expense['amount'] > 0]
#
#             # Send the data in the correct format
#             data_to_send = filtered_expenses
#
#             # Debugging: Check the structure of data being sent
#
#             response = requests.post(f"{API_URL}/expenses/{selected_date}", json=data_to_send)
#
#             # Check if the response is successful
#             if response.status_code == 200:
#             else:
#                 st.error(f"Failed to add expenses. Error: {response.text}")
#
#
#
#
#         # Filter expenses with amount greater than 0
#
#     # for i in range(num_rows):
#     #         delete_button = st.button(f"Delete Row {i}", key=f"delete_{i}")
#     #         if delete_button:
#     #             st.session_state.rows_to_delete.append(i)
# #builing analytics
#         #         st.success("Expenses added successfully!")
from urllib.request import localhost

#Heading
# st.markdown(
#     """
#     <style>
#     .title-container {
#         text-align: center;
#         font-size: 40px;
#         font-family: 'Times New Roman';
#         background-image: url(https://ebillity.com/wp-content/uploads/2021/11/blog-tt-operating-costs-expenses.jpeg);
#         background-size: cover;
#         padding: 50px;
#         border-radius: 10px;
#
#     }
#     .centered-title {
#         text-align: center;
#         font-size: 40px;
#         font-family: 'Times New Roman';
#
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )
#
# st.markdown('<div class="centered-title">Expense Tracker</div>', unsafe_allow_html=True)


# Filter new expenses to remove duplicates
new_expenses = [expense for expense in expenses if not is_duplicate(expense, existing_expenses)]
# submit_button = st.button("Submit")
# if submit_button:
#     # Filter out rows with invalid amounts (e.g., zero or negative)
#     filtered_expenses = [expense for expense in new_expenses if expense['amount'] > 0]
#     st.write("Filtered Expenses:", filtered_expenses)
#
#     # Send the data to the backend API if there are valid expenses
#     if filtered_expenses:
#         data_to_send = filtered_expenses
#         response = requests.post(f"{API_URL}/expenses/{selected_date}", json=data_to_send)
#
#         # Check the response status
#         if response.status_code == 200:
#             st.success("Expenses submitted successfully!")
#         else:
#             st.error(f"Failed to submit expenses. Error: {response.text}")
#     else:
#         st.warning("No valid expenses to submit.")

# Handle deletion of rows from session state and backend

# Update the session state after deletion

# Handle the submission of filtered expenses

# Re-render the page to show updated list after deletion

# Define the function to check for duplicates

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