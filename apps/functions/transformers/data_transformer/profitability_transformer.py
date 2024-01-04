
class ProfitabilityTransformer:
    def __init__(self, df):
        self.df = df

    def transform_for_bar_chart(self, df):
        # Create a dictionary to group data by quarter
        transformed_data = {}
        for _, row in df.iterrows():
            quarter_key = f"{row['Year']} {row['Quarter']}"
            if quarter_key not in transformed_data:
                transformed_data[quarter_key] = {"quarter": quarter_key}

            # Add data for each metric
            for metric in ["NetIncomeLoss", "Revenues", "OperatingIncomeLoss", "ProfitMarginPercent"]:
                metric_key = metric + "Value"
                color_key = metric + "Color"
                transformed_data[quarter_key][metric_key] = row[metric]
                transformed_data[quarter_key][color_key] = f"hsl({hash(metric) % 360}, 70%, 50%)"

        # Convert dictionary to list as required by the bar chart
        return list(transformed_data.values())

    def transform_for_line_chart(self, df):
        transformed_data = []

        for metric in ["NetIncomeLoss", "Revenues", "OperatingIncomeLoss", "ProfitMarginPercent"]:
            line_data = {
                "id": metric,
                "color": "hsl({0}, 70%, 50%)".format(hash(metric) % 360),  # Generating a unique color for each line
                "data": []
            }

            for _, row in df.iterrows():
                point = {
                    "x": row["DATE"],
                    "y": row[metric]
                }
                line_data["data"].append(point)

            transformed_data.append(line_data)

        return transformed_data

    def transform_for_pie_chart(self, df):
        # Transformation logic specific to pie charts
        # Return transformed JSON data
        pass

    def transform_all(self, df):
        # Calls all transformation methods and aggregates results
        return {
            "line_chart": self.transform_for_line_chart(df),
            "bar_chart": self.transform_for_bar_chart(df),
            # Add other chart transformations here
        }

