import pandas as pd

from autoviz.AutoViz_Class import AutoViz_Class

# load df data/year_price.csv
df = pd.read_csv("data/year_price.csv")

# autoviz data/year_price.csv
av = AutoViz_Class()
chart = av.AutoViz(
    filename="",
    sep=",",
    depVar="",
    dfte=df,
    header=0,
    verbose=2,
    lowess=False,
    chart_format="html",
    max_rows_analyzed=150000,
    max_cols_analyzed=30,
    save_plot_dir="year_price_plot"
)

print(chart)
