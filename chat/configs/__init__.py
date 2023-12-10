# In chat/configs/__init__.py
from .config_classes import StreamlitConfig, OpenAIConfig, LlamaConfig
import streamlit as st

streamlit_config = StreamlitConfig(
    PAGE_TITLE="Chat with the assistant",
    PAGE_ICON="🦙",
    LAYOUT="centered",
    INITIAL_SIDEBAR_STATE="auto",
    MENU_ITEMS=[]
)

PAGE_TITLE = streamlit_config.PAGE_TITLE
PAGE_ICON = streamlit_config.PAGE_ICON
LAYOUT = streamlit_config.LAYOUT
INITIAL_SIDEBAR_STATE = streamlit_config.INITIAL_SIDEBAR_STATE
MENU_ITEMS = streamlit_config.MENU_ITEMS

openai_config = OpenAIConfig(
    API_KEY=st.secrets["openai_key"]
)

OPENAI_API_KEY = openai_config.API_KEY

llama_config = LlamaConfig(
    INDEX_NAME='your_index_name',
    DIRECTORY_PATH='./data/llama_data',
    MODEL="gpt-3.5-turbo",
    TEMPERATURE=0.5,
    SYSTEM_PROMPT="Your custom prompt here"
)

INDEX_NAME = llama_config.INDEX_NAME
DIRECTORY_PATH = llama_config.DIRECTORY_PATH
MODEL = llama_config.MODEL
TEMPERATURE = llama_config.TEMPERATURE
SYSTEM_PROMPT = llama_config.SYSTEM_PROMPT

__all__ = [
    'PAGE_TITLE', 'PAGE_ICON', 'LAYOUT', 'INITIAL_SIDEBAR_STATE', 'MENU_ITEMS',
    'OPENAI_API_KEY',
    'INDEX_NAME', 'DIRECTORY_PATH', 'MODEL', 'TEMPERATURE', 'SYSTEM_PROMPT'
]
