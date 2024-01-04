from .data_transformer import ProfitabilityTransformer


class TransformerManager:
    def __init__(self):
        pass

    def transform_profitability_data(self, df, chart_type=None):
        transformer = ProfitabilityTransformer(df)
        if chart_type is None:
            return transformer.transform_all(df)
        elif chart_type == 'line_chart':
            return transformer.transform_for_line_chart(df)
        elif chart_type == 'bar_chart':
            return transformer.transform_for_bar_chart(df)
        # Add more conditions for other chart types
        else:
            raise ValueError("Unsupported chart type for profitability")

    # def transform_liquidity_data(self, df):
        # Call the liquidity transformation function
        # return liquidity_to_json(df)

    # ... Other transformation methods ...

    def transform_data(self, df, category, chart_type):
        """
        General method to transform data based on category.
        """
        if category == "Profitability":
            return self.transform_profitability_data(df, chart_type)
        # elif category == "Liquidity":
            # return self.transform_liquidity_data(df, chart_type)
        # placeholder for other categories as needed
        else:
            raise ValueError("Unsupported category")
