import plotly.graph_objects as go
from tqdm import tqdm
import os
import pandas as pd
import glob
import numpy as np

def Read_csv_one(path,index_col=None):
    if(os.path.isfile(path)==True):
        df = pd.read_csv(path,index_col=index_col).dropna()
    return df

def Read_csv_multi(dir,index_col=None):
    csv_reader=pd.read_csv
    path_isfile=os.path.isfile
    files = glob.glob(fr"{dir}")
    files=[p for p in files if (os.path.isfile(p)==True)]
    print('reading file...')
    df=[csv_reader(path,index_col=index_col).dropna() for path in tqdm(files) if(path_isfile(path)==True)]
    return df

def Fig_xyz(x,y,z,traceName):
    scatterline3d=go.Scatter3d
    data=scatterline3d(x=x,y=y,z=z,line={"width":1},mode='lines',name=traceName)
    return data

def Fig_xy(x,y,traceName):
    scatterline=go.Scatter
    data=scatterline(x=x,y=y,line={"width":1},name=traceName)
    return data
#22222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222

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
def make_figure(input_data):
    figure_dict={}
    for dataType,val in input_data.items():
        dataMatrix=val["data"]
        timeX={}
        timeY={}
        XY={}
        timeXY={}
        for index,data in dataMatrix.iterrows():
            length=len(data)
            lengthHarf=int(length/2)
            N=6000
            time = np.linspace(5.01, 65, N, endpoint=True)
            data_x=data[0:lengthHarf]
            data_y=data[lengthHarf+1:length]
            timeX.update({f'{index}':Fig_xy(x=time,y=data_x,traceName=index)})
            timeY.update({f'{index}':Fig_xy(x=time,y=data_y,traceName=index)})
            XY.update({f'{index}':Fig_xy(x=data_x,y=data_y,traceName=index)})
            timeXY.update({f'{index}':Fig_xyz(x=data_x,y=data_y,z=time,traceName=index)})
        figure_dict.update({
            f'{dataType}':{
                "timeX":timeX,
                "timeY":timeY,
                "XY":XY,
                "timeXY":timeXY
            }
        })
    return figure_dict