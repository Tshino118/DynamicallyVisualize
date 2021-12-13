# -*- coding: utf-8 -*-
import os
import dash

from demo import add_layout, add_callbacks

# for the Local version, import local_layout and local_callbacks
#from local import add_layout, add_callbacks
# 
# end
app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
app.title = "t-SNE Explorer"

server = app.server

app.layout = add_layout(app)
add_callbacks(app)

# for the Local version
#app.layout = local_layout(app)
#local_callbacks(app)

# Running server
if __name__ == "__main__":
    app.run_server(debug=True)



#only data0 visible
for d in fig.data:
    d.visible = False
fig.data[0].visible = True
kMeansColorList=[
    [ColorDict[clusterNumber] for clusterNumber in ser.values]
    for ser in kMeans_serList]

binColorDict=dict(zip(kMeansClusters,kMeansColorList))
#add dropdown
modeList=["lines+markers",'lines','markers']
nameList=features_df['id_user'].unique()

#make Binary Dictionary
binDict_name={key:np.where((features_df['id_user'] ==key), True,False) for key in nameList}
eye_stateList=['open','close']
binDict_eye={key:np.where((features_df['eye_state'] ==key), True,False) for key in eye_stateList}
week_List=features_df['week'].unique()
binDict_week={key:np.where((features_df['week'] ==key), True,False) for key in week_List}

logicalAnd=np.logical_and
binDict_name_eye_week={}
for name in nameList:
    for eye in eye_stateList:
        for week in week_List:
            binDict_name_eye_week=dict(**binDict_name_eye_week,**{f'{name}&{eye}&{week}': logicalAnd(logicalAnd(binDict_name[name],binDict_eye[eye]),binDict_week[week])})

binDict_name_eye={}
for name in nameList:
    for eye in eye_stateList:
            binDict_name_eye=dict(**binDict_name_eye,**{f'{name}&{eye}': logicalAnd(binDict_name[name],binDict_eye[eye])})

binDict_name_week={}
for name in nameList:
    for week in week_List:
        binDict_name_week=dict(**binDict_name_week,**{f'{name}&{week}': logicalAnd(binDict_name[name],binDict_week[week])})

binDict_eye_week={}
for eye in eye_stateList:
    for week in week_List:
        binDict_eye_week=dict(**binDict_eye_week,**{f'{eye}&{week}': logicalAnd(binDict_eye[eye],binDict_week[week])})
