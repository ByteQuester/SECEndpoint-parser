'''
Load configuration classes based on service name.
'''
from config_classes import BaseConfig, StreamlitConfig, OpenAIConfig, LlamaConfig
import streamlit as st


def load_config(service_name: str) -> BaseConfig:
    '''
    Load the configuration for the specified service.
    '''
    config_mapping = {
        "Streamlit": StreamlitConfig(
            PAGE_TITLE="Chat with the assistant",
            PAGE_ICON="🦙",
            LAYOUT="centered",
            INITIAL_SIDEBAR_STATE="auto",
            MENU_ITEMS=[]
        ),
        "OpenAI": OpenAIConfig(
            API_KEY=st.secrets["openai_key"]
        ),
        "Llama": LlamaConfig(
            INDEX_NAME='your_index_name',
            DIRECTORY_PATH='./data/llama_data',
            MODEL="gpt-3.5-turbo",
            TEMPERATURE=0.5,
            SYSTEM_PROMPT="Your custom prompt here"
        )
    }

    if service_name in config_mapping:
        return config_mapping[service_name]
    else:
        raise ValueError(f"Invalid service name: {service_name}")
