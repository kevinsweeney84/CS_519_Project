import threading

import dash
from dash import html
from dash.dependencies import Input, Output
import os

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

app = dash.Dash()

server = app.server

app.layout = html.Div(
    children=[
        html.H1(children="Hello Dash"),
        html.Button("show pop up", id="startQT_btn"),
        html.H2(children="", id="result"),
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

    print("Just a test")

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
