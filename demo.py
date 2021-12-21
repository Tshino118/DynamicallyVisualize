import base64
from genericpath import isfile
import io
import pathlib
import os

import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
""" import dash
from PIL import Image
from io import BytesIO
from dash.exceptions import PreventUpdate
 """
from dataRead import readData
input_data,input_features,feature_unique,figure_dict,feature_dict,id_io,week_io,eye_state_io,kMeans_dict=readData()

# get relative data folder
PATH = pathlib.Path(__file__).parent

path_isfile=os.path.isfile
path_isdir=os.path.isdir



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
                        options=[{'label':'All','value':'All'}],
                        value=[],
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
                                        value=[],
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
    @app.callback(
        [
            Output("checklist-id_user-all", "value"),
            Output("checklist-id_user", "value")
        ],
        [
            Input("checklist-id_user-all", "value"),
            Input("checklist-id_user", "value"),
            State("checklist-id_user", "options")
        ]
    )
    def sync_checklists_id(all_selected,selected,options):
        values=[option["value"] for option in options]
        ctx = dash.callback_context
        input_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if input_id == "checklist-id_user-all":
            through=all_selected
            if (all_selected == ["All"]):
                selected = values
            else:
                selected = []
            return [through, selected]

        elif input_id == "checklist-id_user":
            through=selected
            if (set(selected) == set(values)):
                all_selected = ["All"]
            else:
                all_selected = []

            return [all_selected, through]
        else:
            pass
    
    @app.callback(
        [
            Output("checklist-week-all", "value"),
            Output("checklist-week", "value")
        ],
        [
            Input("checklist-week-all", "value"),
            Input("checklist-week", "value"),
            State("checklist-week", "options")
        ]
    )
    def sync_checklists_week(all_selected,selected,options):
        values=[option["value"] for option in options]
        ctx = dash.callback_context
        input_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if input_id == "checklist-week-all":
            through=all_selected
            if (all_selected == ["All"]):
                selected = values
            else:
                selected = []
            return [through, selected]

        elif input_id == "checklist-week":
            through=selected
            if (set(selected) == set(values)):
                all_selected = ["All"]
            else:
                all_selected = []

            return [all_selected, through]
        else:
            pass
  
    @app.callback(
        [
            Output("checklist-eye_state-all", "value"),
            Output("checklist-eye_state", "value")
        ],
        [
            Input("checklist-eye_state-all", "value"),
            Input("checklist-eye_state", "value"),
            State("checklist-eye_state", "options")
        ]
    )
    def sync_checklists_eye_state(all_selected,selected,options):
        values=[option["value"] for option in options]
        ctx = dash.callback_context
        input_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if input_id == "checklist-eye_state-all":
            through=all_selected
            if (all_selected == ["All"]):
                selected = values
            else:
                selected = []
            return [through, selected]

        elif input_id == "checklist-eye_state":
            through=selected
            if (set(selected) == set(values)):
                all_selected = ["All"]
            else:
                all_selected = []

            return [all_selected, through]
        else:
            pass
