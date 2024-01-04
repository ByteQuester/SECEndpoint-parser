import pandas as pd 


def prepare_and_sort_financial_data(df, metric):
    """
    Prepares and sorts financial data for a specific metric, focusing exclusively on quarterly data.

    Args:
    df (DataFrame): The raw DataFrame containing financial data.
    metric (str): The specific financial metric to prepare and sort (e.g., 'OperatingIncomeLoss').

    Returns:
    DataFrame: A DataFrame filtered, cleaned, and sorted for the specific metric, with only quarterly data.
    """
    # Filter by Metric
    df_metric = df[df['Metric'] == metric]

    # Drop unnecessary columns
    columns_to_drop = ['accn', 'form', 'filed']
    df_cleaned = df_metric.drop(columns=columns_to_drop)

    # Function to extract year and quarter, excluding non-quarterly data
    def extract_year_quarter(row):
        if pd.notna(row['frame']) and 'Q' in row['frame']:
            year = row['frame'][2:6]  # Extract year part
            quarter = row['frame'][6:8]  # Extract quarter part
            return [year, quarter]
        return [None, None]  # Exclude non-quarterly entries

    # Apply the function to each row
    df_cleaned[['year', 'quarter']] = df_cleaned.apply(extract_year_quarter, axis=1, result_type="expand")

    # Remove rows with None values in 'year' or 'quarter'
    df_cleaned.dropna(subset=['year', 'quarter'], inplace=True)

    # Sort the DataFrame by year and quarter
    sorted_df = df_cleaned.sort_values(by=['year', 'quarter'])

    # Drop columns
    sorted_df = sorted_df.drop(columns=['frame', 'fp', 'fy'])

    return sorted_df
