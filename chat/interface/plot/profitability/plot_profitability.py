

class PlotProfitability:
    def __init__(self, df):
        self.df = df

    @staticmethod
    def get_available_charts():
        return {
            'line_chart': PlotProfitability.line_chart,
            'bar_chart': PlotProfitability.bar_chart,
            # Add more chart types and their methods
        }

    @staticmethod
    def line_chart(df):
        config = {
            'data': df,
            'margin': {'top': 50, 'right': 110, 'bottom': 50, 'left': 60},
            'xScale': {'type': 'point'},
            'yScale': {
                'type': 'linear',
                'min': 'auto',
                'max': 'auto',
                'stacked': True,
                'reverse': False
            },
            'yFormat': " >-.2f",
            'axisTop': None,
            'axisRight': None,
            'axisBottom': {
                'orient': 'bottom',
                'tickSize': 5,
                'tickPadding': 5,
                'tickRotation': 0,
                'legend': 'Date',
                'legendOffset': 36,
                'legendPosition': 'middle'
            },
            'axisLeft': {
                'orient': 'left',
                'tickSize': 5,
                'tickPadding': 5,
                'tickRotation': 0,
                'legend': 'Amount',
                'legendOffset': -40,
                'legendPosition': 'middle'
            },
            'pointSize': 10,
            'pointColor': {'theme': 'background'},
            'pointBorderWidth': 2,
            'pointBorderColor': {'from': 'serieColor'},
            'pointLabelYOffset': -12,
            'useMesh': True,
            'legends': [
                {
                    'anchor': 'bottom-right',
                    'direction': 'column',
                    'justify': False,
                    'translateX': 100,
                    'translateY': 0,
                    'itemsSpacing': 0,
                    'itemDirection': 'left-to-right',
                    'itemWidth': 80,
                    'itemHeight': 20,
                    'itemOpacity': 0.75,
                    'symbolSize': 12,
                    'symbolShape': 'circle',
                    'symbolBorderColor': 'rgba(0, 0, 0, .5)',
                    'effects': [
                        {
                            'on': 'hover',
                            'style': {
                                'itemBackground': 'rgba(0, 0, 0, .03)',
                                'itemOpacity': 1
                            }
                        }
                    ]
                }
            ],
            'theme': {
                'background': '#ffffff',
                'textColor': '#333333',
                'tooltip': {
                    'container': {
                        'background': '#ffffff',
                        'color': '#333333',
                    }
                }
            }
        }

        return config
    @staticmethod
    def bar_chart(df):
        config = {
            'data': df,
            'keys': ["NetIncomeLossValue", "RevenuesValue", "OperatingIncomeLossValue", "ProfitMarginPercentValue"],
            'indexBy': "quarter",
            'margin': {"top": 50, "right": 130, "bottom": 50, "left": 60},
            'padding': 0.3,
            'valueScale': {"type": "linear"},
            'indexScale': {"type": "band", "round": True},
            'colors': {"scheme": "nivo"},
            'borderColor': {"from": "color", "modifiers": [["darker", 1.6]]},
            'axisTop': None,
            'axisRight': None,
            'axisBottom': {
                "tickSize": 5,
                "tickPadding": 5,
                "tickRotation": 0,
                "legend": "Quarter",
                "legendPosition": "middle",
                "legendOffset": 32
            },
            'axisLeft': {
                "tickSize": 5,
                "tickPadding": 5,
                "tickRotation": 0,
                "legend": "Value",
                "legendPosition": "middle",
                "legendOffset": -40
            },
            'labelSkipWidth': 12,
            'labelSkipHeight': 12,
            'labelTextColor': {"from": "color", "modifiers": [["darker", 1.6]]},
            'legends': [
                {
                    "dataFrom": "keys",
                    "anchor": "bottom-right",
                    "direction": "column",
                    "justify": False,
                    "translateX": 120,
                    "translateY": 0,
                    "itemsSpacing": 2,
                    "itemWidth": 100,
                    "itemHeight": 20,
                    "itemDirection": "left-to-right",
                    "itemOpacity": 0.85,
                    "symbolSize": 20
                }
            ],
            'role': "application",
            'ariaLabel': "Profitability bar chart",
            'barAriaLabel': lambda e: f"{e.id}: {e.formattedValue} in quarter: {e.indexValue}"
        }
        return config
