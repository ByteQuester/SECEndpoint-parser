'''
Implement the ChatBot class to encapsulate chat functionalities.
'''
import streamlit as st

from chat.utils import ChatHelper


class ChatBot:
    def __init__(self, chat_engine_instance):
        self.initialize_session_state()
        self.chat_helper = ChatHelper()
        self.chat_engine_instance = chat_engine_instance

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
        # Display chat message handled by AppInterface in app.py self.chat_interface.display_chat_messages()
        # #    # Initialize the application interface
        #     app_interface = AppInterface()
        # Setup and initialize other components like ChatBot
        # ...

        # Run the ChatBot component
        # chat_bot = ChatBot(chat_engine_instance)
        # chat_bot.run()

        # Display other components like plots and data tables
