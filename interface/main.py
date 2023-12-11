import streamlit as st
from functions.data.data_loader import DataLoader
from functions.ui.ui_components import UIComponents
from functions.visualization.data_visualizer import FinancialVisualizer


def main():
    st.title('Financial Data Dashboard')

    # Initialize classes
    data_loader = DataLoader()
    ui = UIComponents()
    visualizer = FinancialVisualizer()

    # Hardcoded values for testing
    cik_number = '12927'
    query_type = 'liquidity'

    st.write(f"CIK Number: {cik_number}")
    st.write(f"Query Type: {query_type}")

    # TODO: Date range selection based on available data
    # date_options = data_loader.get_available_dates(cik_number, query_type)
    # selected_date = ui.select_date(date_options)

    # For now, proceed without date selection
    if ui.submit_button():
        file_path = data_loader.construct_file_path(cik_number, query_type)
        data = data_loader.load_data(file_path)

        if data is not None:
            if query_type == 'profitability':
                visualizer.plot_profitability(data)
            elif query_type == 'liquidity':
                visualizer.plot_liquidity(data)
            elif query_type == 'cash_flow':
                visualizer.plot_cash_flow(data)
            else:
                st.write("Query type not supported.")
        else:
            st.write("No data available for the selected CIK and query type.")


if __name__ == '__main__':
    main()
