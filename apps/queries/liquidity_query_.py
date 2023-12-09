def liquidity_query(df):
    filtered_df = df[df['Metric'].isin(['AssetsCurrent', 'LiabilitiesCurrent'])]

    grouped_df = filtered_df.groupby(['EntityName', 'CIK', 'End'])

    result_df = grouped_df.agg({
        'Value': {
            'CurrentAssets': lambda x: round(x[df['Metric'] == 'AssetsCurrent'].sum() / 1000000, 2),
            'CurrentLiabilities': lambda x: round(x[df['Metric'] == 'LiabilitiesCurrent'].sum() / 1000000, 2),
        }
    })

    result_df['CurrentRatio'] = result_df.apply(
        lambda row: round(row['Value']['CurrentAssets'] / row['Value']['CurrentLiabilities'], 2)
        if row['Value']['CurrentLiabilities'] > 0 else None, axis=1
    )

    result_df['Quarter'] = result_df.index.get_level_values('End').map(
        lambda date: f"Q{((date.month-1)//3)+1}-{date.year}"
    )

    return result_df.reset_index()
