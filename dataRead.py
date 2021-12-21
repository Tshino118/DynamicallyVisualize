import pathlib
import pandas as pd
import plotly.graph_objs as go

from figure import figure
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("asset/data").resolve()
KMEANS_PATH = PATH.joinpath("asset/data/kMeans").resolve()
def readData():
    DATA_PATH = PATH.joinpath("asset/data").resolve()
    print('read dataset')
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
    }
    print('read features')
    input_features={
        'feature':pd.read_csv(DATA_PATH.joinpath("features.csv")),
        'statistics':pd.read_csv(DATA_PATH.joinpath("statistics.csv"))
    }

    feature_unique={
        "id":input_features["feature"]['id_user'].unique(),
        "week":input_features["feature"]['week'].unique(),
        "eye_state":input_features["feature"]['eye_state'].unique(),
    }
    print('make figure')
    '''example
    figure_dict={
        'lerp':{
            "timeX":go.scatter(),
            "timeY":go.scatter(),
            "XY":go.scatter(),
            "timeXY":go.scatter3d()
        },
    }
    '''
    figure_dict=figure.make_figure(input_data)

    print('make IO')
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

    id_io={f'{key}':val.values for key,val in zip(feature_unique['id'],[input_features["feature"]['id_user']==key for key in feature_unique['id'] ])}
    week_io={f'{key}':val.values for key,val in zip(feature_unique['week'],[input_features["feature"]['week']==key for key in feature_unique['week'] ])}
    eye_state_io={f'{key}':val.values for key,val in zip(feature_unique['eye_state'],[input_features["feature"]['eye_state']==key for key in feature_unique['eye_state'] ])}

    print('read kMeans')
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
    return input_data,input_features,feature_unique,figure_dict,feature_dict,id_io,week_io,eye_state_io,kMeans_dict
