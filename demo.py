import base64
from genericpath import isfile
import io
import pathlib
import os

import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
from PIL import Image
from io import BytesIO
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from numpy.lib.arraysetops import unique

import pandas as pd
import plotly.graph_objs as go
import scipy.spatial.distance as spatial_distance

import layoutplt

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("asset/data").resolve()
KMEANS_PATH = PATH.joinpath("asset/data/kMeans").resolve()

path_isfile=os.path.isfile
path_isdir=os.path.isdir

input_data={
    'lerp':{
        'label':'linear interporation',
        'descriotion':'Linear interpolation of missing data for each data.',
        'data' :pd.read_csv(DATA_PATH.joinpath("lerp.csv")),
    },
    "meanZero": {
        'label':'mean zero',
        'description':'The average value of each data is zero.',
        'data' :pd.read_csv(DATA_PATH.joinpath("meanZero.csv")),
    },
    "medianZero": {
        'label':'median zero',
        'description':'The median of each data set is zero.',
        'data' :pd.read_csv(DATA_PATH.joinpath("medianZero.csv")),
    },
    "firstPointZero": {
        'label':'first point value is zero',
        'description':'The first value of each data set is zero.',
        'data' :pd.read_csv(DATA_PATH.joinpath("firstPointZero.csv")),
    },
    'feature':pd.read_csv(DATA_PATH.joinpath("features.csv")),
    'statistics':pd.read_csv(DATA_PATH.joinpath("statistics.csv"))
}

kMeans_dict={
    "lerp": {
        'inertia':{
            'label':'cluster inertia',
            'data': {
                'x':pd.read_csv(KMEANS_PATH.joinpath("lerp/inertia/X.csv")),
                'y':pd.read_csv(KMEANS_PATH.joinpath("lerp/inertia/Y.csv")),
                'xy':pd.read_csv(KMEANS_PATH.joinpath("lerp/inertia/XY.csv"))
            },
        },
        'predict':{
            'label':'predict cluster number',
            'data': {
                'x':pd.read_csv(KMEANS_PATH.joinpath("lerp/predict/X.csv")),
                'y':pd.read_csv(KMEANS_PATH.joinpath("lerp/predict/Y.csv")),
                'xy':pd.read_csv(KMEANS_PATH.joinpath("lerp/predict/XY.csv"))
            }
        }
    },
    "meanZero": {
        'inertia':{
            'label':'cluster inertia',
            'data': {
                'x':pd.read_csv(KMEANS_PATH.joinpath("meanZero/inertia/X.csv")),
                'y':pd.read_csv(KMEANS_PATH.joinpath("meanZero/inertia/Y.csv")),
                'xy':pd.read_csv(KMEANS_PATH.joinpath("meanZero/inertia/XY.csv"))
            },
        },
        'predict':{
            'label':'predict cluster number',
            'data': {
                'x':pd.read_csv(KMEANS_PATH.joinpath("meanZero/predict/X.csv")),
                'y':pd.read_csv(KMEANS_PATH.joinpath("meanZero/predict/Y.csv")),
                'xy':pd.read_csv(KMEANS_PATH.joinpath("meanZero/predict/XY.csv"))
            }
        }
    },
    "medianZero": {
        'inertia':{
            'label':'cluster inertia',
            'data': {
                'x':pd.read_csv(KMEANS_PATH.joinpath("medianZero/inertia/X.csv")),
                'y':pd.read_csv(KMEANS_PATH.joinpath("medianZero/inertia/Y.csv")),
                'xy':pd.read_csv(KMEANS_PATH.joinpath("medianZero/inertia/XY.csv"))
            },
        },
        'predict':{
            'label':'predict cluster number',
            'data': {
                'x':pd.read_csv(KMEANS_PATH.joinpath("medianZero/predict/X.csv")),
                'y':pd.read_csv(KMEANS_PATH.joinpath("medianZero/predict/Y.csv")),
                'xy':pd.read_csv(KMEANS_PATH.joinpath("medianZero/predict/XY.csv"))
            }
        }
    },
    "firstPointZero": {
        'inertia':{
            'label':'cluster inertia',
            'data': {
                'x':pd.read_csv(KMEANS_PATH.joinpath("firstPointZero/inertia/X.csv")),
                'y':pd.read_csv(KMEANS_PATH.joinpath("firstPointZero/inertia/Y.csv")),
                'xy':pd.read_csv(KMEANS_PATH.joinpath("firstPointZero/inertia/XY.csv"))
            },
        },
        'predict':{
            'label':'predict cluster number',
            'data': {
                'x':pd.read_csv(KMEANS_PATH.joinpath("firstPointZero/predict/X.csv")),
                'y':pd.read_csv(KMEANS_PATH.joinpath("firstPointZero/predict/Y.csv")),
                'xy':pd.read_csv(KMEANS_PATH.joinpath("firstPointZero/predict/XY.csv"))
            }
        }
    }
}
feature_unique={
    "id":input_data["feature"]['id_user'].unique(),
    "week":input_data["feature"]['week'].unique(),
    "eye_state":input_data["feature"]['eye_state'].unique(),
}
#feature setting
feature_dict={
    "id":{
        'label':'select ids',
        'options':[{
            'label': key,
            'value': key
        } for key in feature_unique['id']],
    },
    "week":{
        'label':'select weekdays',
        'options':[{
            'label': key,
            'value': key
        } for key in feature_unique['week']],
    },
    "eye_state":{
        'label':'select eye_states',
        'options':[{
            'label': key,
            'value': key
        } for key in feature_unique['eye_state']],
    }
}

id_io={f'{key}':val.values for key,val in zip(feature_unique['id'],[input_data["feature"]['id_user']==key for key in feature_unique['id'] ])}
week_io={f'{key}':val.values for key,val in zip(feature_unique['week'],[input_data["feature"]['week']==key for key in feature_unique['week'] ])}
eye_state_io={f'{key}':val.values for key,val in zip(feature_unique['eye_state'],[input_data["feature"]['eye_state']==key for key in feature_unique['eye_state'] ])}

with open(PATH.joinpath("asset/demo_intro.md"), "r") as file:
    demo_intro_md = file.read()

with open(PATH.joinpath("asset/demo_description.md"), "r") as file:
    demo_description_md = file.read()
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

def NamedChecklist(name, short, options, vals):
    return html.Div(
        style={"margin": "25px 5px 30px 0px"},
        children=[
            f"{name}:",
            html.Div(
                style={"margin-left": "5px"},
                children=[
                    dcc.Checklist(
                        id=f"checklist-{short}-all",
                        options=[{'label':'all','value':'all'}],
                        value=['all'],
                        labelStyle={'display': 'inline-block'}
                    ),
                    dcc.Checklist(
                        id=f"checklist-{short}",
                        options=options,
                        value=vals,
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

def Header(app):
    # Header
    return html.Div(
                className="row header",
                id="app-header",
                style={"background-color": "#f9f9f9"},
                children=[
                    html.Div(
                        [
                            html.Img(
                                src=app.get_asset_url("dash-logo.png"),
                                className="logo",
                                id="plotly-image",
                            )
                        ],
                        className="three columns header_img",
                    ),
                    html.Div(
                        [
                            html.H3(
                                "t-SNE Explorer",
                                className="header_title",
                                id="app-title",
                            )
                        ],
                        className="nine columns header_title_container",
                    ),
                ],
            )

def description(intro_md):
    #  Demo Description
    return html.Div(
            className="row background",
            id="demo-explanation",
            style={"padding": "50px 45px"},
            children=[
                html.Div(
                    id="description-text", children=dcc.Markdown(intro_md)
                ),
                html.Div(
                    html.Button(id="learn-more-button", children=["Learn More"])
                ),
            ],
        )

def add_layout(app):
    # Actual layout of the app
    return html.Div(
        className="row",
        style={"max-width": "100%", "font-size": "1.5rem", "padding": "0px 0px"},
        children=[
            Header(app),
            description(intro_md=demo_intro_md),
            # Body
            html.Div(
                className="row background",
                style={"padding": "10px"},
                children=[
                    html.Div(
                        className="three columns",
                        children=[
                            Card(
                                [
                                    dcc.Dropdown(
                                        id="dropdown-dataset",
                                        searchable=False,
                                        clearable=False,
                                        options=[
                                            {
                                                "label": key,
                                                "value": key
                                            }
                                            for key in input_data.keys()
                                        ],
                                        placeholder="Select a dataset",
                                        value='lerp',
                                    ),
                                    NamedSlider(
                                        name="Number of Clusters",
                                        short="numberOfClusters",
                                        min=2,
                                        max=10,
                                        step=None,
                                        val=2,
                                        marks={
                                            i: str(i) for i in range(2,10)
                                        },
                                    ),
                                    NamedChecklist(
                                        name="id_user",
                                        short='id_user',
                                        options=feature_dict["id"]['options'],
                                        vals=feature_unique['id']
                                    ),
                                    NamedChecklist(
                                        name="week",
                                        short='week',
                                        options=feature_dict["week"]['options'],
                                        vals=feature_unique['week']
                                    ),
                                    NamedChecklist(
                                        name="eye_state",
                                        short='eye_state',
                                        options=feature_dict["eye_state"]['options'],
                                        vals=feature_unique['eye_state']
                                    ),
                                ]
                            )
                        ],
                    ),
                    html.Div(
                        className="six columns",
                        children=[
                            dcc.Graph(id="graph-3d-plot", style={"height": "98vh"})
                        ],
                    ),
                    html.Div(
                        className="three columns",
                        id="euclidean-distance",
                        children=[
                            Card(
                                style={"padding": "5px"},
                                children=[
                                    html.Div(
                                        id="div-plot-click-message",
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
            ),
        ],
    )


def add_callbacks(app):
    return app