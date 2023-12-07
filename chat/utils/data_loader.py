'''
Keep the current structure.
'''
from llama_index.llms import OpenAI
from llama_index import SimpleDirectoryReader, ServiceContext, VectorStoreIndex
import streamlit as st


@st.cache_resource(show_spinner=False)
def load_data():
    '''
    Load and index the documents.
    '''
    with st.spinner(text="Loading and indexing the docs – hang tight! This should take 1-2 minutes."):
        reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
        docs = reader.load_data()
        service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-3.5-turbo", temperature=0.5, system_prompt="You are an expert on the financial market and your job is to answer detailed questions about finance. Assume that all questions are related to the finance. Keep your answers concice and based on facts you have been provided with which is a query of data – do not hallucinate features."))
        index = VectorStoreIndex.from_documents(docs, service_context=service_context)
        query_engine = index.as_query_engine()
        return query_engine
