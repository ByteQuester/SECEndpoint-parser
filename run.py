import logging
import streamlit as st

from apps import DataPipelineIntegration
from chat.utils import DataLoader
from chat.interface import AppInterface
from chat.configs import PAGE_TITLE, PAGE_ICON, LAYOUT, INITIAL_SIDEBAR_STATE, MENU_ITEMS
from chat.interface.ui_components import UIComponents


# Initialize Logging
# ----------------------------------------
def init_logging():
    logging.basicConfig(filename='app.log', level=logging.INFO,
                        format='[%(asctime)s %(levelname)s] %(message)s',
                        datefmt='%Y-%d-%m %H:%M:%S', encoding="utf-8")


init_logging()

# Configure Streamlit Page
# ----------------------------------------
st.set_page_config(page_title="Your App ", page_icon="🌟", layout="centered", initial_sidebar_state="auto")

# User Interface Management
# ----------------------------------------
ui_components = UIComponents()
data_loader = DataLoader()

# Fetch dynamically available CIK numbers and query types
available_ciks = data_loader.get_available_cik_numbers()
available_query_types = data_loader.get_available_query_types()

# User Selection for CIK and Query Type
# ----------------------------------------
selected_cik = ui_components.select_cik_number(available_ciks)
selected_query_type = ui_components.select_query_type(available_query_types)

# Data Processing
# ----------------------------------------
if selected_cik and selected_query_type:
    data_pipeline = DataPipelineIntegration(cik_number=selected_cik, use_snowflake=False)
    raw_data = data_pipeline.fetch_data()
    preprocessed_data = data_pipeline.preprocess_data(raw_data)
    processed_data = data_pipeline.process_and_store_data()

    # Visualization and Post-processing
    # ...
    display_data(processed_data)  # Implement this function to show data

    # Chatbot Integration (if API key is provided)
    # ...
    if "OPENAI_API_KEY" in st.secrets:
        run_chatbot(processed_data)  # Implement this function to run the chatbot

else:
    st.warning("Please select both CIK number and query type.")

if __name__ == "__main__":
    run_application()
