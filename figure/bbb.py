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
all_cities =[option["value"] for option in options]

app.layout = html.Div(
    [
        dcc.Checklist(
            id="all-checklist",
            options=[{"label": "All", "value": "All"}],
            value=[],
            labelStyle={"display": "inline-block"},
        ),
        dcc.Checklist(
            id="city-checklist",
            options=options,
            value=[],
            labelStyle={"display": "inline-block"},
        ),
    ]
)
@app.callback(
    Output("city-checklist", "value"),
    Output("all-checklist", "value"),
    Input("city-checklist", "value"),
    Input("all-checklist", "value"),
)
def sync_checklists(selected,all_selected):
    ctx = dash.callback_context
    input_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if input_id == "all-checklist":
        through=all_selected
        if (all_selected == ["All"]):
            selected = all_cities
        else:
            selected = []
        return [selected,through]

    elif input_id == "city-checklist":
        through=selected
        if (set(selected) == set(all_cities)):
            all_selected = ["All"]
        else:
            all_selected = []
        return [through,all_selected]
    else:
        pass

if __name__ == "__main__":
    app.run_server(debug=True)