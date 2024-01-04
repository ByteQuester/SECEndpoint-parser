import streamlit as st
from streamlit_elements import elements, nivo, mui
from chat.interface.plot.profitability.plot_profitability import PlotProfitability
import json

with open('data/0000012927/processed_json/Profitability/bar_chart/0000012927_Profitability_bar_chart_20240103183509.json', 'r') as json_file:
    json_data = json.load(json_file)

st.title("Bar Chart Test")

with elements("nivo_charts"):
    with mui.Box(sx={"height": 400}):
        plot_profitability = PlotProfitability(json_data)
        bar_chart_config = plot_profitability.bar_chart(json_data)
        nivo.Bar(**bar_chart_config)


