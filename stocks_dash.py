from dash import Dash, html, dcc, dash_table, Input, Output, State
import yfinance as yf
import plotly.graph_objects as go


price=yf.Ticker(' ').history(period='1d', interval='15m').reset_index()

app = Dash()

app.layout = html.Div([
    html.H1('My financial dashboard'),
    dcc.Input(id='ticker-input',
              placeholder='Search for symbols from Yahoo Finance',
              style={'width':'50%'}),
    html.Button(id='submit-button', children='Submit'),
    html.Br(),
    html.Br(),
    dcc.Tabs([
        dcc.Tab(label='Candlestick Chart', 
                children=dcc.Graph(id='stock-graph')),
        dcc.Tab(label = 'Recent Data', 
                children=dash_table.DataTable(
                    id='stock-data', 
                    data=price.tail(10).to_dict('records'))),
    ]),
    dcc.Interval(id='chart-interval', interval=1000*60*15, n_intervals=0),
    dcc.Interval(id='table-interval', interval=1000*60, n_intervals=0)
])

@app.callback(
    # the graph will be updated
    Output('stock-graph', 'figure'),
    # by either the submit button being clicked or time passing
    Input('submit-button', 'n_clicks'), 
    Input('chart-interval', 'n_intervals'),
    # the chosen stock symbol will be held as a state until a trigger is made
    State('ticker-input', 'value')
)

def update_chart(button_click, chart_interval, stock_symbol):
    if stock_symbol is None:
        return {}
    price=yf.Ticker(stock_symbol).history(period='1d', interval='15m').reset_index()
    if len(price) == 0:
        return {}
    # create graph here for layout
    fig = go.Figure(data=go.Candlestick(x=price['Datetime'],
                open=price['Open'],
                high=price['High'],
                low=price['Low'],
                close=price['Close']))  
    return fig

if __name__=='__main__':
    app.run_server(debug=True)