# In apps/functions/storages/__init__.py

from .sw_flake import SnowflakeDataManager
from .local_data_storage import DataStorageManager

__all__ = ['SnowflakeDataManager',
           'DataStorageManager']
