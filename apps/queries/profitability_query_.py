def profitability_query(df):
    filtered_df = df[df['Metric'].isin(['NetIncomeLoss', 'Revenues', 'OperatingIncomeLoss'])]

    grouped_df = filtered_df.groupby(['EntityName', 'CIK', 'End'])

    result_df = grouped_df.agg({
        'Value': {
            'NetIncomeLoss': lambda x: round(x[df['Metric'] == 'NetIncomeLoss'].sum() / 1000000, 2),
            'Revenues': lambda x: round(x[df['Metric'] == 'Revenues'].sum() / 1000000, 2),
            'OperatingIncomeLoss': lambda x: round(x[df['Metric'] == 'OperatingIncomeLoss'].sum() / 1000000, 2)
        }
    })

    result_df['ProfitMarginPercent'] = result_df.apply(
        lambda row: round((row['Value']['NetIncomeLoss'] / row['Value']['Revenues']) * 100, 2)
        if row['Value']['Revenues'] != 0 else None, axis=1
    )

    result_df['Quarter'] = result_df.index.get_level_values('End').map(
        lambda date: f"Q{((date.month-1)//3)+1}-{date.year}"
    )

    return result_df.reset_index()
