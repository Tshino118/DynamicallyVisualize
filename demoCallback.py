import dash
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import dataRead
import pathlib
import math
PATH = pathlib.Path(__file__).parent

dataClass=dataRead.dataSets
input_data=dataClass.Input_data()
input_features=dataClass.Input_features()
kMeans_dict=dataClass.KMeans_dict()
input_indexes=dataClass.Input_indexes(input_data)
figure_dict=dataClass.Figure_dict(input_data)
feature_unique=dataClass.Feature_unique(input_features)
feature_dict=dataClass.Feature_dict(feature_unique)


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
        graphTypeLabel={
            'timeX':{"description":"right and left moving Line","specs":{"type": "xy"}}, 
            'timeY':{"description":"top and bottom moving Line","specs":{"type": "xy"}},
            'XY':{"description":"body moving Line","specs":{"type": "xy"}},
            'timeXY':{"description":"body moving with time-series Line","specs":{"type": "scene"}}
        }
        @app.callback(
            [
                Output(f"graph-3d-plot", "figure"),
            ],
            [
                Input("submit-val","n_clicks"),
                State("dropdown-dataset", "value"),
                State("checklist-id_user", "value"),
                State("checklist-week", "value"),
                State("checklist-eye_state", "value"),
                State("slider-numberOfClusters", "value"),
                State("dropdown-graph-type", "value")
            ]
        )
        def graph3d(n_clicks,dataset,id_user,week,eye_state,numberOfClusters,graph_type):
            id_user_io=[]
            week_io=[]
            eye_state_io=[]
            feature=input_features["feature"].set_index('id_index')
            for val in id_user:
                id_user_io.extend(feature[feature['id_user']==val].index)
            for val in week:
                week_io.extend(feature[feature['week']==val].index)
            for val in eye_state:
                eye_state_io.extend(feature[feature['eye_state']==val].index)
            select_data_index = list(set(id_user_io) & set(week_io) & set(eye_state_io))

            #clusterNumber=kMeans_dict[dataset]["predict"]["data"]["xy"].loc[numberOfClusters]
            num=len(graph_type)
            rows=math.ceil(math.sqrt(num))
            cols=math.ceil(num/int(rows))
            specs=[[] for _ in rows]
            cnt=0
            for row in range(rows):
                for col in range(cols):
                    if (cnt<num):
                        specs=graphTypeLabel[graph_type[cnt]]["specs"]
            figure = make_subplots(
                rows=rows,cols=cols,
                subplot_titles=[graphTypeLabel[type]["description"] for type in graph_type],
                specs=specs
            )
            cnt=0
            for row in range(rows):
                for col in range(cols):
                    if (cnt<num):
                        graphType=graph_type[cnt]
                        target_fig=figure_dict[dataset][graphType]#{'index':Fig_xyz(),'index2':Fig_xyz(),...}
                        [figure.append_trace(trace=target_fig[index],row=row+1, col=col+1) for index in select_data_index]
                        cnt+=1
            return [figure]

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