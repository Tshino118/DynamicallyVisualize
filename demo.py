import base64
from genericpath import isfile
import io
import pathlib
import os
import numpy as np
import dash_core_components as dcc
import dash_html_components as html
#from dash.dependencies import Input, Output, State
""" 
from PIL import Image
from io import BytesIO
from dash.exceptions import PreventUpdate
"""

import dataRead

# get relative data folder
PATH = pathlib.Path(__file__).parent

path_isfile=os.path.isfile
path_isdir=os.path.isdir

ids={
    "app-header":["plotly-image","app-title"],
    "demo-explanation":["description-text","learn-more-button"],
    "app-body":{
        "setting":[
            "dropdown-setting-dataset",
            "checklist-setting-id_user-all",
            "checklist-setting-id_user",
            "checklist-setting-week-all",
            "checklist-setting-week",
            "checklist-setting-eye_state-all",
            "checklist-setting-eye_state",
            "slider-setting-numberOfClusters"
        ],
        "main-graph":[
            "select-data",
            "graph-3d-plot"
        ],
        "plot-click":[
            "div-plot-click-message",
            "div-plot-click-image"
        ]

    }
}


'''
def numpy_to_b64(array, scalar=True):
    # Convert from 0-1 to 0-255
    if scalar:
        array = np.uint8(255 * array)

    im_pil = Image.fromarray(array)
    buff = BytesIO()
    im_pil.save(buff, format="png")
    im_b64 = base64.b64encode(buff.getvalue()).decode("utf-8")

    return im_b64
'''

# Methods for creating components in the layout code
def Card(children, **kwargs):
    return html.Section(children, className="card-style")

def NamedSlider(name, short, min, max, step, val, marks=None):
    if marks:
        step = None
    else:
        marks = {i: i for i in range(min, max + 1, step)}

    return html.Div(
        style={"margin": "25px 5px 30px 0px"},
        children=[
            f"{name}:",
            html.Div(
                style={"margin-left": "5px"},
                children=[
                    dcc.Slider(
                        id=f"slider-{short}",
                        min=min,
                        max=max,
                        marks=marks,
                        step=step,
                        value=val,
                    )
                ],
            ),
        ],
    )

def NamedChecklist(name, short, options):
    return html.Div(
        style={"margin": "25px 5px 30px 0px"},
        children=[
            f"{name}:",
            html.Div(
                style={"margin-left": "5px"},
                children=[
                    dcc.Checklist(
                        id=f"checklist-{short}-all",
                        options=[{'label':'All','value':'All'}],
                        value=['All'],
                        labelStyle={'display': 'inline-block'}
                    ),
                    dcc.Checklist(
                        id=f"checklist-{short}",
                        options=options,
                        value=[],
                        labelStyle={'display': 'inline-block'}
                    )
                ],
            ),
        ],
    )

def NamedInlineRadioItems(name, short, options, val, **kwargs):
    return html.Div(
        id=f"div-{short}",
        style={"display": "inline-block"},
        children=[
            f"{name}:",
            dcc.RadioItems(
                id=f"radio-{short}",
                options=options,
                value=val,
                labelStyle={"display": "inline-block", "margin-right": "7px"},
                style={"display": "inline-block", "margin-left": "7px"},
            ),
        ],
    )

def Header():
    # Header
    return html.Div(
                className="row header",
                id="app-header",
                style={"background-color": "#f9f9f9"},
                children=[
                    html.Div(
                        [
                            html.Img(
                                src='./asset/dash-logo.png',
                                className="logo",
                                id="plotly-image",
                            )
                        ],
                        className="three columns header_img",
                    ),
                    html.Div(
                        [
                            html.H3(
                                "Dynamically Visualize",
                                className="header_title",
                                id="app-title",
                            )
                        ],
                        className="nine columns header_title_container",
                    ),
                ],
            )

def description():
    #  Demo Description
    return html.Div(
            className="row background",
            id="demo-explanation",
            style={"padding": "50px 45px"},
            children=[
                html.Div(
                    id="description-text", children=dcc.Markdown()
                ),
                html.Div(
                    html.Button(id="learn-more-button", children=["Learn More"])
                ),
            ],
        )

def Body():
    dataClass=dataRead.dataSets
    #input_data=dataClass.Input_data()
    input_features=dataClass.Input_features()
    feature_unique=dataClass.Feature_unique(input_features)
    feature_dict=dataClass.Feature_dict(feature_unique)
    inputDataLabel=['lerp',"meanZero","medianZero","firstPointZero"]

    def Store():
        return html.Div(
            children=[
                #dcc.Store(
                #    id="indexes-store",
                #    storage_type="session",
                #    data=dataClass.Input_indexes(input_data),
                #    clear_data=False
                #),

                #dcc.Store(
                #    id="figure-store",
                #    storage_type="session",
                #    data=dataClass.Figure_dict(input_data),
                #    clear_data=False
                #),
                
                #dcc.Store(
                #    id="IO-store",
                #    storage_type="session",
                #    data=dataClass.IO_dict(feature_unique,input_features),
                #    clear_data=False
                #),
                #dcc.Store(
                #    id="kMeans-store",
                #    storage_type="session",
                #    data=dataClass.KMeans_dict(),
                #    clear_data=False
                #),
            ]
        )

    return html.Div(
        className="row background",
        id="app-body",
        style={"padding": "10px"},
        children=[
            html.Div(
                className="three columns",
                id="setting",
                children=[
                    Card([
                        dcc.Dropdown(
                            id="dropdown-setting-dataset",
                            searchable=False,
                            clearable=False,
                            options=[
                                {
                                    "label": key,
                                    "value": key
                                }
                                for key in inputDataLabel
                            ],
                            placeholder="Select a dataset",
                            value='lerp',
                        ),
                        NamedChecklist(
                            #id="checklist-setting-id_user-all"
                            #id="checklist-setting-id_user"
                            name="id_user",
                            short='setting-id_user',
                            options=feature_dict["id_user"]['options'],
                        ),
                        NamedChecklist(
                            #id="checklist-setting-week-all"
                            #id="checklist-setting-week"
                            name="week",
                            short='setting-week',
                            options=feature_dict["week"]['options'],
                        ),
                        NamedChecklist(
                            #id="checklist-setting-eye_state-all"
                            #id="checklist-setting-eye_state"
                            name="eye_state",
                            short='setting-eye_state',
                            options=feature_dict["eye_state"]['options'],
                        ),
                        NamedSlider(
                            #id="slider-setting-numberOfClusters"
                            name="Number of Clusters",
                            short="setting-numberOfClusters",
                            min=2,
                            max=10,
                            step=None,
                            val=2,
                            marks={
                                i: str(i) for i in range(2,10)
                            },
                        ),
                        dcc.Dropdown(
                            id="dropdown-setting-clusteringData",
                            searchable=False,
                            clearable=False,
                            options=[
                                {
                                    "label": key,
                                    "value": key
                                }
                                for key in ['x','y','xy']
                            ],
                            placeholder="Select clustering data set",
                            value='xy',
                        ),
                        dcc.Dropdown(
                            id="dropdown-setting-graph_type",
                            searchable=False,
                            clearable=False,
                            options=[
                                {"label": 'CoPx-CoPy-time',"value": "timeXY"},
                                {"label": 'time-CoPx',"value": "timeX"},
                                {"label": 'time-CoPy',"value": "timeY"},
                                {"label": 'CoPx-CoPy',"value": "XY"},
                            ],
                            placeholder="Selects graph type",
                            value=["timeX","timeY","XY"],
                            multi=True
                        ),
                        dcc.Dropdown(
                            id="dropdown-graph-color",
                            searchable=False,
                            clearable=False,
                            options=[
                                {"label": 'id',"value": "id_user"},
                                {"label": 'week',"value": "week"},
                                {"label": 'eye state',"value": "eye_state"},
                                {"label": 'cluster',"value": "cluster"},
                            ],
                            placeholder="Selects graph color",
                            value=["id_user"],
                            multi=True
                        ),
                        dcc.Store(id='color-store',storage_type='session'),
                        html.Button(
                            children="submit",
                            id="setting-submit",
                            n_clicks=0
                        )
                    ]),
                ],            
            ),
            html.Div(
                className="six columns",
                id="main-graph",
                children=[
                    html.Div(id="graph-color"),
                    html.Hr(),
                    dcc.Loading(
                        children=html.Div(id="graph-area")
                    )
                ],
            ),
            html.Div(
                className="three columns",
                id="plot-click",
                children=[
                    Card(
                        style={"padding": "5px"},
                        children=[
                            html.Div(
                                id="div-plot-click-message",
                                children=['click-message'],
                                style={
                                    "text-align": "center",
                                    "margin-bottom": "7px",
                                    "font-weight": "bold",
                                },
                            ),
                            html.Div(id="div-plot-click-image"),
                            #html.Div(id="div-plot-click-wordemb"),
                        ],
                    )
                ],
            ),
        ],
    )

def add_layout():
    # Actual layout of the app
    return html.Div(
        className="row",
        style={"max-width": "100%", "font-size": "1.5rem", "padding": "0px 0px"},
        children=[
            # header
            Header(),
            # description
            description(),
            # Body
            Body()
        ],
    )

