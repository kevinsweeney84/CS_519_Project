from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from PY.Widget_Control import *
from PY.Pipeline_VTKSpheres import *
from PY.Pipeline_VTKTriangulation import *
from PY.Widget_VTK import *

import numpy as np

class ExplorerWindow(QMainWindow):
    closed = QtCore.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(ExplorerWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Delaunay Triangulation")

        self.buildInterior()

        self.polydata = None
        self.spheres = None

        self.locations = []
        self.connectControls()

    def buildInterior(self):
        """
        Method build the layout for the window
        :return:
        """
        self.splitter = QSplitter()
        self.setCentralWidget(self.splitter)

        # Add the VTK widget to the splitter (left)
        self.vtkWidget = VTKWidget()
        self.splitter.addWidget(self.vtkWidget)

        # Make a scroll widget to hold the controls
        scroll = QtWidgets.QScrollArea()

        # Create the control layout
        self.controls = ControlWidget()

        # Add the controls to the scroll and the splitter (right)
        self.splitter.addWidget(scroll)
        scroll.setWidget(self.controls)
        scroll.setWidgetResizable(True)

        self.splitter.setSizes([750, 250])

    def closeEvent(self, event):
        self.closed.emit()
        super().closeEvent(event)

    def connectControls(self):
        """
        Method connects all the controls for the app.
        :return:
        """
        self.controls.changeAlpha.connect(self.updateAlpha)
        self.controls.changeSphereSize.connect(self.updateSphereSize)
        self.controls.dataChanged.connect(self.updateData)
        self.controls.dataFileReadRequested.connect(self.readDataFile)
        self.controls.render.connect(self.updateRender)
        self.controls.projectRequested.connect(self.projectData)

        
    def projectData(self):

        self.polydata = self.convertToPolydata()
        self.vtkWidget.reset()

        self.setupDefaultPipelines()
    
    ''' Update functions'''

    def updateRender(self):
        self.vtkWidget.updateView()

    def updateSphereSize(self, val, updateRender=True):
        self.vtkWidget.updateProperty('sphereSize', val, updateRender)

    def updateAlpha(self, val, updateRender=True):
        self.vtkWidget.updateProperty('alpha', val, updateRender)

    def updateData(self, val):
        self.vtkWidget.updateProperty('vtkPoints', val)

    ''' Read / Write Files '''

    def readDataFile(self, filename):

        data = np.load(filename)
        self.locations = data

        return 

    ''' Other '''

    def setupDefaultPipelines(self, updateView=True):
        # Now that the polydata is read in, we need to create and install
        # some appropriate vtk pipelines, and update the info in the controls.
        self.spheres = VTKSpherePipeline()
        self.spheres.setupPipeline(self.polydata, self.controls.sphereSlider.value() / 100.0)
        self.vtkWidget.addPipeline(self.spheres, True)

        dims = self.getDimensions(self.polydata)
        if dims == 2:
            triangle = VTKTriangulatorPipeline()
            triangle.setupPipeline(self.polydata, self.controls.alphaSlider.value() / 100.0)
            self.vtkWidget.addPipeline(triangle, False)
        else:
            tets = VTKTetrahedralizerPipeline()
            tets.setupPipeline(self.polydata, self.controls.alphaSlider.value() / 100.0)
            self.vtkWidget.addPipeline(tets, False)

        if updateView:
            self.vtkWidget.updateView()

    def convertToPolydata(self):
        """
        Convert the input embedding space to a vtkPolyData type.  This will be a 3D object
        """

        pointdata = vtk.vtkPoints()

        for point in self.locations:
            pt = [0, 0, 0]
            # Determine the number of points available ( no more than 3 - 3D)
            numPts = min(len(point), 3)
            pt[0:numPts] = point[0:numPts]

            pointdata.InsertNextPoint(pt[0], pt[1], pt[2])

        polydata = vtk.vtkPolyData()
        polydata.SetPoints(pointdata)
        
        return polydata
        

    @staticmethod
    def getDimensions(data):
        """
        Method determines the dimension of the inputted polydata

        :param data:
        :return:
        """
        b = data.GetBounds()
        if b[0] == 0.0 and b[1] == 0.0:
            return 2
        if b[2] == 0.0 and b[3] == 0.0:
            return 2
        if b[4] == 0.0 and b[5] == 0.0:
            return 2
        return 3
