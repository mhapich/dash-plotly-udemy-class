# Display avocado price info for user-selected areas

# import packages
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output

app = Dash()

avocados = pd.read_csv('avocado.csv')

app.layout = html.Div([
    html.H1('Avocado Prices Dashboard'),
    dcc.Dropdown(id='place-dd', 
                 options=avocados['geography'].unique(),
                 value='Albany'),
    dcc.Graph(id='prices-line-graph')
])

@app.callback(
    Output('prices-line-graph', 'figure'),
    Input('place-dd', 'value')
)

def update_graph(selected_place):
    df = avocados[avocados['geography']==selected_place]
    lines_fig = px.line(df, x='date', y='average_price', 
                        color='type',
                        title=f'Avocado prices in {selected_place}')
    return lines_fig


if __name__=='__main__':
    app.run_server(debug=True)