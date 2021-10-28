import functools
import os
import threading

from PyQt5 import QtCore, QtWidgets

import dash
import dash_html_components as html
from dash.dependencies import Input, Output


class MainWindow(QtWidgets.QMainWindow):
    closed = QtCore.pyqtSignal()

    def closeEvent(self, event):
        self.closed.emit()
        super().closeEvent(event)


class Manager(QtCore.QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._view = None

    @property
    def view(self):
        return self._view

    def init_gui(self):
        self._view = MainWindow()

    @QtCore.pyqtSlot()
    def show_popup(self):
        if self.view is not None:
            self.view.show()


qt_manager = Manager()

app = dash.Dash()
server = app.server

print("__name__")
print(__name__)

app.layout = html.Div(
    children=[
        html.H1(children="Hello Dash"),
        html.Button("show pop up", id="button"),
        html.H2(children="", id="result"),
    ]
)


@app.callback(
    Output(component_id="result", component_property="children"),
    [Input(component_id="button", component_property="n_clicks")],
)
def popUp(n_clicks):
    if not n_clicks:
        raise dash.exceptions.PreventUpdate

    main()
    loop = QtCore.QEventLoop()

    print("qt_manager")
    print(qt_manager)
    print("qt_manager.view")
    print(qt_manager.view)

    qt_manager.view.closed.connect(loop.quit)
    QtCore.QMetaObject.invokeMethod(
        qt_manager, "show_popup", QtCore.Qt.QueuedConnection
    )
    loop.exec_()

    return "You saw a pop-up"


def main():
    qt_app = QtWidgets.QApplication.instance()
    if qt_app is None:
        qt_app = QtWidgets.QApplication([os.getcwd()])
    qt_app.setQuitOnLastWindowClosed(False)
    qt_manager.init_gui()
    threading.Thread(
        target=app.run_server, kwargs=dict(debug=False), daemon=True,
    ).start()

    return qt_app.exec_()


if __name__ == "__main__":
    main()

# import threading

# import dash
# from dash import html
# from dash.dependencies import Input, Output
# import os

# from PY.ExplorerWindow import *


# class Manager(QtCore.QObject):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self._view = None

#     @property
#     def view(self):
#         return self._view

#     def init_gui(self):
#         self._view = 'This is available' #ExplorerWindow()

#     @QtCore.pyqtSlot()
#     def show_popup(self):
#         if self.view is not None:
#             self.view.show()

#     @QtCore.pyqtSlot()
#     def reinit_gui(self):
#         self._view = ExplorerWindow()


# qt_manager = Manager()

# app = dash.Dash(__name__)
# server = app.server

# app.layout = html.Div(
#     children=[
#         html.H1(children="Hello Dash"),
#         html.Button("show pop up", id="startQT_btn"),
#         html.H2(children="", id="result"),
#     ]
# )


# @app.callback(
#     Output(component_id="result", component_property="children"),
#     [Input(component_id="startQT_btn", component_property="n_clicks")],
# )

# def popUp(n_clicks):
#     if not n_clicks:
#         raise dash.exceptions.PreventUpdate

#     loop = QtCore.QEventLoop()

#     print("Inside popUp")
#     print("qt_manager")
#     print(qt_manager)
#     print("qt_manager.view")
#     print(qt_manager.view)
#     print("loop")
#     print(loop)

#     # Connecting the ExplorerWindow closure to quiting the loop
#     qt_manager.view.closed.connect(loop.quit)
    
#     QtCore.QMetaObject.invokeMethod(
#         qt_manager, "reinit_gui", QtCore.Qt.QueuedConnection
#     )

#     QtCore.QMetaObject.invokeMethod(
#         qt_manager, "show_popup", QtCore.Qt.QueuedConnection
#     )
#     loop.exec_()


#     return "You saw a pop-up"


# def main():
#     qt_app = QtWidgets.QApplication.instance()

#     if qt_app is None:
#         qt_app = QtWidgets.QApplication([os.getcwd()])
    
#     # Do not want to quit the app when the window is closed
#     qt_app.setQuitOnLastWindowClosed(False)
#     qt_manager.init_gui()

#     threading.Thread(
#         target=app.run_server, 
#         kwargs=dict(debug=False), 
#         daemon=True,
#     ).start()

#     return qt_app.exec_()


# if __name__ == "__main__":
#     main()
