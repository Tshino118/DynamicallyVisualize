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
                'data' :pd.read_csv(DATA_PATH.joinpath("lerp.csv"),index_col=0),
            },
            "meanZero": {
                'label':'mean zero',
                'description':'The average value of each data is zero.',
                'data' :pd.read_csv(DATA_PATH.joinpath("meanZero.csv"),index_col=0),
            },
            "medianZero": {
                'label':'median zero',
                'description':'The median of each data set is zero.',
                'data' :pd.read_csv(DATA_PATH.joinpath("medianZero.csv"),index_col=0),
            },
            "firstPointZero": {
                'label':'first point value is zero',
                'description':'The first value of each data set is zero.',
                'data' :pd.read_csv(DATA_PATH.joinpath("firstPointZero.csv"),index_col=0),
            }
        }
    
    def Input_indexes(input_data):
        return input_data["lerp"]['data'].index

    def Input_features():
        print('read features')
        return {
            'feature':pd.read_csv(DATA_PATH.joinpath("features.csv"),index_col=0),
            'statistics':pd.read_csv(DATA_PATH.joinpath("statistics.csv"),index_col=0)
        }

    def Feature_unique(input_features):
        return {
            "id_user":input_features["feature"]['id_user'].unique(),
            "week":input_features["feature"]['week'].unique(),
            "eye_state":input_features["feature"]['eye_state'].unique(),
        }

    def Feature_dict(feature_unique):
        #feature setting
        return {
            "id_user":{
                'label':'select ids',
                'options':[{
                    'label': key,
                    'value': key
                } for key in feature_unique['id_user']],
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
                        'x':pd.read_csv(KMEANS_PATH.joinpath("lerp_clusterInertia.csv"),index_col=0,usecols=['x']),
                        'y':pd.read_csv(KMEANS_PATH.joinpath("lerp_clusterInertia.csv"),index_col=0,usecols=['y']),
                        'xy':pd.read_csv(KMEANS_PATH.joinpath("lerp_clusterInertia.csv"),index_col=0,usecols=['xy'])
                    },
                },
                'predict':{
                    'label':'predict cluster number',
                    'data': {
                        'x':pd.read_csv(KMEANS_PATH.joinpath("lerp_kMeansPredict_x.csv"),index_col=0),
                        'y':pd.read_csv(KMEANS_PATH.joinpath("lerp_kMeansPredict_y.csv"),index_col=0),
                        'xy':pd.read_csv(KMEANS_PATH.joinpath("lerp_kMeansPredict_xy.csv"),index_col=0)
                    }
                }
            },
            "meanZero": {
                'inertia':{
                    'label':'cluster inertia',
                    'data': {
                        'x':pd.read_csv(KMEANS_PATH.joinpath("meanZero_clusterInertia.csv"),index_col=0,usecols=['x']),
                        'y':pd.read_csv(KMEANS_PATH.joinpath("meanZero_clusterInertia.csv"),index_col=0,usecols=['y']),
                        'xy':pd.read_csv(KMEANS_PATH.joinpath("meanZero_clusterInertia.csv"),index_col=0,usecols=['xy'])
                    },
                },
                'predict':{
                    'label':'predict cluster number',
                    'data': {
                        'x':pd.read_csv(KMEANS_PATH.joinpath("meanZero_kMeansPredict_x.csv"),index_col=0),
                        'y':pd.read_csv(KMEANS_PATH.joinpath("meanZero_kMeansPredict_y.csv"),index_col=0),
                        'xy':pd.read_csv(KMEANS_PATH.joinpath("meanZero_kMeansPredict_xy.csv"),index_col=0)
                    }
                }
            },
            "medianZero": {
                'inertia':{
                    'label':'cluster inertia',
                    'data': {
                        'x':pd.read_csv(KMEANS_PATH.joinpath("medianZero_clusterInertia.csv"),index_col=0,usecols=['x']),
                        'y':pd.read_csv(KMEANS_PATH.joinpath("medianZero_clusterInertia.csv"),index_col=0,usecols=['y']),
                        'xy':pd.read_csv(KMEANS_PATH.joinpath("medianZero_clusterInertia.csv"),index_col=0,usecols=['xy'])
                    },
                },
                'predict':{
                    'label':'predict cluster number',
                    'data': {
                        'x':pd.read_csv(KMEANS_PATH.joinpath("medianZero_kMeansPredict_x.csv"),index_col=0),
                        'y':pd.read_csv(KMEANS_PATH.joinpath("medianZero_kMeansPredict_y.csv"),index_col=0),
                        'xy':pd.read_csv(KMEANS_PATH.joinpath("medianZero_kMeansPredict_xy.csv"),index_col=0)
                    }
                }
            },
            "firstPointZero": {
                'inertia':{
                    'label':'cluster inertia',
                    'data': {
                        'x':pd.read_csv(KMEANS_PATH.joinpath("firstPointZero_clusterInertia.csv"),index_col=0,usecols=['x']),
                        'y':pd.read_csv(KMEANS_PATH.joinpath("firstPointZero_clusterInertia.csv"),index_col=0,usecols=['y']),
                        'xy':pd.read_csv(KMEANS_PATH.joinpath("firstPointZero_clusterInertia.csv"),index_col=0,usecols=['xy'])
                    },
                },
                'predict':{
                    'label':'predict cluster number',
                    'data': {
                        'x':pd.read_csv(KMEANS_PATH.joinpath("firstPointZero_kMeansPredict_x.csv"),index_col=0),
                        'y':pd.read_csv(KMEANS_PATH.joinpath("firstPointZero_kMeansPredict_y.csv"),index_col=0),
                        'xy':pd.read_csv(KMEANS_PATH.joinpath("firstPointZero_kMeansPredict_xy.csv"),index_col=0)
                    }
                }
            }
        }

    def IO_dict(feature_unique,input_features):
        print('make IO')
        return {
            "id_user":{
                f'{key}':val.values for key,val in zip(feature_unique['id_user'],[input_features["feature"]['id_user']==key for key in feature_unique['id'] ])
            },
            "week":{
                f'{key}':val.values for key,val in zip(feature_unique['week'],[input_features["feature"]['week']==key for key in feature_unique['week'] ])
            },
            "eye_state":{
                f'{key}':val.values for key,val in zip(feature_unique['eye_state'],[input_features["feature"]['eye_state']==key for key in feature_unique['eye_state'] ])
            }
        }

def readData(
        input_data=False,input_indexes=False,input_features=False,feature_unique=False,figure_dict=False,feature_dict=False,kMeans_dict=False
    ):
    class_dataSets=dataSets
    #input_data,input_features,feature_unique,figure_dict,feature_dict,kMeans_dict
    if input_data==True:
        input_data=class_dataSets.Input_data()
        if input_indexes==True:
            input_indexes=class_dataSets.Input_indexes(input_data)
        if figure_dict==True:
            figure_dict=class_dataSets.Figure_dict(input_data)
    if input_features==True:
        input_features=class_dataSets.Input_features()
        if feature_unique==True:
            feature_unique=class_dataSets.Feature_unique(input_features)
            if feature_dict==True:
                feature_dict=class_dataSets.Feature_dict(feature_unique)

    if kMeans_dict==True:
        kMeans_dict=class_dataSets.KMeans_dict()
    return {
        "input_data":input_data,
        "input_indexes":input_indexes,
        "input_features":input_features,
        "feature_unique":feature_unique,
        "figure_dict":figure_dict,
        "feature_dict":feature_dict,
        "kMeans_dict":kMeans_dict
    }

