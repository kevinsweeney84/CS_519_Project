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
        dbc.CardHeader("Project Description"),
        dbc.CardBody(
            [
                html.P(
                    "Provide a brief description of the project",
                    className="card-text",
                )
            ]
        ),
    ]
)
contact_us_card = dbc.Card([
    dbc.CardHeader("Contact Us"),
    dbc.CardBody(
        [
            html.H6("Kevin Sweeney", className="card-subtitle"),
            html.P(
                "kts4/kts4@illinois.edu",
                className="card-text",
            ),
            html.H6("Saurabh Sharma", className="card-subtitle"),
            html.P(
                "saurabh6/saurabh6@illinois.edu",
                className="card-text",
            ),
        ]
    ),
])
guide_card = dbc.Card([
    dbc.CardHeader("Guide/Instructions"),
    dbc.CardBody(
        [
            html.Ul([
                html.Li("Click on 'LAUNCH APP' button"),
                html.Li("Click on 'Select Data File (.npy) button on top right hand side of the app"),
                html.Li("Select a .npy file. There are some sample files provided in ../Data folder"),
                html.Li("Adjust Alpha and Sphere values using the slider to see triangulation at work"),
            ]),
        ]
    ),
    dbc.CardImg(src="/assets/image.png", bottom=True),
])
launch_app_card = dbc.Card([
    dbc.CardHeader("Let's Get Started"),
    dbc.CardBody(
        [
            html.P("Click on the below button to launch the QT app"),
            dbc.Button("Launch App", color="primary", id="startQT_btn"),
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
                                html.H2("Creation and Visualisation of a Delaunay Triangulation Mesh"),
                                html.H2("", id="result"),
                            ]),
                            className="mb-2 text-center", ),
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    dbc.Row([dbc.Col(project_description_card, )], className="mb-2", ),
                                    dbc.Row([dbc.Col(contact_us_card, )], className="mb-2", ),
                                    dbc.Row([dbc.Col([launch_app_card]), ], className="mb-2", ),
                                ]),
                            ], width=4),
                            dbc.Col([
                                guide_card
                            ])
                        ], className="mb-2", ),

                    ])],
                    width={"size": 8, "offset": 2},
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
