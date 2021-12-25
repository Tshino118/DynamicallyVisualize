import dash
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import dataRead
import pathlib
PATH = pathlib.Path(__file__).parent

dataClass=dataRead.dataSets
input_data=dataClass.Input_data()
input_features=dataClass.Input_features()
kMeans_dict=dataClass.KMeans_dict()
input_indexes=dataClass.Input_indexes(input_data)
figure_dict=dataClass.Figure_dict(input_data)
feature_unique=dataClass.Feature_unique(input_features)
feature_dict=dataClass.Feature_dict(feature_unique)
io_dict=dataClass.IO_dict(feature_unique,input_features)

with open(PATH.joinpath("asset/demo_intro.md"), "r") as file:
    demo_intro_md = file.read()

with open(PATH.joinpath("asset/demo_description.md"), "r") as file:
    demo_description_md = file.read()

def add_callbacks(app):
    # Callback function for the learn-more button
    def learnMore_callbacks():
        @app.callback(
            [
                Output("description-text", "children"),
                Output("learn-more-button", "children"),
            ],
            [Input("learn-more-button", "n_clicks")],
        )
        def learn_more(n_clicks):
            # If clicked odd times, the instructions will show; else (even times), only the header will show
            if n_clicks is None:
                n_clicks = 0
            if (n_clicks % 2) == 1:
                n_clicks += 1
                return (
                    html.Div(
                        style={"padding-right": "15%"},
                        children=[dcc.Markdown(demo_description_md)],
                    ),
                    "Close",
                )
            else:
                n_clicks += 1
                return (
                    html.Div(
                        style={"padding-right": "15%"},
                        children=[dcc.Markdown(demo_intro_md)],
                    ),
                    "Learn More",
                )

    #add checklist callbacks
    def checklists_sync_callbacks(short):
        @app.callback(
            [
                Output(f"checklist-{short}-all", "value"),
                Output(f"checklist-{short}", "value")
            ],
            [
                Input(f"checklist-{short}-all", "value"),
                Input(f"checklist-{short}", "value"),
                State(f"checklist-{short}", "options")
            ]
        )
        def sync_checklists(all_selected,selected,options):
            values=[option["value"] for option in options]
            ctx = dash.callback_context
            input_id = ctx.triggered[0]["prop_id"].split(".")[0]
            if input_id == f"checklist-{short}-all":
                through=all_selected
                if (all_selected == ["All"]):
                    selected = values
                else:
                    selected = []
                return [through, selected]
            elif input_id == f"checklist-{short}":
                through=selected
                if (set(selected) == set(values)):
                    all_selected = ["All"]
                else:
                    all_selected = []
                return [all_selected, through]
            else:
                pass

    def select_data_callback():
        @app.callback(
            [
                Output(f"select-data", "children")
            ],
            [
                Input("submit-val","n_clicks"),
                State("dropdown-dataset", "value"),
                State("checklist-id_user", "value"),
                State("checklist-week", "value"),
                State("checklist-eye_state", "value"),
                State("slider-numberOfClusters", "value")
            ]
        )
        def selectData(n_clicks,dataset,id_user,week,eye_state,numberOfClusters):
            target_fig=figure_dict#{'index':Fig_xyz(),'index2':Fig_xyz(),...}
            return [
                f"data set:{dataset} type{type(dataset)}\
                user:{id_user} type{type(id_user)}\
                weekdays:{week} type{type(week)}\
                eye state:{eye_state} type{type(eye_state)}\
                Number of clusters:{numberOfClusters} type{type(numberOfClusters)}"
            ]
            

    #add graph-3d-plot callbacks
    def graph_callbacks():
        @app.callback(
            [
                Output(f"graph-3d-plot", "figure"),
                Output("select-graph", "children")
            ],
            [
                Input("submit-val","n_clicks"),
                State("dropdown-dataset", "value"),
                State("checklist-id_user", "value"),
                State("checklist-week", "value"),
                State("checklist-eye_state", "value"),
                State("slider-numberOfClusters", "value"),
            ]
        )
        def graph3d(n_clicks,dataset,id_user,week,eye_state,numberOfClusters):
            id_user_io=pd.Series()
            week_io=pd.Series()
            eye_state_io=pd.Series()
            for val in id_user:
                id_user_io+=pd.Series(io_dict["id"][val])
            for val in week:
                week_io+=pd.Series(io_dict["week"][val])
            for val in eye_state:
                eye_state_io+=pd.Series(io_dict["eye_state"][val])
            io_data=id_user_io+week_io+eye_state_io
            io_data=io_data.astype('bool')
            io_index=[index for index,io in zip(input_indexes,io_data) if io==True ]

            #clusterNumber=kMeans_dict[dataset]["predict"]["data"]["xy"].loc[numberOfClusters]
            target_fig=figure_dict[dataset]["timeXY"]#{'index':Fig_xyz(),'index2':Fig_xyz(),...}
            timeXY=[target_fig[index] for index in io_index]
            figure=go.Figure(data=timeXY)
            return [figure,f"dataset:{dataset} io_index:{io_index}\ntimeXY:{timeXY}"]

    #add clicked on graph-3d-plot callbacks
    def plotClick_callbacks():
        @app.callback(
            [
                Output(f"div-plot-click-message", "value"),
            ],
            [
                Input("graph-3d-plot", "clickData")
            ]
        )
        def sync_checklists(clickData):
            return [clickData,clickData]
    
    checklist_short=["id_user", "week", "eye_state"]
    [checklists_sync_callbacks(short) for short in checklist_short]

    learnMore_callbacks()
    graph_callbacks()
    select_data_callback()
    '''
    plotClick_callbacks()
    '''