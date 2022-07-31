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
    dcc.Dropdown(id='country-dropdown',
                 options=happiness['country'].unique(), 
                 value='United States'),
    dcc.RadioItems(id='data-radio',
                   options={'happiness_score':'Happiness Score',
                            'happiness_rank':'Happiness Rank'},
                   value='happiness_score'),
    dcc.Graph(
        id='happiness-graph')
    ])

@app.callback(
    Output('happiness-graph', 'figure'),
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
    return line_fig

if __name__=='__main__':
    app.run_server(debug=True)  # change to False when deploying/after development
