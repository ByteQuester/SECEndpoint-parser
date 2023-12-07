'''
Maintain the current structure with utility functions for configuration.
'''
import streamlit as st
import openai
import os


def set_page_configuration():
    '''
    Set the page configuration for Streamlit app.
    '''
    st.set_page_config(
        page_title="Chat with the assistant",
        page_icon="🦙",
        layout="centered",
        initial_sidebar_state="auto",
        menu_items=None
    )


def set_openai_key():
    '''
    Set the OpenAI API key from Streamlit secrets.
    '''
    openai.api_key = st.secrets["openai_key"]
    os.environ["OPENAI_API_KEY"] = st.secrets["openai_key"]