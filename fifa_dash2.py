# import packages
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc

# read in dataset
soccer = pd.read_csv('fifa_soccer_players.csv')

# set up navbar
navbar = dbc.NavbarSimple(
    brand='Soccer Players Dashboard',
    children=[
        html.Img(src='https://uptime.com/media/website_profiles/sofifa.com.png',
                  height=20),
        html.A('Data Source',
                href='https://sofifa.com',
                target='_blank',
                style={'color':'black'})
    ],
    color='primary',
    fluid=True
)

# instantiate Dash app using bootstrap components
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


# set up page layout
app.layout = html.Div(navbar)

# set up callback area


# run the app
from distutils.log import debug  # put here by vscode 

if __name__=='__main__':
    app.run_server(debug=True)