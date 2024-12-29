import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import calendar


class Dashboard:
    def __init__(self):
        self.db_url = "mysql+pymysql://root:@127.0.0.1:3306/Expense_tracking"
        self.engine = create_engine(self.db_url)
        self.data = self.load_data()
        

    def load_data(self):
        query = """SELECT * FROM transactions;"""
        data = pd.read_sql(query, self.engine)
        data['transaction_date'] = pd.to_datetime(data['transaction_date'], errors='coerce')  # Ensure date is datetime
        return data
    
    def refreshing_data(self):
        st.cache_data.clear() # clearing the cache data
        self.data = self.load_data()
        st.success("Data refreshed!")

    def filtering_data(self,year,month):
         # # # Filter data based on selections
        filtered_data = self.data[
            (self.data['transaction_date'].dt.year == year) &
            (self.data['transaction_date'].dt.month_name() == month)
            ]
        return filtered_data
    
    def kpi_calculation(self,filtered_data):
        Total_earning = filtered_data[filtered_data["transaction_type"] == "Credit"]["amount"].sum()
        # total spending
        Total_spending = filtered_data[filtered_data["transaction_type"] == "Debit"]["amount"].sum()
        # net balance
        Net_balance = Total_earning - Total_spending
        # Display KPIs
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
    def user_spend(self,filtered_data):
        filtered_transactions = filtered_data[filtered_data['category'] != 'Income']
        data_frame = filtered_transactions.groupby("user_name")["amount"].sum().reset_index()
        data_frame = data_frame.sort_values(by="amount", ascending=True)
        fig = px.bar(
            data_frame=data_frame,
            x='amount',  # X-axis (amount)
            y='user_name',  # Y-axis (category)
            orientation='h',  # Horizontal orientation
            title="Who spend the most ?",
            color = "amount"
            #color_continuous_scale=["white","red"]
    
    
    
    



        )
        fig.update_layout(
        yaxis=dict(title=None) ,
        xaxis = dict(title = None)) # This will hide the y-axis  and x- axis title 



        fig.update_layout(

            height=300,  # Adjust height
            width=600,  # Adjust width
            margin=dict(l=50, r=50, t=50, b=50),  # Adjust margins to give some space
            
        )
        # Display the chart in Streamlit
        st.plotly_chart(fig)


    def category_distribution(self,filtered_data):

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
    
    def calender(self,filtered_data,selected_year,selected_month):
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

    def run(self):
        import datetime
        if 'data' not in st.session_state:
            st.session_state['data'] = self.load_data()
            st.session_state['data'] = self.data
        
        button = st.button("Refresh Data")
        if button:
            self.refreshing_data()
            st.session_state['data'] = self.data
        
        st.sidebar.header("Filters")
        current_year = datetime.datetime.now().year
        current_month = pd.Timestamp.today().strftime('%B').strip()

        selected_year = st.sidebar.selectbox("Year", options=self.data['transaction_date'].dt.year.unique(),index=list(self.data['transaction_date'].dt.year.unique()).index(current_year))
        selected_month = st.sidebar.selectbox("Month", options=self.data['transaction_date'].dt.month_name().unique(),index = list(self.data['transaction_date'].dt.month_name().unique()).index(current_month))
        st.header(f"Dashboard - {selected_month} | {selected_year}")

        filtered_data = self.filtering_data(selected_year,selected_month)

        col1,col2 = st.columns(2)
        with col1:
            self.user_spend(filtered_data)
        with col2:
            self.kpi_calculation(filtered_data)
        col1,col2 = st.columns(2)
        with col1:
            self.category_distribution(filtered_data)
        with col2:
            self.calender(filtered_data,selected_year,selected_month)
    

if __name__ == "main":
    dashboard = Dashboard()
    dashboard.run()






    



   
   