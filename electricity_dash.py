# import packages
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, dash_table, Input, Output, State
import dash_bootstrap_components as dbc


# read in dataset
electricity = pd.read_csv('electricity.csv')

# create variables to make layout cleaner
year_min = min(electricity['Year'])
year_max = max(electricity['Year'])


# instantiate dash object
app = Dash(external_stylesheets=[dbc.themes.SOLAR])

# create layout
app.layout = html.Div([
    html.H1('Electricity Prices by US State'),
    dcc.RangeSlider(
        id='year-slider',
        min=year_min,
        max=year_max ,
        value=[year_min, year_max],
        marks={i:str(i) for i in range(year_min, year_max+1)}
    ),
    dcc.Graph(id='map-graph'),
    # adding Div section for interactivity of graph controlling table
    # html.Div(id='click-children'), # used that to see structure; don't need anymore
    dash_table.DataTable(id='price-info')
    # removed: data=electricity.to_dict('records')
    # b/c now it's coming from the second callback function
])

# callback area
@app.callback(
    Output('map-graph','figure'),
    # Output('price-info','data'),
    Input('year-slider', 'value')
)

def update_map_graph(selected_years):
    filtered_electricity = electricity[
                (electricity['Year'] >= selected_years[0]) &
                (electricity['Year'] <= selected_years[1])]
    avg_prices_df = filtered_electricity.groupby('US_State')['Residential Price'].mean().reset_index()
    map_fig = px.choropleth(avg_prices_df,
                        locations='US_State',
                        locationmode='USA-states',
                        color='Residential Price',
                        scope='usa',
                        color_continuous_scale='reds')
    return map_fig

@app.callback(
    # this one will use dcc.Graph interactive properties
    #  Output('click-children', 'children'),  # this was just to see the structure
    Output('price-info', 'data'),
    Input('map-graph', 'clickData'),
    Input('year-slider', 'value')
)

def update_datatable(clicked_data, selected_years):
    if clicked_data is None:
        return []
    clicked_state = clicked_data['points'][0]['location']
    filtered_electricity = electricity[
                                (electricity['Year']>=selected_years[0]) &
                                (electricity['Year']<=selected_years[1]) &
                                (electricity['US_State']==clicked_state)]
    return filtered_electricity.to_dict('records')
    # return str(clicked_data)  # only used this to see structure of this item
                              # to know how to pull out what is needed
                              # from the complicated dictionary
    # here's what it looks like
    # {'points': [{'curveNumber': 0, 'pointNumber': 38, 'pointIndex': 38, 
    # 'location': 'PA', 'z': 11.074333333333334, 
    # 'bbox': {'x0': 589.8674840402983, 'x1': 589.8674840402983, 
    # 'y0': 265.3324707223069, 'y1': 265.3324707223069}}]}
    # so we'll need
    # clicked_data['points']['location']

# run the app
if __name__=='__main__':
    app.run_server(debug=True)