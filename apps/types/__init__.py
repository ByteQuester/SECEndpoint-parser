# In apps/types/__init__.py

from .types import SECEndpoints
from .file_paths import FilePaths

BASE_URL = SECEndpoints.BASE_URL.value
COMPANY_TICKERS = SECEndpoints.COMPANY_TICKERS.value
SUBMISSIONS = SECEndpoints.SUBMISSIONS.value
COMPANY_FACTS = SECEndpoints.COMPANY_FACTS.value

DEFAULT_STAGE_NAME = FilePaths().DEFAULT_STAGE_NAME
DEFAULT_TABLE_NAME = FilePaths().DEFAULT_TABLE_NAME
CSV_DIRECTORY = FilePaths().CSV_DIRECTORY
CSV_FILE_PATH = FilePaths().CSV_FILE_PATH

__all__ = [
    'SECEndpoints',
    'BASE_URL',
    'COMPANY_TICKERS',
    'SUBMISSIONS',
    'COMPANY_FACTS',
    'FilePaths',
    'DEFAULT_STAGE_NAME',
    'DEFAULT_TABLE_NAME',
    'CSV_DIRECTORY',
    'CSV_FILE_PATH'
]


# example :# In another part of your application
# from apps.types import DEFAULT_STAGE_NAME, DEFAULT_TABLE_NAME, CSV_DIRECTORY, CSV_FILE_PATH
#
# # Use DEFAULT_STAGE_NAME, DEFAULT_TABLE_NAME, CSV_DIRECTORY, CSV_FILE_PATH as needed