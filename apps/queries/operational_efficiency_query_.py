def operational_efficiency_query(df):
    filtered_df = df[df['Metric'].isin(['CostOfGoodsSold', 'OperatingExpenses', 'Revenues'])]

    grouped_df = filtered_df.groupby(['EntityName', 'CIK', 'End'])

    result_df = grouped_df.agg({
        'Value': {
            'COGS': lambda x: round(x[df['Metric'] == 'CostOfGoodsSold'].sum() / 1000000, 2),
            'OperatingExpenses': lambda x: round(x[df['Metric'] == 'OperatingExpenses'].sum() / 1000000, 2),
            'Revenues': lambda x: round(x[df['Metric'] == 'Revenues'].sum() / 1000000, 2)
        }
    })

    result_df['OperationalEfficiencyRatio'] = result_df.apply(
        lambda row: round((row['Value']['OperatingExpenses'] + row['Value']['COGS']) / row['Value']['Revenues'], 2)
        if row['Value']['Revenues'] > 0 else None, axis=1
    )

    result_df['Quarter'] = result_df.index.get_level_values('End').map(
        lambda date: f"Q{((date.month-1)//3)+1}-{date.year}"
    )

    return result_df.reset_index()

