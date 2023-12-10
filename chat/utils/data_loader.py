'''
Keep the current structure.
'''
from llama_index.llms import OpenAI
from llama_index import SimpleDirectoryReader, ServiceContext, VectorStoreIndex
import streamlit as st

from chat.configs import DIRECTORY_PATH, MODEL, TEMPERATURE, SYSTEM_PROMPT


def load_data():
    '''
    Load and index the documents using configurations from LlamaConfig.
    '''
    with st.spinner("Loading and indexing the docs – hang tight!"):
        reader = SimpleDirectoryReader(input_dir=DIRECTORY_PATH, recursive=True)
        docs = reader.load_data()
        service_context = ServiceContext.from_defaults(
            llm=OpenAI(model=MODEL,
                       temperature=TEMPERATURE,
                       system_prompt=SYSTEM_PROMPT)
        )
        index = VectorStoreIndex.from_documents(docs, service_context=service_context)
        query_engine = index.as_query_engine()
        return query_engine
