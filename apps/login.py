from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State


layout = html.Div([
    html.Div(children=['User Login Page'], id='headline'),
    html.Br(),
    dbc.Input(id="username", placeholder="Username", type="text", style={'width':'450px'}),
    dbc.Input(id="password", placeholder="Password", type="password", className="mt-2", style={'width':'450px'}),
    html.Br(),
    dbc.Button('Login', id='login-button', n_clicks=0, className="mt-2", style={"marginRight": "10px"}),
    dbc.Button('Forgot Username/Password', id='forgot-button', n_clicks=0, className="mt-2", style={"marginRight": "10px"}),
    html.Br(),
    html.Br(),
    html.Div(id="error-div", style={'width': '450px'})
], style={'margin': '40px 40px 0px 40px', 'align':'center'})

