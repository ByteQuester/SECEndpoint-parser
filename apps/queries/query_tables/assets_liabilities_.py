import pandas as pd


def assets_liability_query(df):
    # Pivot the DataFrame so that each metric becomes a column
    pivot_df = df.pivot_table(index=['EntityName', 'CIK', 'end', 'year', 'quarter'],
                              columns='Metric',
                              values='val')

    # Reset index to make 'EntityName', 'CIK', 'end', 'year', 'quarter' columns again
    pivot_df.reset_index(inplace=True)

    # Rename columns to remove MultiIndex
    pivot_df.columns.name = None

    # 1. Convert 'end' column to datetime
    pivot_df['end'] = pd.to_datetime(pivot_df['end'], format='%Y-%m-%d')

    # 2. Convert financial values from cents to millions for readability
    pivot_df['Assets'] /= 1000000
    pivot_df['StockholdersEquity'] /= 1000000
    pivot_df['Liabilities'] /= 1000000

    # 3. Calculate Asset to Liability Ratio and Debt to Equity Ratio where data is available
    pivot_df['AssetToLiabilityRatio'] = pivot_df.apply(lambda row: row['Assets'] / row['Liabilities'] if pd.notna(row['Liabilities']) else None, axis=1)
    pivot_df['DebtToEquityRatio'] = pivot_df.apply(lambda row: row['Liabilities'] / row['StockholdersEquity'] if pd.notna(row['Liabilities']) and pd.notna(row['StockholdersEquity']) else None, axis=1)

    # 4. Selecting and renaming columns to match the desired format
    df_final = pivot_df[['EntityName', 'CIK', 'end', 'Assets', 'Liabilities', 'StockholdersEquity', 'AssetToLiabilityRatio', 'DebtToEquityRatio', 'year', 'quarter']]
    df_final.rename(columns={'EntityName': 'ENTITY', 'end': 'DATE', 'year': 'Year', 'quarter': 'Quarter'}, inplace=True)

    return df_final
