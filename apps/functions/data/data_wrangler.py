'''
This module provides a FinancialDataProcessor class for processing financial data.
The FinancialDataProcessor class handles the flattening and structuring of financial data
retrieved from the SEC API and converts it into a pandas DataFrame for further analysis.
'''
from abc import ABC, abstractmethod
import pandas as pd


class FinancialDataProcessor(ABC):
    @abstractmethod
    def process_data(self, metric):
        pass


class AnnualDataProcessor(FinancialDataProcessor):
    def __init__(self, df):
        self.df = df

    def process_data(self, metrics):
        """
        Prepares and sorts financial data for a specific metric.
        Args:
            metrics (list[str]): The specific financial metrics to prepare and sort.
        Returns:
            DataFrame: A DataFrame filtered, cleaned, and sorted for the specific metric.
        """
        # Filter by Metric
        if isinstance(metrics, str):
            metrics = [metrics]
        df_metric = self.df[self.df['Metric'].isin(metrics)]
        # Filter for 10-K filings and ensure 'frame' column is not empty
        filtered_df = df_metric[df_metric['form'] == '10-K']
        filtered_df = filtered_df[filtered_df['frame'].notna()]
        # Drop unnecessary columns
        columns_to_drop = ['accn', 'fy', 'fp', 'form', 'filed']
        filtered_df_cleaned = filtered_df.drop(columns=columns_to_drop)
        # Define a custom sorting key and split into 'year' and 'quarter'

        def custom_sort_key(frame_value):
            year = frame_value[2:6]  # Extract the year part (e.g., '2007')
            quarter_order = {'Q1': 1, 'Q2': 2, 'Q3': 3, 'Q4': 4, 'FY': 5}  # Define order for quarters and FY
            quarter = frame_value[6:] if frame_value[6:] in quarter_order else 'FY'
            return year, quarter_order[quarter]
        filtered_df_cleaned[['year', 'quarter']] = filtered_df_cleaned['frame'].apply(custom_sort_key).apply(pd.Series)
        # Sort the DataFrame and drop the 'frame' and 'frame_sort_key' columns
        sorted_df = filtered_df_cleaned.sort_values(by=['year', 'quarter']).drop(columns=['frame'])
        return sorted_df


class QuarterlyDataProcessor(FinancialDataProcessor):
    def __init__(self, df):
        self.df = df

    def process_data(self, metrics):
        """
        Prepares and sorts financial data for a specific metric, focusing exclusively on quarterly data.
        Args:
            metrics (list[str]): The specific financial metrics to prepare and sort.
        Returns:
            DataFrame: A DataFrame filtered, cleaned, and sorted for the specific metric, with only quarterly data.
        """
        # Filter by Metric
        if isinstance(metrics, str):
            metrics = [metrics]
        df_metric = self.df[self.df['Metric'].isin(metrics)]
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
