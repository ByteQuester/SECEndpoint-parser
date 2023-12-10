import pandas as pd

def operational_efficiency_query(df):
    filtered_df = df[df['Metric'].isin(['CostOfGoodsSold', 'OperatingExpenses', 'Revenues'])]

    # Pivot the data
    pivoted_df = filtered_df.pivot_table(
        index=['EntityName', 'CIK', 'End'],
        columns='Metric',
        values='Value',
        aggfunc='sum'
    )

    # Ensure all required columns are present
    required_metrics = ['CostOfGoodsSold', 'OperatingExpenses', 'Revenues']
    pivoted_df = pivoted_df.reindex(columns=required_metrics, fill_value=0)

    # Perform the calculations
    result_df = pd.DataFrame({
        'COGS': round(pivoted_df['CostOfGoodsSold'] / 1000000, 2),
        'OperatingExpenses': round(pivoted_df['OperatingExpenses'] / 1000000, 2),
        'Revenues': round(pivoted_df['Revenues'] / 1000000, 2)
    })

    # Calculate Operational Efficiency Ratio
    result_df['OperationalEfficiencyRatio'] = round(
        (result_df['OperatingExpenses'] + result_df['COGS']) / result_df['Revenues'], 2
    )
    result_df['OperationalEfficiencyRatio'] = result_df['OperationalEfficiencyRatio'].where(result_df['Revenues'] > 0)

    # Calculate Quarter
    result_df['Quarter'] = result_df.index.get_level_values('End').map(
        lambda date_str: f"Q{((pd.to_datetime(date_str).month - 1) // 3) + 1}-{pd.to_datetime(date_str).year}"
    )

    return result_df.reset_index()


