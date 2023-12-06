import streamlit as st
from utils import config, helpers, chat_interface, data_loader


def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I assist you today?"}]



def main():
    # Config
    config.set_page_configuration()
    config.set_openai_key()

    # Initialize session state
    initialize_session_state()

    # Load data
    chat_engine_instance = data_loader.load_data()

    # Handle user input
    prompt = st.chat_input("Your question")
    if prompt and prompt.strip() != "":  # Check if there's valid user input
        # First, append the user's message
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Then, generate and append the chatbot's response
        helpers.generate_response(chat_engine_instance, prompt)


    # Display chat interface
    chat_interface.display_chat_messages()

main()