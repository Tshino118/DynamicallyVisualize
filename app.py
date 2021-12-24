# -*- coding: utf-8 -*-
import os
import dash

from demo import add_layout
from demoCallback import add_callbacks

# for the Local version, import local_layout and local_callbacks
#from local import add_layout, add_callbacks
# 
# end
app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
app.title = "Dynamically Visualize"

print('add app-callback')
server = app.server
app.layout = add_layout(app)
add_callbacks(app)

# for the Local version
#app.layout = local_layout(app)
#local_callbacks(app)

# Running server
if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=False)
