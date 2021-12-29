import math
import pandas as pd

import pathlib
import os
# get relative data folder
PATH = pathlib.Path(__file__).parent
figSetting=pd.read_csv(PATH.joinpath("figSetting.csv"),index_col=['dataType','fig','feature','dimension'])

def fig_timeX(dataType):
    fig='timeX'
    layout={
        "xaxis": {
            "type": "linear",
            "dtick": 10,
            "range": figSetting.loc[dataType,fig,'range','x'],
            "ticks": "inside",
            "title": {
                "font": {
                    "size": 18
                },
                "text": "Move right-left"
            },
            "domain": [0,1],
            "showline": False,
            "tickmode": "linear",
            "autorange": False,
            "tickwidth": 1,
            "showspikes": False,
            "rangeslider": {
                "range": figSetting.loc[dataType,fig,'range','x'],
                "yaxis": {},
                "visible": False,
                "autorange": True
            },
            "zerolinecolor": "rgb(85, 94, 105)",
            "zerolinewidth": 2,
            "spikethickness": 10
        },
        "yaxis": {
            "type": "linear",
            "dtick": 10,
            "range": figSetting.loc[dataType,fig,'range','y'],
            "domain": [
                0,
                1
            ],
            "ticks": "inside",
            "title": {
                "font": {
                "size": 18
                },
                "text": "Move top-bottom"
            },
            "tickmode": "linear",
            "autorange": False,
            "tickwidth": 1,
            "fixedrange": False,
            "showspikes": False,
            "zerolinecolor": "rgb(85, 94, 105)",
            "zerolinewidth": 2,
            "spikethickness": 10
        },
        "margin": {
        "b": 10,
        "l": 10,
        "r": 10,
        "t": 100
        }
    }
    return layout
#
def fig_timeY(dataType):
    fig='timeY'
    layout={
        "xaxis": {
                "type": "linear",
                "dtick": 5,
                "range": figSetting.loc[dataType,fig,'range','x'],
                "ticks": "inside",
                "title": {
                    "font": {
                        "size": 18
                    },
                    "text": "time"
                },
            "domain": [
                0,
                1
            ],
            "showline": False,
            "tickmode": "linear",
            "autorange": False,
            "tickwidth": 1,
            "showspikes": False,
            "rangeslider": {
                "range": figSetting.loc[dataType,fig,'range','y'],
                "yaxis": {},
                "visible": False,
                "autorange": True
            },
            "zerolinecolor": "rgb(85, 94, 105)",
            "zerolinewidth": 2,
            "spikethickness": 10
        },
        "yaxis": {
            "type": "linear",
            "dtick": 5,
            "range": figSetting.loc[dataType,fig,'range','y'],
            "ticks": "inside",
            "title": {
                "font": {
                "size": 18
                },
                "text": "Move top-bottom"
            },
            "domain": [
                0,
                1
            ],
            "tickmode": "linear",
            "autorange": False,
            "tickwidth": 1,
            "fixedrange": False,
            "showspikes": False,
            "zerolinecolor": "rgb(85, 94, 105)",
            "zerolinewidth": 2,
            "spikethickness": 10
        },
        "margin": {
        "b": 10,
        "l": 10,
        "r": 100,
        "t": 10
        }
    }
    return layout
#
def fig_XY(dataType):
    fig='XY'
    layout={
        "xaxis": {
            "type": "linear",
            "dtick": 10,
            "range": figSetting.loc[dataType,fig,'range','x'],
            "ticks": "inside",
            "title": {
                "font": {
                    "size": 18
                },
                "text": "Move right-left"
            },
            "domain": [0,1],
            "showline": False,
            "tickmode": "linear",
            "autorange": False,
            "tickwidth": 1,
            "showspikes": False,
            "rangeslider": {
                "range": figSetting.loc[dataType,fig,'range','y'],
                "yaxis": {},
                "visible": False,
                "autorange": True
            },
            "zerolinecolor": "rgb(85, 94, 105)",
            "zerolinewidth": 2,
            "spikethickness": 10
        },
        "yaxis": {
            "type": "linear",
            "dtick": 10,
            "range": figSetting.loc[dataType,fig,'range','y'],
            'scaleanchor':"x",
            'scaleratio':1,
            "domain": [
                0,
                1
            ],
            "ticks": "inside",
            "title": {
                "font": {
                "size": 18
                },
                "text": "Move top-bottom"
            },
            "tickmode": "linear",
            "autorange": False,
            "tickwidth": 1,
            "fixedrange": False,
            "showspikes": False,
            "zerolinecolor": "rgb(85, 94, 105)",
            "zerolinewidth": 2,
            "spikethickness": 10
        },
        "margin": {
        "b": 10,
        "l": 10,
        "r": 10,
        "t": 100
        }
    }
    return layout
#
def fig_timeXY(dataType):
    fig='timeXY'
    layout={
        "scene": {
            "camera": {
                "projection": {
                    "type": "orthographic"
                }
            },
            "dragmode": "turntable",
            "xaxis": {
                "title": {
                    "font": {
                    "size": 18
                    },
                    "text": "Move right-left"
                },
                "range": figSetting.loc[dataType,fig,'range','x'],
            },
            "yaxis": {
                "title": {
                    "font": {
                    "size": 18
                    },
                    "text": "Move top-bottom"
                },
                "range": figSetting.loc[dataType,fig,'range','y'],
            },
            "zaxis": {
                "title": {
                    "font": {
                    "size": 18
                    },
                    "text": "time"
                },
                "range": figSetting.loc[dataType,fig,'range','z'],
            },
            "aspectratio": {
                "x": 1,
                "y": 1,
                "z": 0.8
            }
        },
        "dragmode": "zoom"
    }
    return layout  
#
def fig_contour():
    layout={
        "xaxis": {
            "side": "bottom", 
            "type": "linear", 
            "range": [-60,60],
            "domain": [0, 1], 
            "autorange": False,
            "dtick": 5,
            "ticks": "inside",
            "title": {
                "font": {
                    "size": 18
                },
                "text": "Move right-left"
            },
            "showline": False,
            "tickmode": "linear",
            "autorange": False,
            "tickwidth": 1,
            "showspikes": False,
            "rangeslider": {
                "range": [-60,60],
                "yaxis": {},
                "visible": False,
                "autorange": True
            },
            "zerolinecolor": "rgb(85, 94, 105)",
            "zerolinewidth": 2,
            "spikethickness": 10
        }, 
        "yaxis": {
            "type": "linear", 
            "range": [-60,60],
            "domain": [0, 1], 
            "autorange": False,
            'scaleanchor':"x",
            'scaleratio':1,
            "dtick": 5,
            "ticks": "inside",
            "title": {
                "font": {
                "size": 18
                },
                "text": "Move top-bottom"
            },
            "tickmode": "linear",
            "autorange": False,
            "tickwidth": 1,
            "fixedrange": False,
            "showspikes": False,
            "zerolinecolor": "rgb(85, 94, 105)",
            "zerolinewidth": 2,
            "spikethickness": 10
        }, 
        "modebar": {"orientation": "h"}, 
        "autosize": True
    }

    return layout 
#
def fig_mean(title):
    layout={
        'title':title,
        'width':800,
        "xaxis": {
            "type": "linear",
            "dtick": 5,
            "range": [-60,60],
            "ticks": "inside",
            "title": {
                "font": {
                    "size": 18
                },
                "text": "mean x"
            },
        "domain": [
            0,
            1
        ],
        "showline": False,
        "tickmode": "linear",
        "autorange": False,
        "tickwidth": 1,
        "showspikes": False,
        "rangeslider": {
            "range": [-60,60],
            "yaxis": {},
            "visible": False,
            "autorange": True
        },
        "zerolinecolor": "rgb(85, 94, 105)",
        "zerolinewidth": 2,
        "spikethickness": 10
        },
        "yaxis": {
            "type": "linear",
            "dtick": 5,
            "range": [-60,60],
            'scaleanchor':"x",
            'scaleratio':1,
            "ticks": "inside",
            "title": {
                "font": {
                "size": 18
                },
                "text": "mean y"
            },
            "domain": [
                0,
                1
            ],
            "tickmode": "linear",
            "autorange": False,
            "tickwidth": 1,
            "fixedrange": False,
            "showspikes": False,
            "zerolinecolor": "rgb(85, 94, 105)",
            "zerolinewidth": 2,
            "spikethickness": 10
        },
        "margin": {
        "b": 10,
        "l": 10,
        "r": 100,
        "t": 10
        }
    }
    return layout
#
def fig_multiContour(title):
    layout={
        'title':title,
        'width':800,
        "xaxis": {
            "side": "bottom", 
            "type": "linear", 
            "range": [-60,60],
            "domain": [0, 1], 
            "autorange": False,
            "dtick": 5,
            "ticks": "inside",
            "title": {
                "font": {
                    "size": 18
                },
                "text": "Move right-left"
            },
            "showline": False,
            "tickmode": "linear",
            "autorange": False,
            "tickwidth": 1,
            "showspikes": False,
            "rangeslider": {
                "range": [-60,60],
                "yaxis": {},
                "visible": False,
                "autorange": True
            },
            "zerolinecolor": "rgb(85, 94, 105)",
            "zerolinewidth": 2,
            "spikethickness": 10
        }, 
        "yaxis": {
            "type": "linear", 
            "range": [-60,60],
            "domain": [0, 1], 
            "autorange": False,
            'scaleanchor':"x",
            'scaleratio':1,
            "dtick": 5,
            "ticks": "inside",
            "title": {
                "font": {
                "size": 18
                },
                "text": "Move top-bottom"
            },
            "tickmode": "linear",
            "autorange": False,
            "tickwidth": 1,
            "fixedrange": False,
            "showspikes": False,
            "zerolinecolor": "rgb(85, 94, 105)",
            "zerolinewidth": 2,
            "spikethickness": 10
        }, 
        "modebar": {"orientation": "h"}, 
        "autosize": True
    }
    return layout
#
def fig_multiXYtime(title):
    layout={
        'title':title,
        "scene": {
            "camera": {
                "projection": {
                    "type": "orthographic"
                },
                'eye':{'x':1,'y':0,'z':0}
            },
            "dragmode": "turntable",
            "xaxis": {
                "title": {
                    "font": {
                    "size": 18
                    },
                    "text": "Move right-left"
                },
                "range": [-60,60],
            },
            "yaxis": {
                "title": {
                    "font": {
                    "size": 18
                    },
                    "text": "Move top-bottom"
                },
                "range": [-60,60],
            },
            "zaxis": {
                "title": {
                    "font": {
                    "size": 18
                    },
                    "text": "time"
                },
                "range": [0,65],
            },
            "aspectratio": {
                "x": 1,
                "y": 1,
                "z": 0.6
            }
        },
        "dragmode": "zoom",
        'sliders':[{
            'active':10,
            'steps':[{
                "method":"update",
                "args":[
                    {'eye':{'x':2*math.cos(i),'y':2*math.sin(i),'z':0}},
                    {"visible": [False] * 40},
                ]} for i in range(0,360,9)]
        }]
    }
    return layout  
#
def fig_correlogram(title):
    layout={
        'title':title,
        "xaxis": {
            "type": "linear", 
            "showgrid": False, 
            "zeroline": True, 
            "autorange": True,
        }, 
        "yaxis": {
            "type": "linear", 
            "showgrid": False, 
            "autorange": True, 
            "gridcolor": "rgb(98, 106, 123)", 
            "zerolinecolor": "rgb(36, 37, 39)",
            "range": [-1,1],
        }, 
    }
    return layout  
#
