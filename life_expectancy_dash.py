# import packages
from distutils.log import debug
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc

# read in data
life_exp = pd.read_csv('life_expectancy.csv')

# helper items
year_min = min(life_exp['year'])
year_max = max(life_exp['year'])

countries = ['Afghanistan', 'American Samoa', 'Yemen']
three_df = life_exp[life_exp['country'].isin(countries)]
fig = px.line(three_df, x='year', y='life expectancy', color='country')

# create Dash object with theme
app = Dash(external_stylesheets=[dbc.themes.ZEPHYR])

# create navbar for layout
navbar = dbc.NavbarSimple(
    brand='Life Expectancy by Country',
    children=[html.A('Data Source',
              href='https://ourworldindata.org/life-expectancy',
              target='_blank',
              style={'color':'white'})],
    color='darkblue',
    dark=True
)

# create layout
app.layout = html.Div([
    navbar,
    # style={'padding':10},   # still trying to figure this out - this didn't compile
    html.Br(), html.Br(), 
    dcc.RangeSlider(id='year-slider', 
                    min=year_min,
                    max=year_max,
                    value=[year_min, year_max],
                    marks={i:str(i) for i in range(year_min, year_max+1,10)},
                    step=1,
                    tooltip={'placement':'top'}),
    html.Div([
        html.Br(),
        html.P('Choose one or more countries to see its life expectancy during the years you selected.'),
        dcc.Dropdown(id='country-dropdown', options=life_exp['country'].unique(), multi=True,
                     placeholder='Start to type country name or scroll to select'),
        html.Button(id='submit-button', children='Submit', style={'backgroundColor':'lightblue'}),
        html.Br(),
        dcc.Graph(id='life-exp-graph', figure=fig)
         ],
        style={'padding':'50px'}
    )
    
])

# create callback and function


# run the app
if __name__=='__main__':
    app.run_server(debug=True)