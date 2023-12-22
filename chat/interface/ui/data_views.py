import streamlit as st
import pandas as pd


def show_data_view(df):
    if df is not None:
        st.dataframe(df)
    else:
        st.error("No data available for display.")
