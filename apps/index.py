from dash import html
from dash.dependencies import Input, Output, State
import dash
from app import app, server

from dash import dcc
import dash_bootstrap_components as dbc

# Import Other Pages.
import login
import dashboard


## Import other supporting modules
import time
import json
with open('site_assets/login_details.json', 'r') as file:
    data = json.load(file)
    user_data = data["login_details"]

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),    # Represents the URL bar
    dbc.NavbarSimple(brand='Interactive Data Dashboard', brand_href="#", color='primary', dark=True),
    html.Div(id='page-content', style={'overflow':'auto'}),
    dcc.Store('login_status'),
    dcc.Store('user_id')
])

### LOGIN ROUTING
@app.callback(Output(component_id='page-content', component_property='children'),
            [Input(component_id='url', component_property='pathname')],
            State(component_id='user_id', component_property='data'))

def display_page(pathname, user_id):
    if pathname == '/':
        return login.layout
    elif pathname == '/login':
        return login.layout
    elif pathname == '/dashboard':
        if user_id is not None:
            return dashboard.layout
        else:
            return login.layout
    # Add more pages as needed
    else:
        return "404: Not Found"  # This can be a better-designed 404 page

@server.route('/dashboard')
def dashboard_page():
    return dashboard.layout
### LOGIN
@app.callback(
    Output(component_id='login_status', component_property='data', allow_duplicate=True),
    Output(component_id='error-div', component_property='children'),
    [Input(component_id='login-button', component_property='n_clicks')],
    [State(component_id='username', component_property='value'), 
     State(component_id='password', component_property='value')],
     prevent_initial_call=True
)
def update_output(n_clicks, username, password):
    Error_Message = "Wrong Username/Password!"
    Missing_Message_1 = "Username is required."
    Missing_Message_2 = "Password is required."
    Missing_Message_3 = "Username and Password are required."
    # Check user credentials (use a secure method in real-world scenarios)
    if n_clicks:
        if username in user_data.keys() and password == user_data[username]:
            # Use Flask's redirect and url_for functions
            return "True", dbc.Alert('Logged in Successful!', color="success")
        elif username in user_data.keys() and password != user_data[username]:
            return "False", dbc.Alert(Error_Message, color="danger")
        elif username not in user_data.keys() and password is not None:
            return "False", dbc.Alert(Error_Message, color="danger")
        elif not username:
            return "False", dbc.Alert(Missing_Message_1, color="danger")
        elif not password:
            return "False", dbc.Alert(Missing_Message_2, color="danger")
        elif not username and not password:
            return "False", dbc.Alert(Missing_Message_3, color="danger")
        else:
            return "False", None
    return dash.no_update, None

        
@app.callback(
    Output(component_id='url', component_property='pathname', allow_duplicate=True),
    Output(component_id='user_id', component_property='data', allow_duplicate=True),
    [Input(component_id='login_status', component_property='data')],
    State(component_id='username', component_property='value'),
    prevent_initial_call=True
)
def check_login_successful(login_status, username):
    if login_status:
        if login_status == 'True':
            time.sleep(0.5)
            return '/dashboard', username
        else:
            return dash.no_update, None


### LOGOUT
@app.callback(
    Output(component_id='url', component_property='pathname', allow_duplicate=True),
    Output(component_id='user_id', component_property='data', allow_duplicate=True),
    [Input(component_id='logout-button', component_property='n_clicks')],
    prevent_initial_call=True
)
def update_output(n_clicks):
    # Check user credentials (use a secure method in real-world scenarios)
    if n_clicks:
        # Use Flask's redirect and url_for functions
        return "/login", None
    else:
        return dash.no_update, dash.no_update


### DASHBOARD CALLBACK
@app.callback(
    Output(component_id='welcome_message', component_property='children'),
    Output(component_id='graph1', component_property='children'),
    Input(component_id='user_id', component_property='data')
)

def display_user_name(user_id):
    from dashboard import create_figure
    if user_id:
        message = 'Welcome {}!'.format(user_id)
        figure = create_figure()
        return message, dcc.Graph(figure=figure, style={'height': '100%'})


if __name__ == '__main__':
    app.run_server(debug=True)