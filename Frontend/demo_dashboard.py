import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import calendar

st.set_page_config(layout="wide")
# Database Connection
@st.cache_resource
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





# Streamlit App

























# Filters

st.sidebar.header("Filters")
selected_year = st.sidebar.selectbox("Year", options=data['transaction_date'].dt.year.unique())
selected_month = st.sidebar.selectbox("Month", options=data['transaction_date'].dt.month_name().unique())

# # # Filter data based on selections
filtered_data = data[
    (data['transaction_date'].dt.year == selected_year) &
    (data['transaction_date'].dt.month_name() == selected_month)
]
st.title(f"Expense dashboard - {selected_year} | {selected_month}")
# KPI Calculation
#total earning
Total_earning = filtered_data[filtered_data["transaction_type"]=="Credit"]["amount"].sum()
#total spending
Total_spending = filtered_data[filtered_data["transaction_type"]=="Debit"]["amount"].sum()
#net balance
Net_balance = Total_earning-Total_spending
col1,col2,col3 = st.columns(3)
with col1:
    st.header("Total Earning")
    st.subheader(f"₹{Total_earning:,.2f}")
with col2:
    st.header("Total Spending")
    st.subheader(f"₹{Total_spending:,.2f}")
with col3:
    st.header("Net Balance")
    st.subheader(f"₹{Net_balance:,.2f}")

















data_frame = filtered_data.groupby("user_name")["amount"].sum().reset_index()
data_frame = data_frame.sort_values(by="amount", ascending=True)
fig = px.bar(
    data_frame=data_frame,
    x='amount',  # X-axis (amount)
    y='user_name',  # Y-axis (category)
    orientation='h',  # Horizontal orientation
    title="Who spend the most ?"

)
fig.update_layout(
    height=300,  # Adjust height
    width=600,   # Adjust width
    margin=dict(l=50, r=50, t=50, b=50)  # Adjust margins to give some space
)



# Display the chart in Streamlit
st.plotly_chart(fig)


col1,col2 = st.columns(2)
with col1:
    st.subheader(f" Expense Distribution by Category")


    category_data = filtered_data[filtered_data['category'] != 'Income'].groupby('category', as_index=False)['amount'].sum()



    #st.write("Category Data:", category_data)


    print(filtered_data)
    fig_pie = px.pie(
        category_data,
        values='amount',
        names='category',
        title=f"Category-wise Expense Distribution - {selected_month}"
    )
    st.plotly_chart(fig_pie)


#heatmap
with col2:
    st.subheader("Expense Heatmap Calendar")                                                                                      
                                                                                                                                  
                                                                                                                                  
                                                                                                                                  
    # Group by the day of the month and sum the expenses                                                                          
                                                                                                                                  
    filtered_data['day'] = filtered_data['transaction_date'].dt.day                                                               
                                                                                                                                  
    daily_expenses = filtered_data[filtered_data['category'] != 'Income'].groupby('day')['amount'].sum().reset_index()            
                                                                                                                                  
                                                                                                                                  
                                                                                                                                  
    # Fill missing days with zero if there's no transaction on that day                                                           
                                                                                                                                  
    all_days = pd.DataFrame({'day': np.arange(1, 32)})  # All possible days in a month (1-31)                                     
                                                                                                                                  
    daily_expenses = pd.merge(all_days, daily_expenses, on='day', how='left').fillna(0)                                           
                                                                                                                                  
                                                                                                                                  
                                                                                                                                  
    # Get the month and year for the title                                                                                        
                                                                                                                                  
    month_name = selected_month                                                                                                   
                                                                                                                                  
    month_year = f"{month_name} {selected_year}"                                                                                  
                                                                                                                                  
                                                                                                                                  
                                                                                                                                  
    # Prepare the heatmap data: Reshape data into a 5-week format (7 days per week)                                               
                                                                                                                                  
    heatmap_data = daily_expenses['amount'].values
                                                                                                                                  
                                                                                                                                  
                                                                                                                                  
    # Adjust number of rows (weeks) dynamically based on the number of days in the month                                          
                                                                                                                                  
    num_days = len(daily_expenses)                                                                                                
                                                                                                                                  
    num_weeks = int(np.ceil(num_days / 7))  # Calculate number of weeks based on the days                                         
                                                                                                                                  
    heatmap_data = np.pad(heatmap_data, (0, num_weeks * 7 - num_days), mode='constant', constant_values=0)                        
                                                                                                                                  
    heatmap_data = heatmap_data.reshape(num_weeks, 7)                                                                             
                                                                                                                                  
                                                                                                                                  
                                                                                                                                  
    # Create the calendar heatmap using Plotly                                                                                    
                                                                                                                                  
    fig_calendar = px.imshow(                                                                                                     
                                                                                                                                  
        heatmap_data,                                                                                                             
                                                                                                                                  
        color_continuous_scale=['white', 'red'],                                                                                  
                                                                                                                                  
        labels={'color': 'Total Expense'},                                                                                        
                                                                                                                                  
        title=f"Expense Heatmap - {month_year}",                                                                                  
                                                                                                                                  
        text_auto=False  # Automatically add the text showing the expense for each day                                            
                                                                                                                                  
    )                                                                                                                             
                                                                                                                                  
                                                                                                                                  
                                                                                                                                  
    # Customize the layout of the heatmap to align with a calendar view                                                           
                                                                                                                                  
    fig_calendar.update_layout(                                                                                                   
                                                                                                                                  
        xaxis=dict(tickmode='array', tickvals=np.arange(7), ticktext=['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']),          
                                                                                                                                  
        yaxis=dict(tickvals=np.arange(num_weeks), ticktext=[f"Week {i+1}" for i in range(num_weeks)]),                            
                                                                                                                                  
        coloraxis_showscale=True                                                                                                  
                                                                                                                                  
    )                                                                                                                             
                                                                                                                                  
    for i in range(num_weeks):                                                                                                    
                                                                                                                                  
        for j in range(7):                                                                                                        
                                                                                                                                  
            # Get the index for the day in the calendar                                                                           
                                                                                                                                  
            day_index = i * 7 + j                                                                                                 
            # Show the heatmap in the Streamlit app                                                                               
            if day_index < len(daily_expenses):                                                                                   
                day_value = int(daily_expenses.iloc[day_index]['day']  )                                                          
                fig_calendar.add_annotation(                                                                                      
                                x=j,                                                                                              
                    y=i,                                                                                                          
                    text=str(day_value),                                                                                          
                    showarrow=False,                                                                                              
                    font=dict(size=12, color="black"),                                                                            
                    align="center"                                                                                                
                )                                                                                                                 
                                                                                                                                  
    st.plotly_chart(fig_calendar)                                                                                                 


