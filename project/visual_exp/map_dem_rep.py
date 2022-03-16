'''
Program to experiment with data visualization for USA counties
'''

from urllib.request import urlopen
import json
import dash
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd


app = dash.Dash()

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

df = pd.read_csv('~/Documents/UChicago/Q2_Winter_2022/capp30122_ACS/proj-python_parser_tongues/visual_exp/cdc_data.csv', dtype={"fips": str})

min_bar = min(i for i in df['comp_vax_rate'] if i >0)

fig = px.choropleth(df, geojson=counties, locations='fips', color='comp_vax_rate',
                           color_continuous_scale="Blues",
                           range_color=(min_bar, 100),
                           scope="usa",
                           labels={'comp_vax_rate':'Vaccination Rate'}
                          )

fig.update_traces(marker_line_width=0.1, marker_opacity=0.85)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.update_geos(showsubunits=True, subunitcolor="black")

#fig.show()
app.layout = html.Div([dcc.Graph(id="life-exp-vs-gdp", figure=fig)])

if __name__ == "__main__":
    app.run_server(debug=True)