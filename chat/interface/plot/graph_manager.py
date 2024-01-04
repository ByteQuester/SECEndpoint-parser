from streamlit_elements import nivo
from .profitability.plot_profitability import PlotProfitability


class GraphManager:
    def __init__(self):
        self.category_to_class = {
            'Profitability': PlotProfitability
            # 'Liquidity': PlotLiquidity,
            # Add more categories and corresponding classes
        }

    def get_plot_class(self, category):
        return self.category_to_class.get(category)

    def get_available_charts(self, category):
        plot_class = self.get_plot_class(category)
        if plot_class:
            return plot_class.get_available_charts()
        return []

