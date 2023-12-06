import logging
import argparse

from env.data_wrangler import FinancialDataProcessor
from env.sec_api_client import SECAPIClient

# Argument Parsing
parser = argparse.ArgumentParser(description="SEC Filing Analyzer")
parser.add_argument('--ciks', nargs='+', type=str, help="List of CIK numbers to analyze", required=True)
# TO DO: add date argument
args = parser.parse_args()

# Start
# ----------------------------------------
#          Init Log
# ----------------------------------------
logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='[%(asctime)s %(levelname)s] %(message)s',
                    datefmt='%Y-%d-%m %H:%M:%S', encoding="utf-8")
# ----------------------------------------
#          Pre Processing
# ----------------------------------------
