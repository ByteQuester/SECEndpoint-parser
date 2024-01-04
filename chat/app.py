import streamlit as st
from streamlit_elements import mui, nivo, elements

from .chat_bot import ChatBot
from .configs import PAGE_TITLE, PAGE_ICON, INITIAL_SIDEBAR_STATE, MENU_ITEMS, LAYOUT
from .data import DataLoader
from .interface import AppInterface, GraphManager


class ApplicationManager:
    def __init__(self, cik_number, query_type, base_dir):
        self.cik_number = cik_number
        self.query_type = query_type
        self.base_dir = base_dir
        self.app_interface = AppInterface(PAGE_TITLE, PAGE_ICON, LAYOUT, INITIAL_SIDEBAR_STATE, MENU_ITEMS)
        self.data_loader = DataLoader(base_dir=base_dir)
        self.graph_manager = GraphManager()

    def push_file(self, cik_number, query_type):
        '''
        :return: json dataframe
        '''
        file_path = self.data_loader.construct_file_path(cik_number, query_type)
        return self.data_loader.load_json_data(file_path)

    def push_directory(self, cik_number, query_type):
        '''
        return: path  to the dir e.g, ./data/0000012927/processed_json/Profitability
        '''
        return self.data_loader.construct_directory_path(cik_number, query_type)

    def push_query_engine(self, cik_number, query_type):
        folder_path = self.push_directory(cik_number, query_type)
        return self.data_loader.load_indexed_data(folder_path) if folder_path else None

    def run(self, category='Profitability'):
        available_charts = self.graph_manager.get_available_charts(category)

        for chart_type, plot_function in available_charts.items():
            data_for_chart = self.data_loader.load_json_data_for_chart(self.cik_number, category, chart_type)
            if data_for_chart:
                plot_function(data_for_chart)
        # Tabs for Data View and Plot View
        # tab1, tab2 = st.tabs(["Data View", "Plot View"])

        # Data View Tab
        # with tab1:
            # self.app_interface.display_data_table(df)

        # Tabs for Data View and Plot View
        # tab1, tab2 = st.tabs(["Data View", "Plot View"])

        # with tab2:
            # if plot_function:
                # with elements("my_dashboard"):
                    # plot_function(df)
            # else:
                # st.write("Plotting not available for this query type.")
        # Expandable ChatBot Section
        # with st.expander("ChatBot", expanded=False):
        # chat_engine_instance = self.push_query_engine(self.cik_number, self.query_type)
        # chat_bot = ChatBot(chat_engine_instance)
        # chat_bot.run()


def run_application(cik_number="0000012927", query_type="Profitability", base_dir="data"):
    app_manager = ApplicationManager(cik_number, query_type, base_dir)
    app_manager.run()


if __name__ == "__main__":
    run_application()