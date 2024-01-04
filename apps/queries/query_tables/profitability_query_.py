import pandas as pd


def profitability_query(df):
    # Pivot the DataFrame so that each metric becomes a column
    pivot_df = df.pivot_table(index=['EntityName', 'CIK', 'end', 'year', 'quarter', 'start'],
                              columns='Metric',
                              values='val')

    # Reset index to make 'EntityName', 'CIK', 'end', 'year', 'quarter', 'start' columns again
    pivot_df.reset_index(inplace=True)

    # Rename columns to remove MultiIndex
    pivot_df.columns.name = None

    # Create a copy of the DataFrame to avoid SettingWithCopyWarning
    df_final = pivot_df.copy()

    # 1. Convert 'end' column to datetime in df_final
    df_final['end'] = pd.to_datetime(df_final['end'], format='%Y-%m-%d')

    # 2. Convert financial values from cents to millions for readability in df_final
    df_final['NetIncomeLoss'] /= 1000000
    df_final['Revenues'] /= 1000000
    df_final['OperatingIncomeLoss'] /= 1000000

    # 3. Calculate Profit Margin where data is available in df_final
    df_final['ProfitMarginPercent'] = df_final.apply(
        lambda row: (row['NetIncomeLoss'] / row['Revenues']) * 100
        if pd.notna(row['NetIncomeLoss']) and pd.notna(row['Revenues']) and row['Revenues'] != 0
        else None, axis=1)

    # 4. Select and rename columns in df_final
    df_final = df_final[
        ['EntityName', 'CIK', 'end', 'NetIncomeLoss', 'Revenues', 'OperatingIncomeLoss', 'ProfitMarginPercent', 'year', 'quarter']]
    df_final.rename(columns={'EntityName': 'ENTITY', 'end': 'DATE', 'year': 'Year', 'quarter': 'Quarter'}, inplace=True)

    return df_final
