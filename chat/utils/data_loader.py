'''
Keep the current structure.
'''
from llama_index.llms import OpenAI
from llama_index import SimpleDirectoryReader, ServiceContext, VectorStoreIndex
import streamlit as st
import os
import pandas as pd
import markdown
from bs4 import BeautifulSoup

from chat.configs import MODEL, TEMPERATURE, SYSTEM_PROMPT


class DataLoader:
    def __init__(self, base_dir='data'):
        self.base_dir = base_dir

    def construct_file_path(self, cik, query_type):
        '''
        Construct path to csv file in directory path of a specific query and cik number.
        '''
        folder_path = os.path.join(self.base_dir, str(cik), 'processed_data', query_type)
        files = os.listdir(folder_path)
        if files:
            latest_file = max(files, key=lambda x: os.path.getctime(os.path.join(folder_path, x)))
            return os.path.join(folder_path, latest_file)
        return None

    def construct_directory_path(self,cik, query_type):
        folder_path = os.path.join(self.base_dir, str(cik), 'processed_data', query_type)
        if os.path.isdir(folder_path):
            return folder_path
        else:
            print(f"Directory not found: {folder_path}")
            return None

    def load_csv_data(self, file_path):
        '''
        Load csv data in directory path.
        '''
        if file_path and os.path.exists(file_path):
            try:
                df = pd.read_csv(file_path)
                return df
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")
        else:
            print(f"File path is invalid: {file_path}")
        return None

    @staticmethod
    def load_indexed_data(directory_path):
        '''
        Load and index the documents using configurations from LlamaConfig.
        '''
        with st.spinner("Loading and indexing the docs – hang tight!"):
            reader = SimpleDirectoryReader(input_dir=directory_path, recursive=True)
            docs = reader.load_data()
            service_context = ServiceContext.from_defaults(
                llm=OpenAI(model=MODEL, temperature=TEMPERATURE, system_prompt=SYSTEM_PROMPT)
            )
            index = VectorStoreIndex.from_documents(docs, service_context=service_context)
            query_engine = index.as_query_engine()
            return query_engine

    def get_available_cik_numbers(self):
        """
        Returns a list of available CIK numbers based on the directory structure.
        """
        cik_numbers = [dir_name for dir_name in os.listdir(self.base_dir)
                       if os.path.isdir(os.path.join(self.base_dir, dir_name))]
        return cik_numbers

    def get_available_query_types(self, cik):
        """
        Returns a list of available query types for a given CIK number.
        """
        index_file_path = os.path.join(self.base_dir, cik, 'processed_data', 'index.md')
        if os.path.exists(index_file_path):
            with open(index_file_path, 'r') as file:
                md_content = file.read()
                md = markdown.Markdown()
                html_content = md.convert(md_content)
                return self.extract_query_types_from_markdown(html_content)
        return []

    @staticmethod
    def extract_query_types_from_markdown(html_content):
        """
        Extracts query types from the HTML content of the markdown file using BeautifulSoup.
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        query_types = [h3.get_text() for h3 in soup.find_all('h3')]
        return query_types


