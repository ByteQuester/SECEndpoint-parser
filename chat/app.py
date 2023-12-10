'''
Ensure it integrates smoothly with the new ChatInterface and ChatHelper classes.
'''
import streamlit as st
import os
import openai

from chat.utils import ChatHelper, ChatInterface, load_data
from chat.configs import PAGE_TITLE, PAGE_ICON, LAYOUT, OPENAI_API_KEY, INITIAL_SIDEBAR_STATE, MENU_ITEMS


def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I assist you today?"}]


def main():
    # Set Streamlit page configuration
    st.set_page_config(
        page_title=PAGE_TITLE,
        page_icon=PAGE_ICON,
        layout=LAYOUT,
        initial_sidebar_state=INITIAL_SIDEBAR_STATE,
        menu_items=MENU_ITEMS
    )

    # Set OpenAI API key
    openai.api_key = OPENAI_API_KEY
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

    # Initialize session state
    initialize_session_state()

    # Initialize ChatInterface with Streamlit configuration
    chat_interface = ChatInterface(PAGE_TITLE, PAGE_ICON, LAYOUT, INITIAL_SIDEBAR_STATE, MENU_ITEMS)

    # Load data for the chat engine (if required)
    chat_engine_instance = load_data()  # Assuming load_data doesn't require config as an argument anymore

    # Handle user input
    prompt = st.chat_input("Your question")
    if prompt and prompt.strip() != "":
        # Append the user's message
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Generate and append the chatbot's response using ChatHelper
        chat_helper = ChatHelper()
        chat_response = chat_helper.generate_response(chat_engine_instance, prompt)
        st.session_state.messages.append({"role": "assistant", "content": chat_response})

    # Display chat interface
    chat_interface.display_chat_messages()


main()
