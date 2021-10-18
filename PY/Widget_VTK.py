import vtk

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import Qt

from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


class MousePickerInteractor(vtk.vtkInteractorStyleTrackballCamera):
    """
    The MousePickerInteractor provides the mechanism for picking in our window.
    """
    def __init__(self):
        super(MousePickerInteractor, self).__init__()
        self.AddObserver("LeftButtonPressEvent", self.handleLeftDown)
        self.AddObserver("LeftButtonReleaseEvent", self.handleLeftUp)

        self.lastPickedActor = None
        self.lastPickedProp = vtk.vtkProperty()
        self.tolerance = 0.001
        self.pipeline = None
        self.qtWidget = None

    def handleLeftDown(self, obj, event):
        print('Mouse Down Event')

        # Only care about this if we have something in the viewer
        if not self.pipeline:
            return

        clickPos = self.GetInteractor().GetEventPosition()
        picker = vtk.vtkPointPicker()
        picker.SetTolerance(self.tolerance)
        picker.SetUseCells(False)
        picker.Pick(clickPos[0], clickPos[1], 0, self.GetDefaultRenderer())
        pos = picker.GetPickPosition()
        print('  Pick at:  ' + str(pos[0]) + ', ' + str(pos[1]) + ', ' + str(pos[2]))
        ds = picker.GetDataSet()
        ptId = self.pipeline.vtkData.FindPoint(picker.GetPickPosition())
        print('  NodeID = ' + str(ptId))
        pointID = picker.GetPointId()
        print('  SphereVertex ID = ' + str(pointID))
        if pointID >= 0:
            self.pipeline.setHighlightedPoint(ptId)
            self.qtWidget.selectionMade(ptId)

        self.OnLeftButtonDown()

    def handleLeftUp(self, obj, event):
        print('Mouse Up Event')
        self.OnLeftButtonUp()

    def setPipeline(self, pipe):
        self.pipeline = pipe


class MousePickerInteractorForImage(vtk.vtkInteractorStyleTrackballCamera):
    """
    Need another version to work with Image VTK data
    """
    def __init__(self):
        super(MousePickerInteractorForImage, self).__init__()
        self.AddObserver("LeftButtonPressEvent", self.handleLeftDown)
        self.AddObserver("LeftButtonReleaseEvent", self.handleLeftUp)

        self.lastPickedActor = None
        self.lastPickedProp = vtk.vtkProperty()
        self.tolerance = 0.001
        self.pipeline = None
        self.qtWidget = None

    def handleLeftDown(self, obj, event):
        print('Mouse Down Event')
        self.OnLeftButtonDown()

    def handleLeftUp(self, obj, event):
        print('Mouse Up Event')
        self.OnLeftButtonUp()

    def setPipeline(self, pipe):
        self.pipeline = pipe


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
        if isImage:
            self.style = MousePickerInteractorForImage()
        else:
            self.style = MousePickerInteractor()

        self.style.SetDefaultRenderer(self.renderer)
        self.style.qtWidget = self
        self.interactor.SetInteractorStyle(self.style)

        # Set up a splitter so we can have some controls
        self.layout.addWidget(self.vtkWidget)

        if isImage:
            self.colors = vtk.vtkNamedColors()
            self.colors.SetColor('BkgColor', [191, 191, 191, 255])
            self.renderer.SetBackground(self.colors.GetColor3d("BkgColor"))

        self.renderer.ResetCamera()
        self.interactor.Initialize()
        self.interactor.Start()

    def selectionMade(self, ptId):
        self.pointSelected.emit(ptId)

    def reset(self):
        # We need to remove all the actors and clear the pipelines
        self.renderer.RemoveAllViewProps()
        self.pipeline = []

    def getVTKRenderer(self):
        return self.renderer

    def getVTKInteractor(self):
        return self.interactor

    def addActors(self, actors):
        for actor in actors:
            self.renderer.AddActor(actor)
        self.renderer.ResetCamera()

    def add2DActors(self, actors):
        for actor in actors:
            self.renderer.AddActor2D(actor)

    def addPipeline(self, pipeline, attach2DActors=True, isPickable=False):
        pipeline.setInteractor(self.interactor)
        pipeline.setRenderer(self.renderer)
        if isPickable:
            self.style.setPipeline(pipeline)
        if attach2DActors:
            self.add2DActors(pipeline.get2DActors())
        self.pipeline.append(pipeline)
        self.addActors(pipeline.getActors())

    def updateView(self):
        self.vtkWidget.GetRenderWindow().Render()

    def setHighlightIDs(self, idList):
        print('VTKWidget::setHighlightIDs() -- ' + str(idList))
        for pipe in self.pipeline:
            pipe.setHighlightIDs(idList)

    def updateProperty(self, key, value, updateView=True):
        for pipe in self.pipeline:
            pipe.updateProperty(key, value)
        if updateView:
            self.updateView()

    def updateLegend(self, legendType):
        for pipe in self.pipeline:
            pipe.updateLegend(legendType)

        self.updateView()
