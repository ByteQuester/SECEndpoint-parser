'''
Keep the current structure.
'''
from llama_index.llms import OpenAI
from llama_index import SimpleDirectoryReader, ServiceContext, VectorStoreIndex
import streamlit as st
import os
import pandas as pd

from chat.configs import MODEL, TEMPERATURE, SYSTEM_PROMPT


class DataLoader:
    def __init__(self, base_dir='data'):
        self.base_dir = base_dir

    def construct_file_path(self, cik, query_type):
        folder_path = os.path.join(self.base_dir, str(cik), 'processed_data', query_type)
        files = os.listdir(folder_path)
        if files:
            latest_file = max(files, key=lambda x: os.path.getctime(os.path.join(folder_path, x)))
            return os.path.join(folder_path, latest_file)
        return None

    def construct_directory_path(self,cik, query_type):
        # Path to the folder
        folder_path = os.path.join(self.base_dir, str(cik), 'processed_data', query_type)
        if os.path.isdir(folder_path):
            return folder_path
        else:
            print(f"Directory not found: {folder_path}")
            return None

    def load_csv_data(self, file_path):
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
