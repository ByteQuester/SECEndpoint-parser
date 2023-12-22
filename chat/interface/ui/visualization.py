import streamlit as st
import pandas as pd
import altair as alt

class FinancialVisualizer:
    def __init__(self):
        # Initialization can be left empty if there's no specific setup needed
        pass

    def get_plot_function(self, plot_type):
        query_to_plot_map = {
            'Cash Flow': self.plot_cash_flow,
            'Liquidity': self.plot_liquidity,
            'Profitability': self.plot_profitability
            # placeholder for other mappings
        }
        return query_to_plot_map.get(plot_type)

    def plot_profitability(self, df):
        df['DATE'] = pd.to_datetime(df['DATE'])
        st.line_chart(df[['DATE', 'NetIncomeLoss', 'Revenues', 'OperatingIncomeLoss']].set_index('DATE'))

    def plot_liquidity(self, df):
        df['DATE'] = pd.to_datetime(df['DATE'])
        st.line_chart(df[['DATE', 'CURRENTASSETS', 'CURRENTLIABILITIES', 'CURRENTRATIO']].set_index('DATE'))

    def plot_cash_flow(self, df):
        df_melted = df.melt(id_vars=['DATE', 'QUARTER'],
                            value_vars=['CASHFLOW_OPERATING', 'CASHFLOW_INVESTING', 'CASHFLOW_FINANCING'])
        st.bar_chart(df_melted.set_index(['DATE', 'QUARTER']))


