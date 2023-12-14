import pandas as pd

def assets_liability_query(df):
    # Filter for Assets, Liabilities, and StockholdersEquity
    filtered_df = df[df['Metric'].isin(['Assets', 'Liabilities', 'StockholdersEquity'])]

    # Group by EntityName, CIK, and End
    grouped_df = filtered_df.groupby(['EntityName', 'CIK', 'End'])

    # Perform aggregation within each group
    def aggregate_group(group):
        result = {
            'Assets_Millions': round(group[group['Metric'] == 'Assets']['Value'].sum() / 1000000, 2),
            'Liabilities_Millions': round(group[group['Metric'] == 'Liabilities']['Value'].sum() / 1000000, 2),
            'Equity_Millions': round(group[group['Metric'] == 'StockholdersEquity']['Value'].sum() / 1000000, 2)
        }
        return pd.Series(result, index=['Assets_Millions', 'Liabilities_Millions', 'Equity_Millions'])

    result_df = grouped_df.apply(aggregate_group)

    # Reset index to move 'EntityName', 'CIK', and 'End' back to columns
    result_df = result_df.reset_index()

    # Convert 'End' to datetime
    result_df['End'] = pd.to_datetime(result_df['End'])

    # Calculate ratios where data is available
    result_df['AssetToLiabilityRatio'] = result_df.apply(
        lambda row: round(row['Assets_Millions'] / row['Liabilities_Millions'], 2) if row['Liabilities_Millions'] > 0 else None, axis=1
    )
    result_df['DebtToEquityRatio'] = result_df.apply(
        lambda row: round(row['Liabilities_Millions'] / row['Equity_Millions'], 2) if row['Equity_Millions'] > 0 else None, axis=1
    )

    # Construct the 'Quarter' column
    result_df['Quarter'] = result_df['End'].apply(lambda date: f"Q{((date.month-1)//3)+1}-{date.year}")

    return result_df

# Example usage
# df = load_your_dataframe_here()
# result = assets_liability_query(df)
