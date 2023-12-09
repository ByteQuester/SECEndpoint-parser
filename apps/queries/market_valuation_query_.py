def market_valuation_query(df, stock_price_df=None):
    filtered_df = df[df['Metric'].isin(['MarketCapitalization', 'EarningsPerShareBasic', 'EarningsPerShareDiluted'])]

    if stock_price_df is not None:
        merged_df = pd.merge(filtered_df, stock_price_df, left_on=['CIK', 'End'], right_on=['CIK', 'Date'], how='left')
    else:
        merged_df = filtered_df
        merged_df['StockPrice'] = None  # Placeholder if stock price data is not available

    grouped_df = merged_df.groupby(['EntityName', 'CIK', 'End'])

    result_df = grouped_df.agg({
        'Value': {
            'MarketCap': lambda x: round(x[df['Metric'] == 'MarketCapitalization'].sum() / 1000000, 2),
            'EPS_Basic': lambda x: x[df['Metric'] == 'EarningsPerShareBasic'].mean(),
            'EPS_Diluted': lambda x: x[df['Metric'] == 'EarningsPerShareDiluted'].mean(),
        },
        'StockPrice': 'mean'
    })

    result_df['PE_Ratio'] = result_df.apply(
        lambda row: round(row['StockPrice'] / row['Value']['EPS_Diluted'], 2)
        if row['Value']['EPS_Diluted'] > 0 else None, axis=1
    )

    result_df['Quarter'] = result_df.index.get_level_values('End').map(
        lambda date: f"Q{((date.month-1)//3)+1}-{date.year}"
    )

    return result_df.reset_index()
