import pathlib
import pandas as pd
from figure import figure
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("asset/data").resolve()
KMEANS_PATH = PATH.joinpath("asset/data/kMeans").resolve()

class dataSets:
    def __init__(self) -> None:
        pass
    def Input_data():
        print('read dataset')
        return {
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
    
    def Input_features():
        print('read features')
        return {
            'feature':pd.read_csv(DATA_PATH.joinpath("features.csv")),
            'statistics':pd.read_csv(DATA_PATH.joinpath("statistics.csv"))
        }

    def Feature_unique(input_features):
        return {
            "id":input_features["feature"]['id_user'].unique(),
            "week":input_features["feature"]['week'].unique(),
            "eye_state":input_features["feature"]['eye_state'].unique(),
        }

    def Feature_dict(feature_unique):
        #feature setting
        return {
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

    def Figure_dict(input_data):
        print('make figure')
        '''example
        figure_dict={
            'lerp':{
                "timeX":{'index':Fig_xy(x=time,y=data_x,traceName=index),},
                "timeY":{'index':Fig_xy(x=time,y=data_y,traceName=index),},
                "XY":{'index':Fig_xy(x=data_x,y=data_y,traceName=index),},
                "timeXY":{'index':Fig_xyz(x=data_x,y=data_y,z=time,traceName=index),}
            },
        }
        '''
        return figure.make_figure(input_data)

    def KMeans_dict():
        print('read kMeans')
        return {
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

    def IO_dict(feature_unique,input_features):
        print('make IO')
        return {
            "id":{
                f'{key}':val.values for key,val in zip(feature_unique['id'],[input_features["feature"]['id_user']==key for key in feature_unique['id'] ])
            },
            "week":{
                f'{key}':val.values for key,val in zip(feature_unique['week'],[input_features["feature"]['week']==key for key in feature_unique['week'] ])
            },
            "eye_state":{
                f'{key}':val.values for key,val in zip(feature_unique['eye_state'],[input_features["feature"]['eye_state']==key for key in feature_unique['eye_state'] ])
            }
        }

def readData(
        input_data=False,input_features=False,feature_unique=False,figure_dict=False,feature_dict=False,
        io_dict=False,kMeans_dict=False
    ):
    class_dataSets=dataSets
    #input_data,input_features,feature_unique,figure_dict,feature_dict,io_dict,kMeans_dict
    if input_data==True:
        input_data=class_dataSets.Input_data()
        if figure_dict==True:
            figure_dict=class_dataSets.Figure_dict(input_data)
    if input_features==True:
        input_features=class_dataSets.Input_features()
        if feature_unique==True:
            feature_unique=class_dataSets.Feature_unique(input_features)
            if feature_dict==True:
                feature_dict=class_dataSets.Feature_dict(feature_unique)
            if io_dict==True:
                io_dict=class_dataSets.IO_dict(feature_unique,input_features)
    if kMeans_dict==True:
        kMeans_dict=class_dataSets.KMeans_dict()
    return {
        "input_data":input_data,
        "input_features":input_features,
        "feature_unique":feature_unique,
        "figure_dict":figure_dict,
        "feature_dict":feature_dict,
        "io_dict":io_dict,
        "kMeans_dict":kMeans_dict
    }

