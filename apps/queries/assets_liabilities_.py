def assets_liability_query(df):
    filtered_df = df[df['Metric'].isin(['Assets', 'Liabilities', 'StockholdersEquity'])]
    grouped_df = filtered_df.groupby(['EntityName', 'CIK', 'End'])

    result_df = grouped_df.agg({
        'Value': {
            'Assets_M': lambda x: round(x[df['Metric'] == 'Assets'].sum() / 1000000, 2),
            'TotalLiabilities_Millions': lambda x: round(x[df['Metric'] == 'Liabilities'].sum() / 1000000, 2),
            'Equity_Millions': lambda x: round(x[df['Metric'] == 'StockholdersEquity'].sum() / 1000000, 2)
        }
    })

    result_df['AssetToLiabilityRatio'] = result_df.apply(
        lambda row: round(row['Assets_M'] / row['TotalLiabilities_Millions'], 2)
                    if row['TotalLiabilities_Millions'] > 0 else None,
        axis=1
    )
    result_df['DebtToEquityRatio'] = result_df.apply(
        lambda row: round(row['TotalLiabilities_Millions'] / row['Equity_Millions'], 2)
                    if row['Equity_Millions'] > 0 else None,
        axis=1
    )

    result_df['Quarter'] = result_df.index.get_level_values('End').map(lambda date: f"Q{((date.month-1)//3)+1}-{date.year}")

    return result_df.reset_index()
