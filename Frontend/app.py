# import requests
# import streamlit
# import streamlit as st
# import pandas as pd
# from datetime import date
#
# from streamlit import success
#
# st.set_page_config(layout="wide")
#
# st.markdown(
#     """
#     <style>
#     .centered-title {
#         text-align: center;
#         font-size: 40px;
#         font-family:Times New Roman;
#
#
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )
#
# st.markdown('<div class="centered-title">Expense Tracker</div>', unsafe_allow_html=True)
#
# API_URL = "http://127.0.0.1:8000"
# # Define tabs
# # Define tabs
# # Define tabs
# tab1, tab2 = st.tabs(["Add/Update Expenses", "Analytics"])
#
# with tab1:
#     # Date input
#     selected_date = st.date_input(
#         "Add the date:",
#         min_value=date(2020, 1, 1),
#         max_value=date(2040, 1, 1),
#         label_visibility="collapsed"
#     )
#
#     # Fetch existing expenses
#     response = requests.get(f"{API_URL}/expenses/{selected_date}")
#     if response.status_code == 200:
#         existing_expenses = response.json()
#         st.write(existing_expenses)
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
#         "Travel":"✈️"
#     }
#
#     # Define the number of rows based on existing_expenses
#     num_rows = len(existing_expenses) if existing_expenses else 5
#
#     # Define form with dynamic rows
#     with st.form(key="expense_form"):
#         # Header row
#         col1, col2, col3, col4, col5, col6 = st.columns(6)
#         with col1:
#             st.markdown("**Name**  👤")
#         with col2:
#             st.markdown("**Category**  📦")
#         with col3:
#             st.markdown("**Subcategory**  📦")
#         with col4:
#             st.markdown("**Type**  🔄")
#         with col5:
#             st.markdown("**Amount** 💰")
#         with col6:
#             st.markdown("**Note** 📝")
#
#         # Generate dynamic input rows
#
#         expenses = []
#                 for i in range(num_rows):
#                     # Set default values for empty rows
#                     if i < len(existing_expenses):
#                         expense = existing_expenses[i]
#                         name = expense.get('user_name', "")
#                         category = expense.get('category', "")
#                         subcategory = expense.get('subcategory', "")
#                         expense_type = expense.get('transaction_type', "Credit")
#                         amount = expense.get('amount', 0.0)
#                         note = expense.get('notes', "")
#                     else:
#                         name = ""
#                         category = ""
#                         subcategory = ""
#                         expense_type = "Credit"
#                         amount = 0.0
#                         note = ""
#
#             # Input fields for each row
#             col1, col2, col3, col4, col5, col6 = st.columns(6)
#             with col1:
#                 name_options = ['Alice', 'Bob', 'Emily', 'Mark']
#                 name_index = name_options.index(name) if name in name_options else 0  # Default to the first option
#                 user_name = st.selectbox(
#                     "User_name",
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
#                 expense_type_index = ['Credit', 'Debit'].index(expense_type) if expense_type in ['Credit', 'Debit'] else 0
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
#             expenses.append({'Name':name,
#                             'Category':category,
#                             'Subcategory':subcategory,
#                             'Transaction_type':expense_type,
#                             'Amount':amount,
#                             'Note':note}
#     submit_button = st.form_submit_button("Submit")
#     if submit_button:
#         filtered_expense = [expense for expense in expenses if expense['Amount'] > 0]
#     response = requests.post(f"{API_URL}/expenses/{selected_date}", json=filtered_expense)
#     if response == 200:
#         st.success("Expenses added successfully!")
#     else:
#         st.error(f"Failed to add expenses. Error: {response.text}")
    # Tab 2


import requests
import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(layout="wide")

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

API_URL = "http://127.0.0.1:8000"  # Replace with your API URL

# Define tabs
tab1, tab2 = st.tabs(["Add/Update Expenses", "Analytics"])

with tab1:
    # Date input
    selected_date = st.date_input(
        "Add the date:",
        min_value=date(2020, 1, 1),
        max_value=date(2040, 1, 1),
        label_visibility="collapsed"
    )

    # Fetch existing expenses
    response = requests.get(f"{API_URL}/expenses/{selected_date}")
    if response.status_code == 200:
        existing_expenses = response.json()
        st.write(existing_expenses)
    else:
        st.error("Failed to fetch expenses")
        existing_expenses = []

    # Define categories
    Category = {
        "Food": "🍔",
        "Healthcare": "💊",
        "Housing": "🏠",
        "Income": "💵",
        "Personal Care": "🧴",
        "Travel": "✈️"
    }

    # Define the number of rows based on existing_expenses
    num_rows = len(existing_expenses) if existing_expenses else 5

    # Define form with dynamic rows
    with st.form(key="expense_form"):
        # Header row
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:
            st.markdown("**Name** 👤")
        with col2:
            st.markdown("**Category** 📦")
        with col3:
            st.markdown("**Subcategory** 📦")
        with col4:
            st.markdown("**Type** 🔄")
        with col5:
            st.markdown("**Amount** 💰")
        with col6:
            st.markdown("**Note** 📝")

        # Generate dynamic input rows
        expenses = []
        for i in range(num_rows):
            # Set default values for empty rows
            if i < len(existing_expenses):
                expense = existing_expenses[i]
                name = expense.get('user_name', "")
                category = expense.get('category', "")
                subcategory = expense.get('subcategory', "")
                expense_type = expense.get('transaction_type', "Credit")
                amount = expense.get('amount', 0.0)
                note = expense.get('notes', "")
            else:
                name = ""
                category = ""
                subcategory = ""
                expense_type = "Credit"
                amount = 0.0
                note = ""

            # Input fields for each row
            col1, col2, col3, col4, col5, col6 = st.columns(6)
            with col1:
                name_options = ['Alice', 'Bob', 'Emily', 'Mark']
                name_index = name_options.index(
                    name) if name in name_options else 0  # Default to the first option
                name = st.selectbox(
                    "Name",
                    name_options,
                    index=name_index,
                    key=f"name_{i}",
                    label_visibility="collapsed"
                )

            with col2:
                category_index = list(Category.keys()).index(category) if category in Category else 0
                category = st.selectbox(
                    "Category",
                    list(Category.keys()),
                    index=category_index,
                    key=f"category_{i}",
                    label_visibility="collapsed"
                )
            with col3:
                subcategory = st.text_input(
                    "Subcategory",
                    value=subcategory,
                    key=f"subcategory_{i}",
                    label_visibility="collapsed"
                )
            with col4:
                expense_type_index = ['Credit', 'Debit'].index(expense_type) if expense_type in ['Credit',
                                                                                                 'Debit'] else 0
                expense_type = st.selectbox(
                    "Type",
                    ['Credit', 'Debit'],
                    index=expense_type_index,
                    key=f"type_{i}",
                    label_visibility="collapsed"
                )
            with col5:
                amount = st.number_input(
                    "Amount",
                    min_value=0.0,
                    step=1.0,
                    value=amount,
                    key=f"amount_{i}",
                    label_visibility="collapsed"
                )
            with col6:
                note = st.text_input(
                    "Notes",
                    value=note,
                    key=f"note_{i}",
                    label_visibility="collapsed"
                )
            expenses.append({
                'user_name': name,  # Ensure the API expects this key
                'category': category,
                'subcategory': subcategory,
                'transaction_type': expense_type,
                'amount': amount,
                'notes': note
            })

        # Form submission
        submit_button = st.form_submit_button("Submit")
        if submit_button:
            filtered_expense = [expense for expense in expenses if expense['amount'] > 0]

            # Send the data as a list of dictionaries, but ensure that the keys are correct
            response = requests.post(f"{API_URL}/expenses/{selected_date}", json=filtered_expense)

            # Check if the response is successful
            if response.status_code == 200:
                st.success("Expenses added successfully!")
            else:
                st.error(f"Failed to add expenses. Error: {response.text}")


        # Check if there are any rows to submit

        # submit_button = st.form_submit_button("Submit")
        # if submit_button:
        #     filtered_expense = [expense for expense in expenses if expense['Amount'] > 0]
        #     response = requests.post(f"{API_URL}/expenses/{selected_date}", json=filtered_expense)
        #     if response == 200:
        #         st.success("Expenses added successfully!")
        #     else:
        #         st.error(f"Failed to add expenses. Error: {response.text}")
#Tab 2
with tab2:
    st.subheader("Analysis")
    tableau_url = "https://prod-apnortheast-a.online.tableau.com/#/site/kunika29sept-ab6c529615/workbooks/2612569?:origin=card_share_link"

    # Display the URL as a clickable link
    st.markdown(f"[Click here for more analysis]({tableau_url})")







    #st.date_input("Add the date:", min_value=date(2020, 1, 1), max_value=date(2040, 1, 1), label_visibility="collapsed")
    #
    #     for i in range(2):
    #         #, col3, col4, col5, col6
    #         col1,col2=st.columns(2)
    #         with col1:
    #             st.selectbox("Name", ['Alice', 'Bob', 'Emily', 'Mark Lee'])
    #         with col2:
    #             st.selectbox("Category", ['Food', 'Healthcare', 'Housing', 'Income', 'Personal Care'])
    #
    # submitted = st.form_submit_button("Submit")






