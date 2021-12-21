import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

options = [
    {"label": "New York City", "value": "NYC"},
    {"label": "Montréal", "value": "MTL"},
    {"label": "San Francisco", "value": "SF"},
]
app.layout = html.Div(
    [
        dcc.Checklist(
            id="checklist-id_user-all",
            options=[{"label": "All", "value": "All"}],
            value=[],
            labelStyle={"display": "inline-block"},
        ),
        dcc.Checklist(
            id="checklist-id_user",
            options=options,
            value=[],
            labelStyle={"display": "inline-block"},
        )
    ]
)
@app.callback(
    [
        Output("checklist-id_user-all", "value"),
        Output("checklist-id_user", "value")
    ],
    [
        Input("checklist-id_user-all", "value"),
        Input("checklist-id_user", "value"),
        State("checklist-id_user", "options"),
    ]
)
def sync_checklists(all_selected,selected,options):
    values=[option["value"] for option in options]
    ctx = dash.callback_context
    input_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if input_id == "checklist-id_user-all":
        through=all_selected
        if (all_selected == ["All"]):
            selected = values
        else:
            selected = []
        return [through, selected]

    elif input_id == "checklist-id_user":
        through=selected
        if (set(selected) == set(values)):
            all_selected = ["All"]
        else:
            all_selected = []
        return [all_selected, through]
    else:
        print("ERROR")

if __name__ == "__main__":
    app.run_server(debug=True)