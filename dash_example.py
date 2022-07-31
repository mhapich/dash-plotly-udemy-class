from distutils.log import debug
from turtle import title
from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px

happiness = pd.read_csv('world_happiness.csv')


app=Dash()

app.layout=html.Div([
    html.H1('World Happiness Dashboard'),
    html.P(['This dashboard shows the happiness score.',
             html.Br(),
             html.A('World Happiness Report Data Source',
                     href='https://worldhappiness.report',
                     target='_blank')]),
    dcc.RadioItems(id='region-radio',
                    options=happiness['region'].unique(),
                    value='North America'),
    dcc.Dropdown(id='country-dropdown'),
    dcc.RadioItems(id='data-radio',
                   options={'happiness_score':'Happiness Score',
                            'happiness_rank':'Happiness Rank'},
                   value='happiness_score'),
    dcc.Graph(
        id='happiness-graph'),
    html.Div(id='average-div')
    ])

# to chain callbacks, we first let the radio button choice of region
# set both the options and value for the country dropdown
@app.callback(
    Output('country-dropdown', 'options'),
    Output('country-dropdown', 'value'),
    Input('region-radio', 'value')
)

# this decorator needs its own function
def update_dropdown(selected_region):
    filtered_happiness=happiness[happiness['region']==selected_region]
    country_list = filtered_happiness['country'].unique()
    return country_list, country_list[0] 

@app.callback(
    Output('happiness-graph', 'figure'),
    Output('average-div', 'children'),
    Input('country-dropdown', 'value'),
    Input('data-radio', 'value')
)
def update_graph(selected_country, selected_data):
    filtered_happiness = happiness[happiness['country'] == selected_country]
    names_dict = {'happiness_score':'Happiness Score',
                  'happiness_rank':'Happiness Rank'}
    line_fig = px.line(filtered_happiness, 
                       x='year', y=selected_data, 
                       title=f'{names_dict.get(selected_data)} in {selected_country}').update_layout(yaxis_title=names_dict.get(selected_data))
    selected_avg =  round(filtered_happiness[selected_data].mean(),2)
    return line_fig, f'The average {names_dict.get(selected_data)} for {selected_country} is {selected_avg}.'

if __name__=='__main__':
    app.run_server(debug=True)  # change to False when deploying/after development
