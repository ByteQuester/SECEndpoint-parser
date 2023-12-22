'''
Implement the ChatBot class to encapsulate chat functionalities.
'''
import streamlit as st

from .utils import ChatHelper
from .interface.app_interface import AppInterface
from .configs import PAGE_TITLE, PAGE_ICON, INITIAL_SIDEBAR_STATE, MENU_ITEMS, LAYOUT



class ChatBot:
    def __init__(self, chat_engine_instance):
        self.initialize_session_state()
        self.chat_helper = ChatHelper()
        self.chat_engine_instance = chat_engine_instance
        self.chat_interface = AppInterface(PAGE_TITLE, PAGE_ICON, INITIAL_SIDEBAR_STATE, MENU_ITEMS, LAYOUT)



    def initialize_session_state(self):
        if "messages" not in st.session_state:
            st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I assist you today?"}]

    def run(self):
        prompt = st.chat_input("Your question")
        if prompt and prompt.strip() != "":
            st.session_state.messages.append({"role": "user", "content": prompt})
            chat_response = self.chat_helper.generate_response(self.chat_engine_instance, prompt)
            if chat_response is not None:
                st.session_state.messages.append({"role": "assistant", "content": chat_response})
            else:
                st.session_state.messages.append(
                    {"role": "assistant", "content": "I'm sorry, I couldn't generate a response."})
        self.chat_interface.display_chat_messages()

