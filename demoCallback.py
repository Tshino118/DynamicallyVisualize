import dash
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
#from plotly.subplots import make_subplots
import dash_core_components as dcc
import dash_html_components as html
#import dash_daq as daq
#import numpy as np
import pandas as pd
import pathlib
import math
import random
import json

import dataRead
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
        feature=input_features["feature"]
        figSetting=pd.read_csv(PATH.joinpath(r"figure/figSetting.csv"),index_col=['dataType','fig','feature','dimension'])
        
        @app.callback(
            [   
                Output(f"graph-area", "children"),
                Output(f"graph-color","children"),
                Output(f"color-store","data"),
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
            numberOfClusters_index=list(range(numberOfClusters))
            id_user_index=list(range(len(id_user)))
            week_index=list(range(len(week)))
            eye_state_index=list(range(len(eye_state)))
            colorDict={
                f"{k}_{i}_{w}_{e}":randomColor()
                for k in numberOfClusters_index
                for i in id_user_index
                for w in week_index
                for e in eye_state_index
            }
            
            cluster_dict=kMeans_dict[dataset]["predict"]["data"][clusteringData].loc[:,f"{numberOfClusters}"]
            id_dict=dict(zip(id_user,id_user_index))
            week_dict=dict(zip(week,week_index))
            eye_dict=dict(zip(eye_state,eye_state_index))
            #colorLabelList=['cluster','id_user','week','eye_state']
            k_list=[0 for _ in select_data_index]
            i_list=[0 for _ in select_data_index]
            w_list=[0 for _ in select_data_index]
            e_list=[0 for _ in select_data_index]
            if "cluster" in set(selectColor):
                k_list=[cluster_dict[index] for index in select_data_index]#->int index list
            if "id_user" in set(selectColor):
                i_list=[id_dict[feature.at[index,'id_user']] for index in select_data_index]#->int index list
            if "week" in set(selectColor):
                w_list=[week_dict[feature.at[index,'week']] for index in select_data_index]#->int index list
            if "eye_state" in set(selectColor):
                e_list=[eye_dict[feature.at[index,'eye_state']] for index in select_data_index]#->int index list
            
            #colorSet=[
            #    colorDict[f"{k}_{i}_{w}_{e}"] 
            #    for k in set(k_list)
            #    for i in set(i_list)
            #    for w in set(w_list)
            #    for e in set(e_list)
            #]
            

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
                        for figureData,k,i,w,e in zip(figure.data,k_list,i_list,w_list,e_list):
                            figureData['line']['color']=colorDict[f"{k}_{i}_{w}_{e}"]
                        tr+=[html.Td(children=dcc.Graph(figure=figure,id=f"graph-element-{row}{col}", style={"height": "98vh"}))]
                        cnt+=1
                    else:
                        tr+=[html.Td(id=f"graph-element-{row}{col}", style={"height": "98vh"})]
                tb+=[html.Tr(children=tr)]
            figure_table=html.Table(children=html.Tbody(children=tb))
            
            def colorButtonSet(title,short,color):
                return html.Tr(
                    children=[
                        html.Td(f'{title}'),
                        html.Td(
                            html.Button(
                                id=f'color-button-{short}',
                                children=[
                                    'change color',
                                ],
                                style={'background-color': color}
                            )
                        )
                    ]
                )
            color_button=[
                colorButtonSet(
                    title=f"cluster:{k}, id:{id_user[i]}, week:{week[w]}, eye:{eye_state[e]}",
                    short=f"{k}_{i}_{w}_{e}",
                    color=colorDict[f"{k}_{i}_{w}_{e}"]
                )
                for k in set(k_list)
                for i in set(i_list)
                for w in set(w_list)
                for e in set(e_list)
            ]

            #daq.ColorPicker(
            #    id=f'color-picker-button-{title}',
            #    label=f'{title}',
            #    value=dict(hex=f'{color}')
            #)
            color_store={'color_button':[colorDict.keys()]}
            return [figure_table,color_button,color_store]
    
    ##add color button
    #def colorButton_callbacks(app):
    #    colorButtons=State('color-store', "data")
    #    colorButtons
    #    @app.callback(
    #        [
    #            Output(f"div-plot-click-message", "children"),
    #        ],
    #        [
    #            Input()
    #            
    #        ]
    #    )
    #    def colorButtonCallbacks(clickData):
    #        return [f'{clickData}']
    

    #add clicked on graph-area callbacks
    def plotClick_callbacks(app):
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