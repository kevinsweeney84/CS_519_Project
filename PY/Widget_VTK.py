import vtk

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import Qt

from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


class VTKWidget(Qt.QFrame):
    """
    The VTKWindow is a natural endpoint for a vtk pipeline.  It provides a single renderer
    and interactor and expects one (or more) actors to be attached to it.
    """

    ''' SIGNALS '''
    pointSelected = QtCore.pyqtSignal(int)

    def __init__(self, isImage=False):
        super(VTKWidget, self).__init__()
        # Set us up as a QFrame
        self.layout = Qt.QHBoxLayout()
        self.setLayout(self.layout)

        self.pipeline = []
        self.vtkWidget = QVTKRenderWindowInteractor(self)

        # Set up our vtk pipeline endpoint
        self.renderer = vtk.vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.renderer)
        self.interactor = self.vtkWidget.GetRenderWindow().GetInteractor()
        self.interactor.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())

        # Set up a splitter so we can have some controls
        self.layout.addWidget(self.vtkWidget)

        if isImage:
            self.colors = vtk.vtkNamedColors()
            self.colors.SetColor('BkgColor', [191, 191, 191, 255])
            self.renderer.SetBackground(self.colors.GetColor3d("BkgColor"))

        self.renderer.ResetCamera()
        self.interactor.Initialize()
        self.interactor.Start()

    def reset(self):
        # We need to remove all the actors and clear the pipelines
        self.renderer.RemoveAllViewProps()
        self.pipeline = []

    def addActors(self, actors):
        for actor in actors:
            self.renderer.AddActor(actor)
        self.renderer.ResetCamera()

    def add2DActors(self, actors):
        for actor in actors:
            self.renderer.AddActor2D(actor)

    def addPipeline(self, pipeline, attach2DActors=True):
        pipeline.setInteractor(self.interactor)
        pipeline.setRenderer(self.renderer)
        if attach2DActors:
            self.add2DActors(pipeline.get2DActors())
        self.pipeline.append(pipeline)
        self.addActors(pipeline.getActors())

    def updateView(self):
        self.vtkWidget.GetRenderWindow().Render()

    def updateProperty(self, key, value, updateView=True):
        for pipe in self.pipeline:
            pipe.updateProperty(key, value)
        if updateView:
            self.updateView()

