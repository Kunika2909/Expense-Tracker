import requests
import streamlit as st
from datetime import date
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


#setting the page configuration as wide

st.set_page_config(layout="wide")

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

#local host url
API_URL = "http://127.0.0.1:8000"


#tab1, tab2,tab3= st.tabs(["Add/Update", "Analytics by category","Analytics by month"])
st.markdown("*Current tab*")
tab = st.selectbox("Choose a Tab", ["Add/Update Expense", "Analytics by category", "Dashboard"],label_visibility="collapsed")
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
    def load_data():
        response = requests.get(f"{API_URL}/expenses/{selected_date}")
        if response.status_code == 200:
            try:
                existing_expenses = response.json()
                # If the response is None, return an empty list
                if existing_expenses is None:
                    st.warning("No expenses data found.")
                    return []
                print(existing_expenses);
                return existing_expenses
            except ValueError:
                st.error("Error decoding JSON response from the server.")
                return []
        else:
            # Handle failed response
            st.error(f"Failed to fetch expenses. Status code: {response.status_code}")
            return []


    if f"expenses_{selected_date}" not in st.session_state:
        st.session_state[f"expenses_{selected_date}"] = load_data()






    # Initialize session state for rows and expenses
    expenses = st.session_state.get(f"expenses_{selected_date}", [])
    #st.write(expenses)

    # Toggle button for showing/hiding the add expense form
    if "show_add_expense" not in st.session_state:
        st.session_state["show_add_expense"] = False



    # Display existing expenses
    #st.markdown("### Existing Expenses")
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

    # Iterate over rows
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

        # Ensure that the button is outside the loop

    # Toggle button to show/hide the form
    toggle_button_label = "Hide Form" if st.session_state["show_add_expense"] else "Add New Expense"
    if st.button(toggle_button_label):
        st.session_state["show_add_expense"] = not st.session_state["show_add_expense"]

    # Show form only when toggled
    if st.session_state["show_add_expense"]:
        #st.markdown("### Add New Expense")
        col1, col2, col3, col4, col5, col6 = st.columns([1.5, 2, 2, 1.5, 2, 2])

        with col1:
            new_name = st.selectbox("", [''] + ['Alice', 'Bob', 'Emily', 'Mark'], key="new_name")
        with col2:
            new_category = st.selectbox("", [''] + list(categories.keys()), key="new_category")
        with col3:
            new_subcategory = st.text_input("", key="new_subcategory")
        with col4:
            new_amount = st.number_input("",min_value=0.0, step=1.0,value=None, key="new_amount")
        with col5:
            new_type = st.selectbox("", [''] + ["Credit", "Debit"], key="new_type")
        with col6:
            new_notes = st.text_input("", key="new_notes")

        if st.button("Insert Row"):
            # Validate inputs
            if new_name and new_category and new_amount > 0:
                new_expense = [{
                    'user_name': new_name,
                    'category': new_category,
                    'subcategory': new_subcategory,
                    'amount': new_amount,
                    'transaction_type': new_type,
                    'notes': new_notes,
                }]


                response = requests.post(f"{API_URL}/expenses/{selected_date}", json=new_expense)

                # Check the response status
                if response.status_code == 200:
                    st.success("Expense submitted successfully!")
                    st.session_state[f"expenses_{selected_date}"] = load_data()

                    #st.session_state.expenses = load_expenses()  # Save updated data to session state
                    #st.session_state[f"expenses_{selected_date}"].append(new_expense[0])

                    # Rerun the app to reflect the updated data
                    #st.rerun()  # Refresh the app to reflect the updated data
                else:
                    st.error(f"Failed to submit expense. Error: {response.text}")

            else:
                st.warning(f"Please enter the data")



                # Reload the expenses data after successful insertion
                    # You can use the session_state to store the expenses

    if rows_to_delete and st.button("Delete Selected Rows"):
        response = requests.delete(f"{API_URL}/expenses/{selected_date}/delete",
                                   json={"transaction_id": rows_to_delete})
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

            # After deletion, re-render the page to reflect updated data
        st.session_state[f"expenses_{selected_date}"] = [
            expense for i, expense in enumerate(st.session_state[f"expenses_{selected_date}"])
            if i not in rows_to_delete]

            # Send delete request with transaction_ids in the request body


if tab == "Analytics by category":
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Start Date**")
    with col2:
        st.markdown("**End Date**")

    col1,col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start", min_value=date(2020, 1, 1), max_value=date(2030, 1, 1), label_visibility="collapsed")
    with col2:
        end_date = st.date_input("End", min_value=date(2020, 1, 1), max_value=date(2030, 1, 1), label_visibility="collapsed")
    if st.button("Get analytics"):
        payload = {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d")
        }
        response = requests.post(f"{API_URL}/analytics",json = payload)
        response_data = response.json()
        if response.status_code == 200:
            data_for_table = []
            for category,values in response_data.items():
                data_for_table.append({
                    "Category": category,
                    "Total": values["Total"],
                    "Percent%": values["Percent%"]
                })
            df = pd.DataFrame(data_for_table).sort_values(by="Total",ascending=False)
            df.set_index('Category',inplace=True)
            col1,col2 = st.columns(2)
            with col1:
                st.dataframe(df)


            with col2:
                fig, ax = plt.subplots()
                ax.pie(df['Total'], labels=df.index, autopct='%1.1f%%', startangle=90,textprops={'color': 'Black'},
                       colors=['#FF6347', '#2E8B57', '#ff0080',
                               '#FFD700','#3364ff'], wedgeprops={'width': 0.55})  # New colors (Tomato, SeaGreen, DodgerBlue, Gold)
                ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
                ax.set_facecolor('white')
                fig.patch.set_facecolor('white')

                # Display the Pie Chart in Streamlit
                st.pyplot(fig)

        st.success("success")
if tab =="Dashboard":
    # #importing necessary modules
    # import streamlit as st
    # import pandas as pd
    # import numpy as np
    # import plotly.express as px
    # import mysql.connector
    # import seaborn as sns
    # import matplotlib.pyplot as plt
    # from sqlalchemy import create_engine
    # import calendar

    import streamlit as st
    import pandas as pd
    import numpy as np
    import plotly.express as px
    import seaborn as sns
    import matplotlib.pyplot as plt
    from sqlalchemy import create_engine
    import calendar

    #st.set_page_config(layout="wide")


    # Database Connection
    @st.cache_data
    def load_data_from_db():
        # Replace with your database connection details
        db_url = "mysql+pymysql://root:@127.0.0.1:3306/Expense_tracking"

        engine = create_engine(db_url)

        query = """
        SELECT *

        FROM transactions;
        """
        data = pd.read_sql(query, engine)
        data['transaction_date'] = pd.to_datetime(data['transaction_date'], errors='coerce')  # Ensure date is datetime
        return data


    # Load data
    data = load_data_from_db()


    # Database Connection
    # @st.cache_data #caching of data
    #
    # def load_data_from_db():
    #     # Replace with your database connection details
    #     db_url = "mysql+pymysql://root@127.0.0.1:3306/Expense_tracking"
    #
    #     engine = create_engine(db_url)
    #
    #     query = """
    #     SELECT *
    #
    #     FROM transactions;
    #     """
    #     data = pd.read_sql(query,engine)
    #     data['transaction_date'] = pd.to_datetime(data['transaction_date'], errors='coerce')  # Ensure date is datetime
    #     return data
    #
    #
    # # Load data
    # data = load_data_from_db()

    #Refresh button
    if st.button("Refresh Data"):
        st.cache_data.clear() # clearing the cache data
        st.session_state['data'] = load_data_from_db() #load the data
        st.success("Data refreshed!")
    if 'data' not in st.session_state:
        st.session_state['data'] = load_data_from_db()  # Load data for the first time
    data = st.session_state['data']



    # Filters

    st.sidebar.header("Filters")
    selected_year = st.sidebar.selectbox("Year", options=data['transaction_date'].dt.year.unique())
    selected_month = st.sidebar.selectbox("Month", options=data['transaction_date'].dt.month_name().unique())

    # # # Filter data based on selections
    filtered_data = data[
        (data['transaction_date'].dt.year == selected_year) &
        (data['transaction_date'].dt.month_name() == selected_month)
        ]
    st.header(f"Dashboard - {selected_year} | {selected_month}")

    # KPI Calculation
    # Total earning
    Total_earning = filtered_data[filtered_data["transaction_type"] == "Credit"]["amount"].sum()
    # total spending
    Total_spending = filtered_data[filtered_data["transaction_type"] == "Debit"]["amount"].sum()
    # net balance
    Net_balance = Total_earning - Total_spending
    filtered_transactions = filtered_data[filtered_data['category'] != 'Income']

    col1, col2 = st.columns(2)
    with col1:
        data_frame = filtered_transactions.groupby("user_name")["amount"].sum().reset_index()
        data_frame = data_frame.sort_values(by="amount", ascending=True)
        fig = px.bar(
            data_frame=data_frame,
            x='amount',  # X-axis (amount)
            y='user_name',  # Y-axis (category)
            orientation='h',  # Horizontal orientation
            title="Who spend the most ?",
            color_continuous_scale=["white","red"]



        )
        fig.update_layout(

            height=300,  # Adjust height
            width=600,  # Adjust width
            margin=dict(l=50, r=50, t=50, b=50)  # Adjust margins to give some space
        )

        # Display the chart in Streamlit
        st.plotly_chart(fig)

    with col2:


        empty_col1, col1, col2, col3, empty_col2 = st.columns([1, 9, 9, 9, 1])
        with col1:
            st.text("Total Earning")
            st.subheader(f"₹{Total_earning:,.1f}")
        with col2:
            st.text("Total Spending")
            st.subheader(f"₹{Total_spending:,.1f}")
        with col3:
            st.text("Net Balance")
            st.subheader(f"₹{Net_balance:,.1f}")










    col1, col2 = st.columns(2)
    with col1:
        #st.subheader(f" Expense Distribution by Category")

        category_data = filtered_data[filtered_data['category'] != 'Income'].groupby('category', as_index=False)[
            'amount'].sum()

        # st.write("Category Data:", category_data)

        print(filtered_data)
        fig_pie = px.pie(
            category_data,
            values='amount',
            names='category',
            title=f"Category-wise Expense Distribution"
        )
        st.plotly_chart(fig_pie)

    # heatmap
    with col2:
        import calendar
        import numpy as np
        import pandas as pd
        import plotly.express as px
        import streamlit as st

        # Month name to number conversion
        month_name_to_number = {month: i + 1 for i, month in enumerate(calendar.month_name[1:])}

        # Convert selected_month to numeric if given as a name
        if isinstance(selected_month, str):
            selected_month = month_name_to_number[selected_month]

        # Ensure selected_year is an integer
        selected_year = int(selected_year)

        # Get the first weekday and number of days in the selected month
        first_weekday, month_days = calendar.monthrange(selected_year, selected_month)
        first_weekday = (first_weekday + 1) % 7

        # Create a DataFrame for all days in the month
        all_days = pd.DataFrame({'day': np.arange(1, month_days + 1)})

        # Filter out income category and group expenses by day
        filtered_data['day'] = filtered_data['transaction_date'].dt.day
        daily_expenses = filtered_data[filtered_data['category'] != 'Income'].groupby('day')[
            'amount'].sum().reset_index()

        # Merge daily expenses with all days and fill missing values with 0
        daily_expenses = pd.merge(all_days, daily_expenses, on='day', how='left').fillna(0)

        # Prepare the heatmap data
        heatmap_data = daily_expenses['amount'].values

        # Pad the start of the heatmap to align with the first weekday
        heatmap_data = np.pad(heatmap_data, (first_weekday, 0), mode='constant', constant_values=0)

        # Calculate the total number of rows (weeks) required
        num_days = len(heatmap_data)
        num_weeks = int(np.ceil(num_days / 7))

        # Pad the end of the heatmap to make a complete grid
        heatmap_data = np.pad(heatmap_data, (0, num_weeks * 7 - num_days), mode='constant', constant_values=0)
        heatmap_data = heatmap_data.reshape(num_weeks, 7)

        # Create the calendar heatmap using Plotly
        fig_calendar = px.imshow(
            heatmap_data,
            color_continuous_scale=['white', 'red'],
            labels={'color': 'Total Expense'},
            title=f"Debit Flow Calendar",
            text_auto=False
        )

        # Customize the layout
        fig_calendar.update_layout(
            xaxis=dict(
                tickmode='array',
                tickvals=np.arange(7),
                ticktext=['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
            ),
            yaxis=dict(
                tickmode='array',
                tickvals=np.arange(num_weeks),
                ticktext=[f"Week {i + 1}" for i in range(num_weeks)]
            ),
            coloraxis_showscale=True
        )

        # Add annotations for each day in the month
        for i in range(num_weeks):
            for j in range(7):
                day_index = i * 7 + j
                day_value = day_index - first_weekday + 1  # Calculate the actual day of the month
                if 1 <= day_value <= month_days:
                    fig_calendar.add_annotation(
                        x=j,
                        y=i,
                        text=str(day_value),
                        showarrow=False,
                        font=dict(size=12, color="black"),
                        align="left"
                    )

        # Show the calendar heatmap in Streamlit
        st.plotly_chart(fig_calendar)

        # import calendar
        # import numpy as np
        # import pandas as pd
        # import plotly.express as px
        # import streamlit as st
        #
        # # Month name to number conversion
        # month_name_to_number = {month: i + 1 for i, month in enumerate(calendar.month_name[1:])}
        #
        # # Ensure selected_month is a number, even if it's given as a month name
        # if isinstance(selected_month, str):
        #     selected_month = month_name_to_number[selected_month]  # Convert month name to number
        #
        # # Ensure selected_month and selected_year are integers
        # selected_year = int(selected_year)
        #
        # # Step 1: Get the number of days and the weekday of the first day of the selected month
        # first_weekday, month_days = calendar.monthrange(selected_year, selected_month)
        #
        # # Step 2: Update the all_days DataFrame to match the number of days in the selected month
        # all_days = pd.DataFrame({'day': np.arange(1, month_days + 1)})
        #
        # # Filter data for the selected month and remove 'Income' category
        # filtered_data['day'] = filtered_data['transaction_date'].dt.day
        # daily_expenses = filtered_data[filtered_data['category'] != 'Income'].groupby('day')[
        #     'amount'].sum().reset_index()
        #
        # # Step 3: Merge with all days and fill missing days with zero
        # daily_expenses = pd.merge(all_days, daily_expenses, on='day', how='left').fillna(0)
        #
        # # Step 4: Get the month and year for the title
        # month_name = calendar.month_name[selected_month]
        # month_year = f"{month_name} {selected_year}"
        #
        # # Step 5: Prepare the heatmap data (reshape it for a 5-week calendar view)
        # heatmap_data = daily_expenses['amount'].values
        #
        # # Adjust number of rows (weeks) dynamically based on the number of days in the month
        # num_days = len(daily_expenses)
        # num_weeks = int(np.ceil(num_days / 7))
        #
        # # Pad the data to ensure it fills up a full grid (e.g., 5 weeks if needed)
        # heatmap_data = np.pad(heatmap_data, (0, num_weeks * 7 - num_days), mode='constant', constant_values=0)
        # heatmap_data = heatmap_data.reshape(num_weeks, 7)
        #
        # # Step 6: Create the calendar heatmap using Plotly
        # fig_calendar = px.imshow(
        #     heatmap_data,
        #     color_continuous_scale=['white', 'red'],
        #     labels={'color': 'Total Expense'},
        #     title=f"Debit Flow Calendar - {month_year}",
        #     text_auto=False
        # )
        #
        # # Customize the layout to align with a calendar view
        # fig_calendar.update_layout(
        #     xaxis=dict(tickmode='array', tickvals=np.arange(7),
        #                ticktext=['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']),
        #     yaxis=dict(tickvals=np.arange(num_weeks), ticktext=[f"Week {i + 1}" for i in range(num_weeks)]),
        #     coloraxis_showscale=True
        # )
        #
        # # Add annotations for the days of the month
        # for i in range(num_weeks):
        #     for j in range(7):
        #         day_index = i * 7 + j
        #         if day_index < len(daily_expenses):
        #             day_value = int(daily_expenses.iloc[day_index]['day'])
        #
        #             # Adjust the x-position based on the first weekday of the month
        #             # If the first day of the month is not Sunday, shift the annotations accordingly
        #             if j >= first_weekday:
        #                 fig_calendar.add_annotation(
        #                     x=j - first_weekday,
        #                     y=i,
        #                     text=str(day_value),
        #                     showarrow=False,
        #                     font=dict(size=12, color="black"),
        #                     align="center"
        #                 )
        #             else:
        #                 fig_calendar.add_annotation(
        #                     x=j + (7 - first_weekday),
        #                     y=i,
        #                     text=str(day_value),
        #                     showarrow=False,
        #                     font=dict(size=12, color="black"),
        #                     align="center"
        #                 )
        #
        # # Show the calendar heatmap
        # st.plotly_chart(fig_calendar)

        # e.weekday()
        #
        # # Get the total number of days in the month
        # num_days_in_month = (month_end_date - month_start_date).days + 1
        #
        # # Continue with the rest of the code...
        #
        # # Convert selected_month and selected_year to integers if they're strings
        #
        # # Group by the day of the month and sum the expenses
        # filtered_data['day'] = filtered_data['transaction_date'].dt.day
        #
        # # Filter out 'Income' category and group by 'day' to get daily expenses
        # daily_expenses = filtered_data[filtered_data['category'] != 'Income'].groupby('day')[
        #     'amount'].sum().reset_index()
        #
        # # Fill missing days with zero if there's no transaction on that day
        # all_days = pd.DataFrame({'day': np.arange(1, num_days_in_month + 1)})  # All possible days in the month
        #
        # daily_expenses = pd.merge(all_days, daily_expenses, on='day', how='left').fillna(0)
        #
        # # Prepare the heatmap data: Reshape data into a 5-week format (7 days per week)
        # heatmap_data = daily_expenses['amount'].values
        #
        # # Adjust number of rows (weeks) dynamically based on the number of days in the month
        # num_weeks = int(np.ceil((num_days_in_month + start_weekday) / 7))  # Calculate number of weeks
        #
        # # Pad the heatmap data to fit the full month (fill with zeros for missing days)
        # heatmap_data = np.pad(heatmap_data, (start_weekday, num_weeks * 7 - num_days_in_month - start_weekday),
        #                       mode='constant', constant_values=0)
        #
        # # Reshape the heatmap data into a 2D array of weeks and days
        # heatmap_data = heatmap_data.reshape(num_weeks, 7)
        #
        # # Create the calendar heatmap using Plotly
        # fig_calendar = px.imshow(
        #     heatmap_data,
        #     color_continuous_scale=['white', 'red'],
        #     labels={'color': 'Total Expense'},
        #     title=f"Debit Flow Calendar ({month_start_date.strftime('%B %Y')})",
        #     # Use month name and year for the title
        #     text_auto=False  # Do not automatically add text showing the expense for each day
        # )
        #
        # # Customize the layout of the heatmap to align with a calendar view
        # fig_calendar.update_layout(
        #     xaxis=dict(tickmode='array', tickvals=np.arange(7),
        #                ticktext=['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']),
        #     yaxis=dict(tickvals=np.arange(num_weeks), ticktext=[f"Week {i + 1}" for i in range(num_weeks)]),
        #     coloraxis_showscale=True
        # )
        # for i in range(num_weeks):
        #
        #
        # # Show the plot (if using Streamlit, use st.plotly_chart(fig_calendar))
        # fig_calendar.show()
        #
        # #st.subheader("Expense Heatmap Calendar")

        # Group by the day of the month and sum the expenses

        # filtered_data['day'] = filtered_data['transaction_date'].dt.day
        #
        # daily_expenses = filtered_data[filtered_data['category'] != 'Income'].groupby('day')[
        #     'amount'].sum().reset_index()
        #
        # # Fill missing days with zero if there's no transaction on that day
        #
        # all_days = pd.DataFrame(
        #     {'day': np.arange(1, 32)})  # All possible days in a month (1-31)
        #
        # daily_expenses = pd.merge(all_days, daily_expenses, on='day', how='left').fillna(0)
        #
        # # Get the month and year for the title
        #
        # month_name = selected_month
        #
        # month_year = f"{month_name} {selected_year}"
        #
        # # Prepare the heatmap data: Reshape data into a 5-week format (7 days per week)
        #
        # heatmap_data = daily_expenses['amount'].values
        #
        # # Adjust number of rows (weeks) dynamically based on the number of days in the month
        #
        # num_days = len(daily_expenses)
        #
        # num_weeks = int(np.ceil(
        #     num_days / 7))  # Calculate number of weeks based on the days
        #
        # heatmap_data = np.pad(heatmap_data, (0, num_weeks * 7 - num_days), mode='constant', constant_values=0)
        #
        # heatmap_data = heatmap_data.reshape(num_weeks, 7)
        #
        # # Create the calendar heatmap using Plotly
        #
        # fig_calendar = px.imshow(
        #
        #     heatmap_data,
        #
        #     color_continuous_scale=['white', 'red'],
        #
        #     labels={'color': 'Total Expense'},
        #
        #     title=f"Debit Flow Calender",
        #
        #     text_auto=False
        #     # Automatically add the text showing the expense for each day
        #
        # )
        #
        # # Customize the layout of the heatmap to align with a calendar view
        #
        # fig_calendar.update_layout(
        #
        #     xaxis=dict(tickmode='array', tickvals=np.arange(7),
        #                ticktext=['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']),
        #
        #     yaxis=dict(tickvals=np.arange(num_weeks), ticktext=[f"Week {i + 1}" for i in range(num_weeks)]),
        #
        #     coloraxis_showscale=True
        #
        # )
        #
        # for i in range(num_weeks):
        #
        #     for j in range(7):
        #
        #         # Get the index for the day in the calendar
        #
        #         day_index = i * 7 + j
        #         # Show the heatmap in the Streamlit app
        #         if day_index < len(daily_expenses):
        #             day_value = int(daily_expenses.iloc[day_index]['day'])
        #             fig_calendar.add_annotation(
        #                 x=j,
        #                 y=i,
        #                 text=str(day_value),
        #                 showarrow=False,
        #                 font=dict(size=12, color="black"),
        #                 align="center"
        #             )
        #
        # st.plotly_chart(fig_calendar
