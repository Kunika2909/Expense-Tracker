#import tab_1
import tab_1 as ae
import tab_2
import tab_3
import streamlit as st

class ExpenseTrackerApp:
    def __init__(self):
        st.set_page_config(layout="wide")

    def render_header(self):
        """Render the title and background image."""
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
                height: 100vh;
                object-fit: cover;
                opacity: 0.1;
                position: absolute;
                top: 0;
                left: 0;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="container"><img src="https://happay.com/blog/wp-content/uploads/sites/12/2022/08/non-operating-expenses.png" alt="Expense Tracker Background" class="background-image"><div class="centered-title">Expense Tracker</div></div>',
            unsafe_allow_html=True,
        )

    def render_tabs(self):
        """Render the tab navigation and load the appropriate tab."""
        st.markdown("*Current tab*")
        tab = st.selectbox(
            "Choose a Tab", 
            ["Add/Update Expense", "Analytics by category", "Dashboard"],index = 2,
            label_visibility="collapsed"
        )

        if tab == "Add/Update Expense":
            ae.AddExpense().run()
            print(st.session_state)

        elif tab == "Analytics by category":
           tab_2.MonthAnalytics().run()

        elif tab == "Dashboard":
            tab_3.Dashboard().run()
           

    def run(self):
        """Run the application."""
        self.render_header()
        self.render_tabs()

if __name__ == "__main__":
    app = ExpenseTrackerApp()
    app.run()
