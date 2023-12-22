import streamlit as st

from .chat_bot import ChatBot
from .interface import AppInterface
from .utils import DataLoader
from .configs import PAGE_TITLE, PAGE_ICON, INITIAL_SIDEBAR_STATE, MENU_ITEMS, LAYOUT


class ApplicationManager:
    def __init__(self, cik_number, query_type, base_dir):
        self.cik_number = cik_number
        self.query_type = query_type
        self.base_dir = base_dir
        self.app_interface = AppInterface(PAGE_TITLE, PAGE_ICON, LAYOUT, INITIAL_SIDEBAR_STATE, MENU_ITEMS)
        self.data_loader = DataLoader(base_dir=base_dir)

    def push_file(self, cik_number, query_type):
        '''
        :param cik_number:
        :param query_type:
        :return: Dataframe
        '''
        file_path = self.data_loader.construct_file_path(cik_number, query_type)
        return self.data_loader.load_csv_data(file_path)

    def push_directory(self, cik_number, query_type):
        '''
        :param cik_number:
        :param query_type:
        :return: path  to the dir e.g, ./data/0000012927/processed_data/Profitability
        '''
        return self.data_loader.construct_directory_path(cik_number, query_type)

    def push_query_engine(self, cik_number, query_type):
        folder_path = self.push_directory(cik_number, query_type)
        return self.data_loader.load_indexed_data(folder_path) if folder_path else None

    def run(self):
        df = self.push_file(self.cik_number, self.query_type)

        # ChatBot Section
        st.header("ChatBot")
        chat_engine_instance = self.push_query_engine(self.cik_number, self.query_type)
        chat_bot = ChatBot(chat_engine_instance)
        chat_bot.run()

def run_application(cik_number="0000012927", query_type="Profitability", base_dir="data"):
    app_manager = ApplicationManager(cik_number, query_type, base_dir)
    app_manager.run()


if __name__ == "__main__":
    run_application()