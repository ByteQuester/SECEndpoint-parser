import streamlit as st
import pandas as pd

def show_data_view():
    st.header("Data View")

    # Example to load and display a CSV file
    df = pd.read_csv('BA.csv')  # Update with actual path
    st.dataframe(df)

