def debt_management_query(df):
    filtered_df = df[df['Metric'].isin(['ShortTermDebt', 'LongTermDebt'])]

    grouped_df = filtered_df.groupby(['EntityName', 'CIK', 'End'])

    result_df = grouped_df.agg({
        'Value': {
            'ShortTermDebt': lambda x: round(x[df['Metric'] == 'ShortTermDebt'].sum() / 1000000, 2),
            'LongTermDebt': lambda x: round(x[df['Metric'] == 'LongTermDebt'].sum() / 1000000, 2),
        }
    })

    result_df['DebtStructureRatio'] = result_df.apply(
        lambda row: round(row['Value']['ShortTermDebt'] / row['Value']['LongTermDebt'], 2)
        if row['Value']['LongTermDebt'] > 0 else None, axis=1
    )

    result_df['Quarter'] = result_df.index.get_level_values('End').map(
        lambda date: f"Q{((date.month-1)//3)+1}-{date.year}"
    )

    return result_df.reset_index()
