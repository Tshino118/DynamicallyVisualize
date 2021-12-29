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
import json
import random
from figure import figureLayout

def randomColor():
    color = [random.choice('0123456789ABCDEF') for _ in range(6)]
    return f'#{"".join(color)}'

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
                Output(f"checklist-setting-{short}-all", "value"),
                Output(f"checklist-setting-{short}", "value")
            ],
            [
                Input(f"checklist-setting-{short}-all", "value"),
                Input(f"checklist-setting-{short}", "value"),
                State(f"checklist-setting-{short}", "options")
            ]
        )
        def sync_checklists(all_selected,selected,options):
            values=[option["value"] for option in options]
            ctx = dash.callback_context
            input_id = ctx.triggered[0]["prop_id"].split(".")[0]
            if input_id == f"checklist-setting-{short}-all":
                through=all_selected
                if (all_selected == ["All"]):
                    selected = values
                else:
                    selected = []
                return [through, selected]
            elif input_id == f"checklist-setting-{short}":
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
                State("dropdown-setting-dataset", "value"),
                State("checklist-setting-id_user", "value"),
                State("checklist-setting-week", "value"),
                State("checklist-setting-eye_state", "value"),
                State("slider-setting-numberOfClusters", "value")
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
            
    #add graph-area callbacks
    def graph_callbacks():
        graphTypeLabel={
            'timeX':{"description":"right and left moving Line","specs":{"type": "xy"}, "title":{'x':'time series','y':'left-right'}},
            'timeY':{"description":"top and bottom moving Line","specs":{"type": "xy"}, "title":{'x':'time series','y':'top-bottom'}},
            'XY':{"description":"body moving Line","specs":{"type": "xy"}, "title":{'x':'left-right','y':'top-bottom'}},
            'timeXY':{"description":"body moving with time-series Line","specs":{"type": "scene"}, "title":{'x':'left-right','y':'top-bottom','z':'time series'}}
        }
        feature=input_features["feature"].set_index('id_index')
        figSetting=pd.read_csv(PATH.joinpath(r"figure/figSetting.csv"),index_col=['dataType','fig','feature','dimension'])
        
        @app.callback(
            [
                Output(f"graph-area", "children"),
            ],
            [
                Input("setting-submit", "n_clicks"),
                State("dropdown-setting-dataset", "value"),
                State("checklist-setting-id_user", "value"),
                State("checklist-setting-week", "value"),
                State("checklist-setting-eye_state", "value"),
                State("slider-setting-numberOfClusters", "value"),
                State("dropdown-setting-clusteringData", "value"),
                State("dropdown-setting-graph_type", "value"),
                State("dropdown-graph-color", "value")
            ]
        )
        def graph3d(n_clicks, dataset, id_user, week, eye_state, numberOfClusters, clusteringData, graph_type,selectColor):
            id_user_io=[]
            week_io=[]
            eye_state_io=[]
            for val in id_user:
                id_user_io.extend(feature[feature['id_user']==val].index)
            for val in week:
                week_io.extend(feature[feature['week']==val].index)
            for val in eye_state:
                eye_state_io.extend(feature[feature['eye_state']==val].index)
            select_data_index = list(set(id_user_io) & set(week_io) & set(eye_state_io))
            
            colorDict={
                f"{k}_{i}_{w}_{e}":randomColor()
                for k in range(numberOfClusters)
                for i in range(len(id_user))
                for w in range(len(week))
                for e in range(len(eye_state))
            }
            
            id_dict=dict(zip(id_user,list(range(len(id_user)))))
            week_dict=dict(zip(week,list(range(len(week)))))
            eye_dict=dict(zip(eye_state,list(range(len(eye_state)))))
            cluster_dict=kMeans_dict[dataset]["predict"]["data"][clusteringData].loc[:,f"{numberOfClusters}"]
            #colorLabelList=['cluster','id_user','week','eye_state']
            k_list=[0 for _ in select_data_index]
            i_list=[0 for _ in select_data_index]
            w_list=[0 for _ in select_data_index]
            e_list=[0 for _ in select_data_index]
            if "cluster" in selectColor:
                k_list=[cluster_dict[index] for index in select_data_index]
            elif "id_user" in selectColor:
                i_list=[id_dict[feature.at[index,'id_user']] for index in select_data_index]
            elif "week" in selectColor:
                w_list=[week_dict[feature.at[index,'week']] for index in select_data_index]
            elif "eye_state" in selectColor:
                e_list=[eye_dict[feature.at[index,'eye_state']] for index in select_data_index]
            colorSet=[colorDict[f"{k}_{i}_{w}_{e}"] for k,i,w,e in zip(k_list, i_list, w_list, e_list)]

            graphType_num=len(graph_type)
            rows=math.ceil(math.sqrt(graphType_num))
            cols=math.ceil(graphType_num/int(rows))
            #specs=[]
            #cnt=0
            #for row in range(rows):
            #    rowList=[]
            #    for col in range(cols):
            #        if(cnt<graphType_num):
            #            rowList+=[graphTypeLabel[graph_type[cnt]]["specs"]]
            #        else:
            #            rowList+=[{}]
            #        cnt+=1
            #    specs+=[rowList]

            #figure = make_subplots(
            #    rows=rows, cols=cols,
            #    subplot_titles=[graphTypeLabel[type]["description"] for type in graph_type],
            #    specs=specs
            #)
            layoutset={
                'timeX':figureLayout.fig_timeX(dataType=dataset),
                'timeY':figureLayout.fig_timeY(dataType=dataset),
                'XY':figureLayout.fig_XY(dataType=dataset),
                'timeXY':figureLayout.fig_timeXY(dataType=dataset)
            }
            cnt=0
            tb=[]
            for row in range(rows):
                tr=[]
                for col in range(cols):
                    if (cnt<graphType_num):
                        figure=go.Figure()
                        graphType=graph_type[cnt]
                        target_fig=figure_dict[dataset][graphType]#{'index':Fig_xyz(),'index2':Fig_xyz(),...}
                        [figure.add_trace(trace=target_fig[index]) for index in select_data_index]
                        figure.update_layout(dict1=layoutset[graphType])
                        figure.update_layout(dict1={
                            "showlegend":False,
                        })
                        figure.update_xaxes(
                            title_text=graphTypeLabel[graphType]['title']['x'],
                            range=figSetting.loc[dataset,graphType,'range','x']
                        )
                        figure.update_yaxes(
                            title_text=graphTypeLabel[graphType]['title']['y'],
                            range=figSetting.loc[dataset,graphType,'range','y']
                        )
                        for n,color in enumerate(colorSet):
                            figure.data[int(n)]['line']['color']=color
                        tr+=[html.Td(children=dcc.Graph(figure=figure,id=f"graph-element-{row}{col}", style={"height": "98vh"}))]
                        cnt+=1
                    else:
                        tr+=[html.Td(id=f"graph-element-{row}{col}", style={"height": "98vh"})]
                tb+=[html.Tr(children=tr)]
            figure_table=html.Table(children=html.Tbody(children=tb))
            return [figure_table]

    #add clicked on graph-area callbacks
    def plotClick_callbacks():
        @app.callback(
            [
                Output(f"div-plot-click-message", "children"),
            ],
            [
                Input("graph-area", "clickData")
            ]
        )
        def plot_click_callbacks(clickData):
            return [f'{clickData}']

    checklist_short=["id_user", "week", "eye_state"]
    [checklists_sync_callbacks(short) for short in checklist_short]

    learnMore_callbacks()
    graph_callbacks()
    plotClick_callbacks()
    '''
    select_data_callback()
    '''