import os
import threading

import dash
import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output

from PY.ExplorerWindow import *


class Manager(QtCore.QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._view = None

    @property
    def view(self):
        return self._view

    def init_gui(self):
        self._view = ExplorerWindow()

    @QtCore.pyqtSlot()
    def show_popup(self):
        if self.view is not None:
            self.view.show()

    @QtCore.pyqtSlot()
    def reinit_gui(self):
        self._view = ExplorerWindow()


qt_manager = Manager()

app = dash.Dash(external_stylesheets=[dbc.themes.MATERIA])

project_description_card = dbc.Card(
    [
        dbc.CardHeader("Project Description", style={'fontWeight': 'bold'}),
        dbc.CardBody(
            [
                html.P(
                    '''Creation and visualisation of a Delaunay triangulation mesh on inputted 2D / 3D data using the VTK toolkit.''',
                    className="card-text",
                ),
                html.P(
                    '''Visualisation is housed within a QT application which is placed inside a Python dash app, allowing for external access.''',
                    className="card-text",
                )
            ]
        ),
    ]
)
contact_us_card = dbc.Card([
    dbc.CardHeader("Contact Us", style={'fontWeight': 'bold'}),
    dbc.CardBody(
        [
            html.Div([
                dbc.Row([
                    dbc.Col([
                        html.H6("Kevin Sweeney", className="card-subtitle"),
                        html.P(
                            "kts4 / kts4@illinois.edu",
                            className="card-text",
                        ),
                    ], width=6),

                    dbc.Col([
                        html.H6("Saurabh Sharma", className="card-subtitle"),
                        html.P(
                            "saurabh6 / saurabh6@illinois.edu",
                            className="card-text",
                        ),
                    ]),
                ], className="mb-2", ),
            ])
        ]
    ),
])
guide_card = dbc.Card([
    dbc.CardHeader("Guide/Instructions", style={'fontWeight': 'bold'}),
    dbc.CardBody(
        [
            html.Ul([
                html.Li("Click on 'LAUNCH APP' button below"),
                html.Ul([
                    html.Li("NOTE: The QT application will launch in a new window."),
                ]),
                html.Li("Click on the 'Select Data File (.npy)' button on top right hand side of the app"),
                html.Li("Select a .npy file from the available list of examples. "),
                html.Ul([
                    html.Li("There are some sample files provided in ../Data folder"),
                ]),
                html.Li("The chosen data will be shown in the left window of the QT application."),
                html.Ul([
                    html.Li("Data points are shown with the colour cyan"),
                    html.Li("Connections between data points are shown with a white line"),
                    html.Li("Connections between data points which create a triangle are shown by yellow lines"),
                    html.Li("Triangles are shown using the colour white"),
                ]),
                html.Li("The application allows the user to manipulate a number of parameters:"),
                html.Ul([
                    html.Li("Sphere: "),
                        html.Ul([
                            html.Li("Change the size of the data points"),
                        ]),
                    html.Li("Alpha: "),
                        html.Ul([
                            html.Li('''If a non-zero alpha distance value is specified (called the "alpha" value), then only tetrahedra, triangles, edges, and vertices laying within the alpha radius are output. 
                                    In other words, non-zero alpha values may result in arbitrary combinations of tetrahedra, triangles, lines, and vertices'''),
                        ]),
                    html.Li("Opacity: "),
                        html.Ul([
                            html.Li("Amend the opacity of the spheres / Delaunay mesh to be able to view structures within the mesh"),
                        ]),
                ]),
            ]),
            dbc.Button("Launch App", color="primary", id="startQT_btn"),
        ]
    )
])

sample_card = dbc.Card([
    dbc.CardHeader("Example", style={'fontWeight': 'bold'}),
    dbc.CardImg(src="/assets/image.png", bottom=True),
])

launch_app_card = dbc.Card([
    dbc.CardHeader("Let's Get Started", style={'fontWeight': 'bold'}),
    dbc.CardBody(
        [
            html.P("Click on the below button to launch the QT app"),
        ]
    )
])

app.layout = dbc.Container(
    fluid=True,
    children=[
        html.Div([
            dbc.Row(
                dbc.Col([
                    html.Div([
                        dbc.Row(
                            dbc.Col([
                                html.H2(""),
                                html.H2(""),
                            ]),
                            className="mb-2", ),
                        
                        dbc.Row(
                            dbc.Col([
                                html.H2("Creation and Visualisation of a Delaunay Triangulation Mesh", className="mb-2 text-center"),
                                html.H2("", id="result"),
                                project_description_card
                            ]),
                            className="mb-2", ),
                        dbc.Row([
                            dbc.Col([
                                guide_card
                            ], width=6),

                            dbc.Col([
                                sample_card,
                                contact_us_card
                            ]),
                            
                        ], className="mb-2", ),

                    ])],
                    width={"size": 10, "offset": 1},
                )
            ),
        ])
    ]
)


@app.callback(
    Output(component_id="result", component_property="children"),
    [Input(component_id="startQT_btn", component_property="n_clicks")],
)
def popUp(n_clicks):
    if not n_clicks:
        raise dash.exceptions.PreventUpdate

    loop = QtCore.QEventLoop()

    # Connecting the ExplorerWindow closure to quiting the loop
    qt_manager.view.closed.connect(loop.quit)

    QtCore.QMetaObject.invokeMethod(
        qt_manager, "reinit_gui", QtCore.Qt.QueuedConnection
    )

    QtCore.QMetaObject.invokeMethod(
        qt_manager, "show_popup", QtCore.Qt.QueuedConnection
    )
    loop.exec_()

    return "You saw a pop-up"


def main():
    qt_app = QtWidgets.QApplication.instance()

    if qt_app is None:
        qt_app = QtWidgets.QApplication([os.getcwd()])

    # Do not want to quit the app when the window is closed
    qt_app.setQuitOnLastWindowClosed(False)
    qt_manager.init_gui()

    threading.Thread(
        target=app.run_server,
        kwargs=dict(debug=False),
        daemon=True,
    ).start()

    return qt_app.exec_()


if __name__ == "__main__":
    main()
