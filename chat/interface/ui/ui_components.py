import streamlit as st


class UIComponents:
    def __init__(self):
        # Any initialization if needed
        pass

    def select_cik_number(self, cik):
        return st.sidebar.selectbox("Select CIK Number", cik)

    def select_query_type(self, query_types):
        return st.sidebar.selectbox("Select Query Type", query_types)

    def select_date_range(self):
        return st.sidebar.date_input("Select Date Range")

    def submit_button(self):
        return st.sidebar.button("Submit")

