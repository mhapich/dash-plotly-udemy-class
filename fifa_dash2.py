# import packages
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc

# read in dataset
soccer = pd.read_csv('fifa_soccer_players.csv')

# calculate statistics for cards
avg_age = soccer['age'].mean()
avg_height = soccer['height_cm'].mean()
avg_weight = soccer['weight_kg'].mean()

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

# create cards to be used in layout
cards = dbc.Row([dbc.Col(dbc.Card([
                                html.H4('Average Age'),
                                html.H5(f'{round(avg_age, 1)} years')],
                                body=True,
                                style={'textAlign':'center', 'color':'white'},
                                color='lightblue')),
                 dbc.Col(dbc.Card([
                                html.H4('Average Height'),
                                html.H5(f'{round(avg_height, 1)} cm')],
                                body=True,
                                style={'textAlign':'center', 'color':'white'},
                                color='blue')),
                 dbc.Col(dbc.Card([
                                html.H4('Average Weight'),
                                html.H5(f'{round(avg_weight, 1)} kg')],
                                body=True,
                                style={'textAlign':'center', 'color':'white'},
                                color='darkblue'))
])

# instantiate Dash app using bootstrap components
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


# set up page layout
app.layout = html.Div([navbar, html.Br(), cards])

# set up callback area


# run the app
from distutils.log import debug  # put here by vscode 

if __name__=='__main__':
    app.run_server(debug=True)