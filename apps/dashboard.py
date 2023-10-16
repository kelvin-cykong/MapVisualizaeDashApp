from dash import html, dcc
import dash_bootstrap_components as dbc

layout = html.Div([
    dbc.Spinner(children=[
    html.Div(html.H1("Dashboard")),
    # Rest of your dashboard components
    html.Br(),
    html.Br(),
    dbc.Button('Logout', id='logout-button', n_clicks=0, className="mt-2")
])
],style={'padding':'40px'})