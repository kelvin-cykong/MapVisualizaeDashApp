from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go

### Tab content
tab1_content = dbc.Card(
    dbc.CardBody(
        [
            html.P("California Vehicle Status", className="card-text"),
            html.Div(id='graph1', style={'height': '65vh'})
        ]
    ),
    className="mt-3",
)

tab2_content = dbc.Card(
    dbc.CardBody(
        [
            html.P("This is tab 2!", className="card-text"),
            html.Div(id='graph2')
        ]
    ),
    className="mt-3",
)


tabs = dbc.Tabs(
    [
        dbc.Tab(tab1_content, label="Graph 1", tab_id='tab1'),
        dbc.Tab(tab2_content, label="Graph 2", tab_id='tab2'),
        dbc.Tab(
            "This tab's content is never seen", label="Tab 3", disabled=True
        ),
    ], active_tab="tab1"
)


### dashboard layout:
layout = html.Div([
    html.Div(html.H2("Interactive Data Dashboard")),
    # Rest of your dashboard components
    html.Div(id='welcome_message'),
    html.Br(),
    tabs,
    dbc.Button('Logout', id='logout-button', n_clicks=0, className="mt-2"),]
,style={'margin': '20px 40px 0px 40px'})


### Dashboard Function:

def read_vehicle_data():
    data2023 = pd.read_csv('https://data.ca.gov/dataset/15179472-adeb-4df6-920a-20640d02b08c/resource/9aa5b4c5-252c-4d68-b1be-ffe19a2f1d26/download/vehicle-fuel-type-count-by-zip-code-2022.csv')
    return data2023



def create_figure():
    california_geojson = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [-124.482003, 32.528832],
                        [-114.131212, 32.72083],
                        [-114.466556, 35.00186],
                        [-120.005746, 41.995232],
                        [-124.482003, 32.528832]
                    ]
                ]
            }
        }
    ]
    }

    fig = go.Figure(go.Choroplethmapbox(
        geojson=california_geojson,
        locations=[0],  # This refers to the indices of the features (just one in this example)
        z=[1],  # Dummy value for coloring
        colorscale="Viridis"
    ))

    fig.update_layout(
        mapbox_style="carto-positron",
        mapbox_zoom=5,
        mapbox_center={"lat": 36.7783, "lon": -119.4179}  # Centered on California
    )
    
    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))

    return fig