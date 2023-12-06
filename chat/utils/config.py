import streamlit as st
import openai
import os


def set_page_configuration():
    st.set_page_config(page_title="Chat with the assitant",
                       page_icon="🦙",
                       layout="centered",
                       initial_sidebar_state="auto",
                       menu_items=None)


def set_openai_key():
    # Directly set the openai.api_key from Streamlit secrets
    openai.api_key = st.secrets["openai_key"]

    # Set the OpenAI API key as an environment variable
    os.environ["OPENAI_API_KEY"] = st.secrets["openai_key"]

