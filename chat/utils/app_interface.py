'''
Transition to a class structure to encapsulate chat functionalities.
'''
import streamlit as st


class AppInterface:
    def __init__(self, page_title, page_icon, layout, initial_sidebar_state, menu_items):
        self.page_title = page_title
        self.page_icon = page_icon
        self.layout = layout
        self.initial_sidebar_state = initial_sidebar_state
        self.menu_items = menu_items

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
    # Add methods for other UI components

    def display_plot(self, plot):
        # Method to display a plot
        pass

    def display_data_table(self, data):
        # Method to display a data table
        pass
