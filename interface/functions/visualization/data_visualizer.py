import matplotlib.pyplot as plt
import seaborn as sns
import mpld3
import streamlit.components.v1 as components
import pandas as pd

class FinancialVisualizer:
    def __init__(self):
        sns.set(style="whitegrid")

    def plot_profitability(self, df):
        df['DATE'] = pd.to_datetime(df['DATE'])
        df.set_index('DATE', inplace=True)

        fig, ax = plt.subplots(figsize=(12, 6))
        df[['NETINCOMELOSS', 'REVENUES', 'OPERATINGINCOMELOSS']].plot(ax=ax)

        ax.set_title('Profitability Over Time')
        #ax.set_ylabel('Values')
        ax.legend(loc='upper left')
        ax.grid(False)  # Enable grid only if needed

        # Convert and display as interactive
        fig_html = mpld3.fig_to_html(fig)
        components.html(fig_html, height=600)

    def plot_liquidity(self, df):
        df['DATE'] = pd.to_datetime(df['DATE'])
        df.set_index('DATE', inplace=True)

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(df.index, df['CURRENTASSETS'], label='Current Assets')
        ax.plot(df.index, df['CURRENTLIABILITIES'], label='Current Liabilities')
        ax.plot(df.index, df['CURRENTRATIO'], label='Current Ratio')

        ax.set_title('Liquidity Over Time')
        #ax.set_ylabel('Values')
        ax.legend(loc='upper left')
        ax.grid(False)

        # Convert to interactive and display
        fig_html = mpld3.fig_to_html(fig)
        components.html(fig_html, height=600)

    def plot_cash_flow(self, df):
        fig, ax = plt.subplots(figsize=(12, 6))
        df_melted = df.melt(id_vars=['DATE', 'QUARTER'], value_vars=['CASHFLOW_OPERATING', 'CASHFLOW_INVESTING', 'CASHFLOW_FINANCING'])
        sns.barplot(x='QUARTER', y='value', hue='variable', data=df_melted, ax=ax)
        ax.set_title('Cash Flow Analysis')
        fig_html = mpld3.fig_to_html(fig)
        components.html(fig_html, height=600)
