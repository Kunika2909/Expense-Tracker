import requests
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date, timedelta, datetime

class MonthAnalytics:
        def __init__(self):
                self.url = "http://127.0.0.1:8000"
                self.max_date = None
                self.min_date = None
                self.df = None

        def min_max(self):
            response_min = requests.get(f"{self.url}/min_date")
            min = response_min.json() #returns the string 
            response_max = requests.get(f"{self.url}/max_date")
            max = response_max.json() #returns the string

            self.min_date = datetime.strptime(min, "%Y-%m-%d").date()
            self.max_date = datetime.strptime(max, "%Y-%m-%d").date()
            
        
        def fetch_row_1(self):
            col1,col2= st.columns(2)
            with col1:
                   start_date = st.date_input("Start", min_value=self.min_date, max_value= self.max_date - timedelta(days = 1), label_visibility="collapsed")
            
            with col2:
                   end_date = st.date_input("End", min_value=self.min_date + timedelta(days=1), max_value=self.max_date, label_visibility="collapsed")
            return start_date,end_date
        
        
        def get_analytics(self,start_date,end_date):
                payload = {
                        "start_date": start_date.strftime("%Y-%m-%d"),
                        "end_date": end_date.strftime("%Y-%m-%d")
                }
                response = requests.post(f"{self.url}/analytics",json = payload)
                response_data = response.json()
                self.fetch_request(response_data)
        
        
               
                # if response.status_code == 200:
                #     print("Success")
                #     data_for_table = []
                #     for category,values in response_data.items():
                #         data_for_table.append({
                #             "Category": category,
                #             "Total": values["Total"],
                #             "Percent%": values["Percent%"]
                #         })
                #     df = pd.DataFrame(data_for_table).sort_values(by="Total",ascending=False)
                #     df.set_index('Category',inplace=True)
                #     self.df = df
                
                
        def fetch_request(self,data):
                data_for_table = []
                for category,values in data.items():
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


        def run(self):
            #st.markdown("**Analytics**")
            self.min_max()
            start, end = self.fetch_row_1()
            button = st.button("Get Analytics")

            if button:
                 self.get_analytics(start,end)
                
                                
              


if __name__ == "__name__":
      month_analytics = MonthAnalytics()
      month_analytics.run()

      
        
        

            

                      
                  
               
               

          
                       
                       
                
                
                            

        



    
