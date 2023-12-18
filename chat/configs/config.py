'''
Load configuration classes based on service name.
'''
from config_classes import BaseConfig, StreamlitConfig, OpenAIConfig, LlamaConfig
import os


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
            API_KEY=os.getenv("OPENAI_API_KEY")
        ),
        "Llama": LlamaConfig(
            MODEL="gpt-3.5-turbo",
            TEMPERATURE=0.5,
            SYSTEM_PROMPT="You're a finance expert given a set of queries. Analyse the data and answer to the user's questions without hallucinating"
        )
    }

    if service_name in config_mapping:
        return config_mapping[service_name]
    else:
        raise ValueError(f"Invalid service name: {service_name}")
