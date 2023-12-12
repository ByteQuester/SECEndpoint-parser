from dataclasses import dataclass, field


@dataclass
class BaseConfig:
    pass


@dataclass
class StreamlitConfig(BaseConfig):
    PAGE_TITLE: str
    PAGE_ICON: str
    LAYOUT: str
    INITIAL_SIDEBAR_STATE: str
    MENU_ITEMS: list = field(default_factory=list)


@dataclass
class OpenAIConfig(BaseConfig):
    def __init__(self, API_KEY: str):
        if not API_KEY:
            raise ValueError("OpenAI API key is not set. Please set the OPENAI_API_KEY environment variable.")
        self.API_KEY = API_KEY



@dataclass
class LlamaConfig(BaseConfig):
    DIRECTORY_PATH: str
    MODEL: str
    TEMPERATURE: float
    SYSTEM_PROMPT: str
