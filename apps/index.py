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
    dcc.Location(id='url', refresh=False),
    # Represents the URL bar
    html.Div(id='page-content'),
    dcc.Store('login_status'),
    dcc.Store('user_id')
])

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

@app.callback(
    Output(component_id='login_status', component_property='data'),
    Output(component_id='error-div', component_property='children'),
    [Input(component_id='login-button', component_property='n_clicks')],
    [State(component_id='username', component_property='value'), 
     State(component_id='password', component_property='value')],
     prevent_initial_call='initial_duplicate'
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
            return "True", 'Logged in Successful!'
        elif username in user_data.keys() and password != user_data[username]:
            return "False", Error_Message
        elif username not in user_data.keys() and password is not None:
            return "False", Error_Message
        elif not username:
            return "False", Missing_Message_1
        elif not password:
            return "False", Missing_Message_2
        elif not username and not password:
            return "False", Missing_Message_3
        else:
            return "False", None
    return dash.no_update, None

        
@app.callback(
    Output(component_id='url', component_property='pathname', allow_duplicate=True),
    Output(component_id='user_id', component_property='data'),
    [Input(component_id='login_status', component_property='modified_timestamp')],
    [State(component_id='login_status', component_property='data'),
    State(component_id='username', component_property='value')],
    prevent_initial_call='initial_duplicate'
)
def check_login_successful(timestamp, login_status, username):
    if timestamp:
        if login_status == 'True':
            time.sleep(0.5)
            return '/dashboard', username
        else:
            return dash.no_update, None
    else:
        return dash.no_update, None



@app.callback(
    Output('url', 'pathname', allow_duplicate=True),
    [Input(component_id='logout-button', component_property='n_clicks')],
    prevent_initial_call=True
)
def update_output(n_clicks):
    # Check user credentials (use a secure method in real-world scenarios)
    if n_clicks:
        # Use Flask's redirect and url_for functions
        return "/login"

@server.route('/dashboard')
def dashboard_page():
    return dashboard.layout

if __name__ == '__main__':
    app.run_server(debug=True)