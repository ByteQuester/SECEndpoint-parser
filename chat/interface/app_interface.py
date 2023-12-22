'''
Transition to a class structure to encapsulate chat functionalities.
'''
import streamlit as st

from .ui import FinancialVisualizer, show_data_view


class AppInterface:
    def __init__(self, page_title, page_icon, layout, initial_sidebar_state, menu_items):
        self.page_title = page_title
        self.page_icon = page_icon
        self.layout = layout
        self.initial_sidebar_state = initial_sidebar_state
        self.menu_items = menu_items
        self.visualizer = FinancialVisualizer()

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

    def display_plot(self, df, plot_type):
        plot_function = self.visualizer.get_plot_function(plot_type)
        if plot_function:
            plot_function(df)
        else:
            st.write(f"No plot available for query type: {plot_type}")
        pass

    def display_data_table(self, df):
        show_data_view(df)

