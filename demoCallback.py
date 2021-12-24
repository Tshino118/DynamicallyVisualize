import dash
from dash.dependencies import Input, Output, State

import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pathlib
PATH = pathlib.Path(__file__).parent

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
            return [
                f"data set:{dataset}\
                user:{id_user}\
                weekdays:{week}\
                eye state:{eye_state}\
                Number of clusters:{numberOfClusters}"
            ]
            

    #add graph-3d-plot callbacks
    def graph_callbacks():
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
                State("figure-store", "data"),
                State("IO-store", "data"),
                State("kMeans-store","data")
            ]
        )
        def graph3d(n_clicks,dataset,id_user,week,eye_state,numberOfClusters,figure_dict,io_dict,kMeans_dict):
            id_user_io=[]
            week_io=[]
            eye_state_io=[]
            for val in id_user:
                id_user_io+=io_dict["id"][val]
            for val in week:
                week_io+=io_dict["week"][val]
            for val in eye_state:
                eye_state_io+=io_dict["eye_state"][val]
            io_data=id_user_io+week_io+eye_state_io
            id_data=np.array(io_data,dtype="bool")
            kMeans_dict[dataset]["predict"]["data"]["xy"][numberOfClusters]
            timeXY=figure_dict[dataset]["timeXY"]
            figure=[]

            return figure
            

    #add clicked on graph-3d-plot callbacks
    def plotClick_callbacks():
        @app.callback(
            [
                Output(f"div-plot-click-message", "value"),
                Output(f"div-plot-click-image", "children")
            ],
            [
                Input("graph-3d-plot", "clickData")
            ]
        )
        def sync_checklists(clickData):
            return [clickData,clickData]
    
    checklist_short=["id_user", "week", "eye_state"]
    [checklists_sync_callbacks(short) for short in checklist_short]

    select_data_callback()
    learnMore_callbacks()
    '''

    graph_callbacks()

    plotClick_callbacks()
    '''