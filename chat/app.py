import streamlit as st
#from interface.ui_components import UIComponents
from interface.app_interface import AppInterface
from interface.ui_components.visualization import FinancialVisualizer
from chat_bot import ChatBot
from utils.data_loader import DataLoader
from configs import PAGE_TITLE, PAGE_ICON, INITIAL_SIDEBAR_STATE, MENU_ITEMS, LAYOUT


class ApplicationManager:
    def __init__(self, cik_number, query_type, base_dir):
        self.cik_number = cik_number
        self.query_type = query_type
        self.base_dir = base_dir
        #self.ui = UIComponents()
        self.app_interface = AppInterface(PAGE_TITLE, PAGE_ICON, LAYOUT, INITIAL_SIDEBAR_STATE, MENU_ITEMS)
        self.visualizer = FinancialVisualizer()
        self.data_loader = DataLoader(base_dir=base_dir)

    def push_file(self, cik_number, query_type):
        file_path = self.data_loader.construct_file_path(cik_number, query_type)
        return self.data_loader.load_csv_data(file_path)

    def push_directory(self, cik_number, query_type):
        return self.data_loader.construct_directory_path(cik_number, query_type)

    def push_query_engine(self, cik_number, query_type):
        folder_path = self.push_directory(cik_number, query_type)
        return self.data_loader.load_indexed_data(folder_path) if folder_path else None

    def run(self):
        # Assuming cik_number and query_type are set
        csv_file_path = self.push_file(self.cik_number, self.query_type)
        directory_path = self.push_directory(self.cik_number, self.query_type)

        tab1, tab2, tab3 = st.tabs(["Data View", "Plot View", "Chat View"])
        with tab1:
            data = self.data_loader.load_csv_data(csv_file_path)
            self.app_interface.display_data_table(data)  # Implement this method to show data in a table format

        # Plot View Tab
        with tab2:
            data_for_plot = self.data_loader.load_csv_data(csv_file_path)
            self.visualizer.plot_profitability(data_for_plot)  # Example plot #TODO: mapping between query type & plot

        # ChatBot Tab
        with tab3:
            ChatBot(directory_path)  # Run the ChatBot


# Keep the entry point clean and straightforward
def run_application():
    st.set_page_config(PAGE_TITLE, PAGE_ICON, LAYOUT, INITIAL_SIDEBAR_STATE, MENU_ITEMS)
    app_manager = ApplicationManager("CIK_number", "query_type", "base_dir")  # Example placeholders
    app_manager.run()


if __name__ == "__main__":
    run_application()