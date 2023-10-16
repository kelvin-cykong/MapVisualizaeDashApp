from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State


layout = html.Div([
    html.Div(children=['Interactive Dashboard Login Page'], id='headline'),
    html.Br(),
    dbc.Input(id="username", placeholder="Username", type="text"),
    dbc.Input(id="password", placeholder="Password", type="password", className="mt-2"),
    html.Br(),
    dbc.Button('Submit', id='login-button', n_clicks=0, className="mt-2"),
    html.Div(id="error-div")
], style={'padding':'40px'})
