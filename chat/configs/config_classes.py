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
    API_KEY: str


@dataclass
class LlamaConfig(BaseConfig):
    INDEX_NAME: str
    DIRECTORY_PATH: str
    MODEL: str
    TEMPERATURE: float
    SYSTEM_PROMPT: str
