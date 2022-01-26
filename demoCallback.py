from copy import deepcopy
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
    
    def select_k_callbacks():
        @app.callback(
            [
                Output('select-k', 'children')
            ],
            [
                Input("slider-setting-numberOfClusters", "value")
            ]
        )
        def select_kCallback(numberOfClusters):
            numberOfClusters_index=[k for k in range(numberOfClusters)]
            return [
                dcc.Checklist(
                    id=f"checklist-setting-cluster",
                    options=[{"label": k,"value": k} for k in numberOfClusters_index],
                    value=numberOfClusters_index,
                    labelStyle={'display': 'inline-block'}
                )
            ]
        
    def dataStore_callback():
        feature=input_features["feature"]
        @app.callback(
            [
                Output("data-store", "data"),
            ],
            [                
                Input("setting-submit", "n_clicks"),
                State("dropdown-setting-dataset", "value"),
                State("checklist-setting-id_user", "value"),
                State("checklist-setting-week", "value"),
                State("checklist-setting-eye_state", "value"),
                State("slider-setting-numberOfClusters", "value"),
                State("checklist-setting-cluster", "value"),
                State("dropdown-setting-clusteringData", "value"),
                State("dropdown-setting-graph_type", "value"),
                State("dropdown-graph-color", "value"),
                State("data-store", 'data'),
            ]
        )
        def dataStore(n_click,dataset,id_user,week,eye_state,numberOfClusters,cluster,clusteringData,graph_type,selectColor,data):
            data['dataset']=dataset
            data['id_user']=id_user
            data['week']=week
            data['eye_state']=eye_state
            data['numberOfClusters']=numberOfClusters
            data['cluster']=cluster
            data['clusteringData']=clusteringData
            data['graph_type']=graph_type
            data['selectColor']=selectColor
            cluster_df=kMeans_dict[dataset]["predict"]["data"][clusteringData]#.loc[:,f"{numberOfClusters}"]
            
            cluster_io=[]
            id_user_io=[]
            week_io=[]
            eye_state_io=[]
            for val in cluster:
                cluster_io.extend(cluster_df[cluster_df[str(numberOfClusters)]==val].index)
            for val in id_user:
                id_user_io.extend(feature[feature['id_user']==val].index)
            for val in week:
                week_io.extend(feature[feature['week']==val].index)
            for val in eye_state:
                eye_state_io.extend(feature[feature['eye_state']==val].index)
            select_data_index = list(set(cluster_io) & set(id_user_io) & set(week_io) & set(eye_state_io))
            data['select_data_index']=select_data_index
            
            numberOfClusters_index=list(range(numberOfClusters))
            data['numberOfClusters_index']=numberOfClusters_index
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
            data['colorDict']=colorDict
            
            cluster_dict=dict(zip(cluster,numberOfClusters_index))
            id_dict=dict(zip(id_user,id_user_index))
            week_dict=dict(zip(week,week_index))
            eye_dict=dict(zip(eye_state,eye_state_index))
            #colorLabelList=['cluster','id_user','week','eye_state']
            k_list=[0 for _ in select_data_index]
            i_list=[0 for _ in select_data_index]
            w_list=[0 for _ in select_data_index]
            e_list=[0 for _ in select_data_index]

            k_select_list=[cluster_dict[cluster_df.at[index,str(numberOfClusters)]] for index in select_data_index]#->int index list
            i_select_list=[id_dict[feature.at[index,'id_user']] for index in select_data_index]#->int index list
            w_select_list=[week_dict[feature.at[index,'week']] for index in select_data_index]#->int index list
            e_select_list=[eye_dict[feature.at[index,'eye_state']] for index in select_data_index]#->int index list
            
            if "cluster" in set(selectColor):
                k_list=k_select_list
            if "id_user" in set(selectColor):
                i_list=i_select_list
            if "week" in set(selectColor):
                w_list=w_select_list
            if "eye_state" in set(selectColor):
                e_list=e_select_list
            data['k_list']=k_list
            data['i_list']=i_list
            data['w_list']=w_list
            data['e_list']=e_list
            
            data['k_select_list']=k_select_list
            data['i_select_list']=i_select_list
            data['w_select_list']=w_select_list
            data['e_select_list']=e_select_list
            
            
            #colorSet=[
            #    colorDict[f"{k}_{i}_{w}_{e}"] 
            #    for k in set(k_list)
            #    for i in set(i_list)
            #    for w in set(w_list)
            #    for e in set(e_list)
            #]
            return [data]
            
    def color_button_callbacks():
        @app.callback(
            [
                Output(f"graph-color","children"),
                Output(f"info-selectGroupCount","children"),
            ],
            [
                Input("setting-submit", "n_clicks"),
                State("data-store", 'data'),
            ]
        )
        def color_buttonCallbacks(n_click,data):
            k_list=data['k_list']
            i_list=data['i_list']
            w_list=data['w_list']
            e_list=data['e_list']
            k_select_list=data["k_select_list"]
            i_select_list=data["i_select_list"]
            w_select_list=data["w_select_list"]
            e_select_list=data["e_select_list"]
            k_select_list_gcount=pd.Series(data=k_select_list).value_counts()
            i_select_list_gcount=pd.Series(data=i_select_list).value_counts()
            w_select_list_gcount=pd.Series(data=w_select_list).value_counts()
            e_select_list_gcount=pd.Series(data=e_select_list).value_counts()
            selectGroupCount=html.P(children=f"Sum  k:{k_select_list_gcount}, id:{i_select_list_gcount}, week:{w_select_list_gcount}, eye:{e_select_list_gcount}")
            colorDict=data['colorDict']
            id_user=data['id_user']
            week=data['week']
            eye_state=data['eye_state']
            
            def colorButtonSet(title,short,color):
                return html.Tr(
                    children=[
                        html.Td(f'{title}'),
                        html.Td(
                            html.Button(
                                id=f'color-button-{short}',
                                children=['change color'],
                                style={'background-color': color}
                            )
                        )
                    ]
                )
            colorbutton=[
                colorButtonSet(
                    title=f"cluster:{k}, id:{id_user[i]}, week:{week[w]}, eye:{eye_state[e]}  ",
                    short=f"{k}_{i}_{w}_{e}",
                    color=colorDict[f"{k}_{i}_{w}_{e}"]
                )
                for k in set(k_list)
                for i in set(i_list)
                for w in set(w_list)
                for e in set(e_list)
            ]
            return [colorbutton, selectGroupCount]

    #add graph-area callbacks
    def graph_callbacks():
        graphTypeLabel={
            'timeX':{
                "description":"right and left moving Line",
                "specs":{"type": "xy"}, 
                "title":{'x':'time series','y':'right-left'}
            },
            'timeY':{
                "description":"top and bottom moving Line",
                "specs":{"type": "xy"}, 
                "title":{'x':'time series','y':'bottom-top'}
            },
            'XY':{
                "description":"body moving Line",
                "specs":{"type": "xy"}, 
                "title":{'x':'left-right','y':'bottom-top'}
            },
            'timeXY':{
                "description":"body moving with time-series Line",
                "specs":{"type": "scene"}, 
                "title":{'x':'left-right','y':'top-bottom','z':'time series'}
            }
        }
        figSetting=pd.read_csv(PATH.joinpath(r"figure/figSetting.csv"),index_col=['dataType','fig','feature','dimension'])
        
        @app.callback(
            [   
                Output(f"graph-area", "children"),
                #Output(f"graph-area-cluster","children"),
            ],
            [   
                Input("setting-submit", "n_clicks"),
                State("data-store","data")
            ]
        )
        def graph3d(n_click,data):
            graph_type=data['graph_type']
            dataset=data['dataset']
            select_data_index=data['select_data_index']
            print('aaaaaa',select_data_index)
            k_list=data['k_list']
            i_list=data['i_list']
            w_list=data['w_list']
            e_list=data['e_list']
            k_select_list=data['k_select_list']
            colorDict=data['colorDict']

            graphType_num=len(graph_type)
            rows=math.ceil(math.sqrt(graphType_num))
            cols=math.ceil(graphType_num/int(rows))
            
            layoutset={
                'timeX':figureLayout.fig_timeX(dataType=dataset),
                'timeY':figureLayout.fig_timeY(dataType=dataset),
                'XY':figureLayout.fig_XY(dataType=dataset),
                'timeXY':figureLayout.fig_timeXY(dataType=dataset)
            }
            def figureCluster(figure_, k_select_list_, numberOfClusters_, numberOfClusters_index_):
                fig=copy(figure_)
                cluster_fig=[]
                for k in numberOfClusters_index_:
                    for figureData,select_k in zip(fig.data, k_select_list_):#loop figuredata
                        if k==select_k:
                            figureData.visible=True
                        else:
                            figureData.visible=False
                    cluster_fig+=[dcc.Graph(figure=fig,id=f"graph-element-cluster{numberOfClusters_}-{k}")]
                return cluster_fig

            cnt=0
            tb=[]
            dataTypeCluster=[]
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
                            'legend':dict(
                                x=0,
                                y=1,
                            )
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
                            
                        tr+=[html.Td(children=dcc.Graph(figure=figure,id=f"graph-element-{graphType}"))]
                        #figure_=deepcopy(figure)
                        #dataTypeCluster+=[html.Div(children=[figureCluster(figure_=figure_,k_select_list_=k_select_list,numberOfClusters_=numberOfClusters,numberOfClusters_index_=numberOfClusters_index)])]
                        cnt+=1
                    else:
                        tr+=[html.Td(id=f"graph-element-{row}{col}", style={"height": "98vh"})]
                tb+=[html.Tr(children=tr)]
            figure_table=html.Table(children=html.Tbody(children=tb))
            return [
                figure_table,
            ]
            
    def clusterChange_callbacks():
        for gt in ['timeXY']:
            @app.callback(
                    Output(f"graph-element-{gt}", "figure"),
                [
                    Input("setting-clusterChange-submit", "n_clicks"),
                    State(f"graph-element-{gt}", "figure"),
                    State("data-store", 'data'),
                    State("select-k","children"),
                ]
            )
            def clusterChangeCallback(n_click,fig,data,k):
                ctx = dash.callback_context
                input_id = ctx.triggered[0]["prop_id"].split(".")[0]
                if input_id == "setting-clusterChange-submit":
                    k_list=data['k_list']
                    for i,k_select in enumerate(k_list):
                        if(k==k_select):
                            fig['data'][i]['visible'] = True
                        else:
                            fig['data'][i]['visible'] = False
                            
                figure=go.Figure(data=fig['data'],layout=fig['layout'])
                return figure

    def clusterMatrix_callbacks():
        def figureCluster(figure_, k_select_list_, numberOfClusters_, numberOfClusters_index_):
            cluster_fig=[]
            for k in numberOfClusters_index_:
                for figureData,select_k in zip(figure_.data, k_select_list_):#loop figuredata
                    if k==select_k:
                        figureData.visible=True
                    else:
                        figureData.visible=False
                cluster_fig+=[dcc.Graph(figure=figure_,id=f"graph-element-cluster{numberOfClusters_}-{k}")]
            return cluster_fig
        #dataTypeCluster+=[html.Div(children=[figureCluster(figure_=figure,k_select_list_=k_select_list,numberOfClusters_=numberOfClusters,numberOfClusters_index_=numberOfClusters_index)])]
        @app.callback(
            [
                Output(f"graph-area","children"),
            ],
            [
                State("data-store", 'data'),
                State(f"graph-area","children"),
            ]
        )
        def cluster_matrix(data):
            colorDict=data['colorDict']
            dataset=data['dataset']
            graph_type=data['graph_type']
            select_data_index=data['select_data_index']
            k_list=data['k_list']
            i_list=data['i_list']
            e_list=data['e_list']
            w_list=data['w_list']
            layoutset={
                'timeX':figureLayout.fig_timeX(dataType=dataset),
                'timeY':figureLayout.fig_timeY(dataType=dataset),
                'XY':figureLayout.fig_XY(dataType=dataset),
                'timeXY':figureLayout.fig_timeXY(dataType=dataset)
            }
            graphTypeLabel={
                'timeX':{
                    "description":"right and left moving Line",
                    "specs":{"type": "xy"}, 
                    "title":{'x':'time series','y':'right-left'}
                },
                'timeY':{
                    "description":"top and bottom moving Line",
                    "specs":{"type": "xy"}, 
                    "title":{'x':'time series','y':'bottom-top'}
                },
                'XY':{
                    "description":"body moving Line",
                    "specs":{"type": "xy"}, 
                    "title":{'x':'left-right','y':'bottom-top'}
                },
                'timeXY':{
                    "description":"body moving with time-series Line",
                    "specs":{"type": "scene"}, 
                    "title":{'x':'left-right','y':'top-bottom','z':'time series'}
                }
            }
            figSetting=pd.read_csv(PATH.joinpath(r"figure/figSetting.csv"),index_col=['dataType','fig','feature','dimension'])
            graphType_num=len(graph_type)
            rows=math.ceil(math.sqrt(graphType_num))
            cols=math.ceil(graphType_num/int(rows))
            cnt=0
            tb=[]
            dataTypeCluster=[]
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
                            "showlegend":True,
                            'legend':dict(
                                x=0,
                                y=1,
                            )
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
            
            c_m_thead=html.Thead()
            c_m_tbody=html.Tbody()
            c_m_table=html.Table(id='cluster-matrix',children=[c_m_thead,c_m_tbody])
            return c_m_table

    #add clicked on graph-area callbacks
    def plotClick_callbacks():
        @app.callback(
            [
                Output(f"div-plot-click-message", "children"),
            ],
            [
            ]
        )
        def plot_click_callbacks(clickData):
            return [f'{clickData}']

    checklist_short=["id_user", "week", "eye_state"]
    [checklists_sync_callbacks(short) for short in checklist_short]

    learnMore_callbacks()
    graph_callbacks()
    dataStore_callback()
    color_button_callbacks()
    select_k_callbacks()
    '''
    clusterChange_callbacks()
    plotClick_callbacks()
    select_data_callback()
    '''