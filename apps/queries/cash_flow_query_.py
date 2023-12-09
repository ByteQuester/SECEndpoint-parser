def cash_flow_query(df):
    filtered_df = df[df['Metric'].isin(['NetCashProvidedByUsedInOperatingActivities',
                                        'NetCashProvidedByUsedInInvestingActivities',
                                        'NetCashProvidedByUsedInFinancingActivities'])]

    grouped_df = filtered_df.groupby(['EntityName', 'CIK', 'End'])

    result_df = grouped_df.agg({
        'Value': {
            'CashFlow_Operating': lambda x: round(x[df['Metric'] == 'NetCashProvidedByUsedInOperatingActivities'].sum() / 1000000, 2),
            'CashFlow_Investing': lambda x: round(x[df['Metric'] == 'NetCashProvidedByUsedInInvestingActivities'].sum() / 1000000, 2),
            'CashFlow_Financing': lambda x: round(x[df['Metric'] == 'NetCashProvidedByUsedInFinancingActivities'].sum() / 1000000, 2),
        }
    })

    result_df['Quarter'] = result_df.index.get_level_values('End').map(lambda date: f"Q{((date.month-1)//3)+1}-{date.year}")

    return result_df.reset_index()
