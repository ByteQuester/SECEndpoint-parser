import pandas as pd

def liquidity_query(df):
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
    pivot_df['CurrentAssets'] = pivot_df['AssetsCurrent'] / 1000000
    pivot_df['CurrentLiabilities'] = pivot_df['LiabilitiesCurrent'] / 1000000

    # 3. Calculate the Current Ratio
    pivot_df['CurrentRatio'] = pivot_df.apply(
        lambda row: row['CurrentAssets'] / row['CurrentLiabilities']
        if row['CurrentLiabilities'] > 0 else None, axis=1)

    # 4. Selecting and renaming columns to match the desired format
    df_final = pivot_df[['EntityName', 'CIK', 'end', 'CurrentAssets', 'CurrentLiabilities', 'CurrentRatio', 'year', 'quarter']]
    df_final.rename(columns={'EntityName': 'ENTITY', 'end': 'DATE', 'year': 'Year', 'quarter': 'Quarter'}, inplace=True)

    return df_final
