'''
Implement the ChatBot class to encapsulate chat functionalities.
'''
import streamlit as st
import os
import openai

from utils import ChatHelper, ChatInterface, load_data
from configs import PAGE_TITLE, PAGE_ICON, LAYOUT, INITIAL_SIDEBAR_STATE, MENU_ITEMS


class ChatBot:
    def __init__(self):
        self.configure_page()
        #self.configure_openai_api()
        self.initialize_session_state()
        self.chat_interface = ChatInterface(PAGE_TITLE, PAGE_ICON, LAYOUT, INITIAL_SIDEBAR_STATE, MENU_ITEMS)
        self.chat_helper = ChatHelper()
        self.chat_engine_instance = self.load_data()

    def configure_page(self):
        st.set_page_config(
            page_title=PAGE_TITLE,
            page_icon=PAGE_ICON,
            layout=LAYOUT,
            initial_sidebar_state=INITIAL_SIDEBAR_STATE,
            menu_items=None #MENU_ITEMS
        )

    #def configure_openai_api(self):
        #openai.api_key = OPENAI_API_KEY
        #os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

    def initialize_session_state(self):
        if "messages" not in st.session_state:
            st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I assist you today?"}]

    def load_data(self):
        return load_data()

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
        # Display chat interface
        self.chat_interface.display_chat_messages()


if __name__ == "__main__":
    chat_bot = ChatBot()
    chat_bot.run()
