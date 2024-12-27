def tab_3():
    import streamlit as st
    import pandas as pd
    import numpy as np
    import plotly.express as px
    import seaborn as sns
    import matplotlib.pyplot as plt
    from sqlalchemy import create_engine
    import calendar
    

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

