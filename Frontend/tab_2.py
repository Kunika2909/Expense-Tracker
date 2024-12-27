import requests
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date, timedelta, datetime



API_URL = "http://127.0.0.1:8000"

def tab_2():
    response_min = requests.get(f"{API_URL}/min_date")
    min = response_min.json() #returns the string 

    response_max = requests.get(f"{API_URL}/max_date")
    max = response_max.json() #returns the string
    

#converting string min and max to date
    min_date = datetime.strptime(min, "%Y-%m-%d").date()
    max_date = datetime.strptime(max, "%Y-%m-%d").date()

    col1,col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start", min_value=min_date, max_value= max_date - timedelta(days = 1), label_visibility="collapsed")
    with col2:
        end_date = st.date_input("End", min_value=min_date + timedelta(days=1), max_value=max_date, label_visibility="collapsed")
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