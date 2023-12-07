'''
Transition to a class structure to encapsulate chat functionalities.
'''
import streamlit as st
class ChatInterface:
    def __init__(self):
        if "messages" not in st.session_state.keys():
            st.session_state.messages = [
                {"role": "assistant", "content": "Ask me a question!"}
            ]
    def display_chat_messages(self):
        '''
        Display chat messages.
        '''
        if not st.session_state.messages:
            st.write("No messages to display")
        else:
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.write(message["content"])