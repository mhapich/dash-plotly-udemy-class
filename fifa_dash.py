# Dash dashboard using fifa soccer players csv

from distutils.log import debug
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc

# import dataset
fifa_df = pd.read_csv('fifa_soccer_players.csv')

app = Dash(external_stylesheets=[dbc.themes.CYBORG])

app.layout = html.Div([
    html.H1('Soccer Players Dashboard'),
    dbc.Row([dbc.Col(html.P(['Source: ',
                     html.A('Sofifa',
                     href='https://sofifa.com',
                     target='_blank')])),
            dbc.Col([html.Label('Player name: '),
                     dcc.Dropdown(id='pname-dd',
                     options=fifa_df['long_name'].unique(),
                     value=fifa_df['long_name'].unique()[0])
            ])
            ])    
])

if __name__=='__main__':
    app.run_server(debug=True)
