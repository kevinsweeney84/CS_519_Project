from PYapp.AppLayout import *
from PYapp.AppCallbacks import *
import dash

#######################################
external_stylesheets = [
    {
        'href': 'https://use.fontawesome.com/releases/v5.8.1/css/all.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-50oBUHEmvpQ+1lW4y57PTFmhCaXp0ML5d60M1M7uH2+nqUivzIebhndOJK28anvf',
        'crossorigin': 'anonymous'
    },
    dbc.themes.SPACELAB
]

app = dash.Dash(external_stylesheets=external_stylesheets)
server = app.server

app.layout = AppLayout().build_layout()
register_callbacks(app)

#######################################

try:  # wrapping this, since a forum post said it may be deprecated at some point.
    app.title = "Visualising Delaunay Triangulation"
except:
    print("Could not set the page title!")

app.run_server(debug=False)
