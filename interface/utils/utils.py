from mpld3 import plugins
import matplotlib.pyplot as plt


def add_tooltips(fig, lines, labels):
    css = """
    table
    {
      border-collapse: collapse;
    }
    th
    {
      color: #ffffff;
      background-color: #000000;
    }
    td
    {
      background-color: #cccccc;
    }
    table, th, td
    {
      font-family:Arial, Helvetica, sans-serif;
      border: 1px solid black;
      text-align: right;
    }
    """

    for line in lines:
        xy_data = line.get_xydata()
        labels_html = [labels.format(x=x, y=y) for x, y in xy_data]
        tooltip = plugins.PointHTMLTooltip(line, labels_html, css=css)
        plugins.connect(fig, tooltip)
