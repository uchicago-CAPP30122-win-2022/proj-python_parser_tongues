'''
Program to experiment with data visualization for USA counties
'''

from urllib.request import urlopen
import json
import dash
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd


#app = Dash(__name__)
app = dash.Dash(external_stylesheets =
    [dbc.themes.BOOTSTRAP, 'https://codepen.io/chriddyp/pen/bWLwgP.css'])

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)


#=========================
app.layout = html.Div([
    html.H4('Vaccination Rates in USA'),
    html.P("Choose an Indicator:"),
    dcc.RadioItems(
        id='vax_type', 
        options=[
            {'label':'Complete Vaccination Rate by State', 'value':'GEN_VAX_RATE'},
            {'label':'Complete Vaccination Rate by County', 'value':'COUN_VAX_RATE'},
            {'label':'Booster Application General Rate', 'value':'BOOSTER_RATE'},
            {'label':'Booster Application 18+ Rate', 'value':'BOOSTER_RATE_18UP'},
            {'label':'Booster Application 65+ Rate', 'value':'BOOSTER_RATE_65UP'},
            {'label':'General Vaccination in Democrat States', 'value':'DEM'},
            {'label':'General Vaccination in Republican States', 'value':'REP'}
            ],
        value="GEN_VAX_RATE"
    ),
    dcc.Graph(id="graph"),
])
#=========================


@app.callback(
    Output("graph", "figure"), 
    Input("vax_type", "value"))
def display_choropleth(vax_type):
    
    if vax_type == "REP":
        df = pd.read_csv('data/data.csv', dtype={"FIPS": str})
        df['FIPS']=df['FIPS'].apply(lambda x: '{0:0>5}'.format(x))
        df = df[df['DEM_WON']==0]
        min_bar = min(i for i in df[vax_type] if i >0)

        fig = px.choropleth(df,
                        geojson=counties,
                        locations='FIPS',
                        color=vax_type,
                        color_continuous_scale="Reds",
                        range_color=(min_bar, 100),
                        scope="usa",
                        hover_name = 'COUNTY',
                        labels={vax_type:'Vaccination Rate',
                                        'FIPS':'County FIPS'}
                        )
        fig.update_traces(marker_line_width=0.1, marker_opacity=0.85)
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        fig.update_geos(showsubunits=True, subunitcolor="black")

        return fig
    elif vax_type == "DEM":
        df = pd.read_csv('data/data.csv', dtype={"FIPS": str})
        df['FIPS']=df['FIPS'].apply(lambda x: '{0:0>5}'.format(x))
        df = df[df['DEM_WON']==1]
        min_bar = min(i for i in df[vax_type] if i >0)

        fig = px.choropleth(df,
                        geojson=counties,
                        locations='FIPS',
                        color=vax_type,
                        color_continuous_scale="Blues",
                        range_color=(min_bar, 100),
                        scope="usa",
                        hover_name = 'COUNTY',
                        labels={vax_type:'Vaccination Rate',
                                        'FIPS':'County FIPS'}
                        )
        fig.update_traces(marker_line_width=0.1, marker_opacity=0.85)
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        fig.update_geos(showsubunits=True, subunitcolor="black")

        return fig

    else:
        df = pd.read_csv('data/data.csv', dtype={"FIPS": str})
        df['FIPS']=df['FIPS'].apply(lambda x: '{0:0>5}'.format(x))
        min_bar = min(i for i in df[vax_type] if i >0)

        fig = px.choropleth(df,
                        geojson=counties,
                        locations='FIPS',
                        color=vax_type,
                        color_continuous_scale="Greens",
                        range_color=(min_bar, 100),
                        scope="usa",
                        hover_name = 'COUNTY',
                        labels={vax_type:'Vaccination Rate',
                                        'FIPS':'County FIPS'}
                        )
        fig.update_traces(marker_line_width=0.1, marker_opacity=0.85)
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        fig.update_geos(showsubunits=True, subunitcolor="black")

        return fig


app.run_server(debug=True)
