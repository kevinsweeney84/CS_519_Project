from datetime import datetime
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg

from PyQt5 import QtCore, QtGui

from PY.Slider_ScalarBar import ScalarBarSlider
from PY.Checkbox_ScalarValues import ScalarValuesCheckboxes
from PY.Widget_ScalarDetails import *
from PY.Widget_NeighbourDetails import *
from PY.Widget_CompareDetails import *
from PY.Widget_MoleculeGraph import *
from PY.Widget_ViewImage import *
from PY.Box_Collapsible import CollapsibleBox
from PY.getenv import getenv

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvas

'''
NOTE:  Due to the self reference in the lambda function in addScalar, this class is NOT garbage collected
'''


class QHLine(Qt.QFrame):
    def __init__(self, sunken=True):
        super(QHLine, self).__init__()
        self.setFrameShape(Qt.QFrame.HLine)
        self.setStyleSheet("color: rgb(191,191,191)")
        self.setLineWidth(3)

        if sunken:
            self.setFrameShadow(Qt.QFrame.Sunken)


class QVLine(Qt.QFrame):
    def __init__(self):
        super(QVLine, self).__init__()
        self.setFrameShape(Qt.QFrame.VLine)
        self.setFrameShadow(Qt.QFrame.Sunken)
        self.setLineWidth(3)


class ScalarWeights(Qt.QWidget):
    def __init__(self):
        super(ScalarWeights, self).__init__()
        self.scalarInfo = {}
        self.scalarLbls = {}
        self.buildInterior()

    def buildInterior(self):
        self.layout = Qt.QFormLayout()
        self.setLayout(self.layout)

    def addScalar(self, name, indexInArray, weight=1.0):
        lbl = Qt.QLabel(name)
        spinner = Qt.QDoubleSpinBox()
        spinner.setMinimum(0.0)
        spinner.setMaximum(1000)
        spinner.setValue(weight)
        self.scalarInfo[indexInArray] = weight
        self.scalarLbls[indexInArray] = name
        spinner.valueChanged.connect(lambda d, index=indexInArray: self.setScalarWeight(index, d))
        self.layout.addRow(lbl, spinner)

    def setScalarWeight(self, index, val):
        self.scalarInfo[index] = val

    def getWeights(self):
        ret = []
        for i in range(len(self.scalarInfo.keys())):
            ret.append(0.0)

        for key in self.scalarInfo.keys():
            ret[key] = self.scalarInfo[key]

        return ret

    def getLabels(self):
        return self.scalarLbls


class ControlWidget(Qt.QWidget):
    ''' SIGNALS '''
    changeActiveScalars = QtCore.pyqtSignal(str)
    changeAlpha = QtCore.pyqtSignal(float)
    changeScalarRange = QtCore.pyqtSignal(float, float)
    changeSphereSize = QtCore.pyqtSignal(float)
    compareTypeChanged = QtCore.pyqtSignal(str)
    dataChanged = QtCore.pyqtSignal()
    fileWriteRequested = QtCore.pyqtSignal(str)
    dataFileReadRequested = QtCore.pyqtSignal(str)
    projectRequested = QtCore.pyqtSignal(str, int, bool, list)
    render = QtCore.pyqtSignal()
    retrainSystem = QtCore.pyqtSignal()
    runParamSweep = QtCore.pyqtSignal()
    screenshot = QtCore.pyqtSignal(str)
    showVtkImageDock = QtCore.pyqtSignal()
    vtkFileReadRequested = QtCore.pyqtSignal(str)

    def __init__(self):
        super(Qt.QWidget, self).__init__()

        self.activeAr = ''
        self.scalarRanges = {'logP': [-1.0, 5.0]}
        self.setupControls()
        self.scalarsLoaded = False
        self.coordsLoaded = False
        self.dataLoaded = False

    def setupControls(self):
        self.setMinimumWidth(200)
        mainLayout = Qt.QVBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(5)
        mainLayout.setAlignment(Qt.Qt.AlignCenter)
        self.setLayout(mainLayout)
        self.headingTextStyle = "font: 16pt; font-weight: bold; padding-top: 8px"
        self.fileTextStyle = "color: DodgerBlue; text-align: center;"

        ''' Screen shot and parameter sweep '''
        hLayout = Qt.QHBoxLayout()
        hLayout.setSpacing(20)
        mainLayout.addLayout(hLayout)

        sshot = Qt.QPushButton('Take Screenshot')
        sshot.clicked.connect(self.createScreenshot)
        hLayout.addWidget(sshot)

        self.sweep = Qt.QPushButton('Run Parameter Sweep')
        self.sweep.clicked.connect(self.runParamSweep)
        self.sweep.setEnabled(False)
        hLayout.addWidget(self.sweep)

        # Line
        mainLayout.addWidget(QHLine(sunken=False))

        ''' Select Data to work with '''
        mainLayout = self.createLayoutLoad(mainLayout)
        # mainLayout.addWidget(QHLine(sunken=False))

        ''' Project Data '''
        mainLayout = self.createLayoutProject(mainLayout)
        mainLayout.addWidget(QHLine(sunken=False))

        ''' Manipulate Plot '''
        mainLayout = self.createLayoutManipulatePlot(mainLayout)
        mainLayout.addWidget(QHLine(sunken=False))

        analyseOutput = Qt.QLabel("Analyse Output(s)")
        analyseOutput.setStyleSheet(self.headingTextStyle)
        mainLayout.addWidget(analyseOutput, alignment=Qt.Qt.AlignCenter)

        ''' Scalar Details '''
        if getenv("SHOW_SCALAR_BOX") == "True":
            mainLayout = self.createLayoutScalarDetails(mainLayout)
            mainLayout.addWidget(QHLine())

        ''' Molecule Graph '''
        if getenv("SHOW_MOLECULE_BOX") == "True":
            mainLayout = self.createLayoutMoleculeGraph(mainLayout)
            mainLayout.addWidget(QHLine())

        ''' View Input '''
        if getenv("SHOW_VIEW_INPUT_BOX") == "True":
            mainLayout = self.createLayoutViewImage(mainLayout)
            mainLayout.addWidget(QHLine())

        ''' Neighbour Details'''
        if getenv("SHOW_COMPARISON_BOX") == "True":
            mainLayout = self.createLayoutCompareNeighbours(mainLayout)
            mainLayout.addWidget(QHLine())

        mainLayout.addStretch()

    def createLayoutLoad(self, mainLayout):
        """
        Layout which sets up method for user to Select Data to work with

        :param mainLayout:
        :return:
        """

        # Heading
        loadText = Qt.QLabel('Load Required Data')
        loadText.setAlignment(Qt.Qt.AlignCenter)
        loadText.setStyleSheet(self.headingTextStyle)
        mainLayout.addWidget(loadText)

        # Organise layouts
        selectFilesLayout = Qt.QHBoxLayout()  # Vertical layout to hold all fields
        hdf5Layout = Qt.QVBoxLayout()  # Horizontal layout to hold latent space info
        hdf5Layout.setAlignment(Qt.Qt.AlignCenter)
        prevprojLayout = Qt.QVBoxLayout()  # Horizontal layout to hold Scalar info
        prevprojLayout.setAlignment(Qt.Qt.AlignCenter)

        selectFilesLayout.addLayout(hdf5Layout)
        selectFilesLayout.addWidget(QVLine())
        selectFilesLayout.addLayout(prevprojLayout)

        mainLayout.addLayout(selectFilesLayout)

        # HDF5 button
        hdf5File = Qt.QPushButton('Select Data File (.h5)')
        hdf5File.clicked.connect(self.openHdf5)

        # HDF5 text showing file name
        self.hdf5Lbl = Qt.QLabel('--')
        self.hdf5Lbl.setStyleSheet(self.fileTextStyle)

        openVTK = Qt.QPushButton('Open Prev. Projected Data')
        openVTK.clicked.connect(self.openVTK)
        openVTK.setEnabled(False)

        # Latent space text showing file name
        self.openVTKLbl = Qt.QLabel('--')
        self.openVTKLbl.setStyleSheet(self.fileTextStyle)

        hdf5Layout.addWidget(hdf5File)
        hdf5Layout.addWidget(self.hdf5Lbl)

        prevprojLayout.addWidget(openVTK)
        prevprojLayout.addWidget(self.openVTKLbl)

        return mainLayout

    def createLayoutProject(self, mainLayout):
        """
        Layout which sets up method for user to specify projection method etc

        :param mainLayout:
        :return:
        """
        projectHeaderText = Qt.QLabel('Projection Information')
        projectHeaderText.setAlignment(Qt.Qt.AlignCenter)
        projectHeaderText.setStyleSheet(self.headingTextStyle)
        mainLayout.addWidget(projectHeaderText)

        # Create layouts
        projectionInfoLayout = Qt.QHBoxLayout()  # Vertical layout to hold all fields
        projectChoiceLayout = Qt.QVBoxLayout()  # Horizontal layout to hold latent space info
        projectChoiceLayout.setAlignment(Qt.Qt.AlignTop)
        projectDimLayout = Qt.QVBoxLayout()  # Horizontal layout to hold Scalar info
        projectDimLayout.setAlignment(Qt.Qt.AlignTop)

        projectionInfoLayout.addLayout(projectChoiceLayout)
        projectionInfoLayout.addWidget(QVLine())
        projectionInfoLayout.addLayout(projectDimLayout)

        mainLayout.addLayout(projectionInfoLayout)

        projectionText = Qt.QLabel("Projection")
        self.projCombo = Qt.QComboBox()
        self.projCombo.setDuplicatesEnabled(False)
        self.projCombo.insertItem(0, 'PCA')
        self.projCombo.insertItem(0, 'UMAP')
        self.projCombo.insertItem(0, 'tSNE')
        self.projCombo.insertItem(0, 'ptSNE')

        projectChoiceLayout.addWidget(projectionText)
        projectChoiceLayout.addWidget(self.projCombo)

        dimensionText = Qt.QLabel("# Dimensions")
        self.dimCombo = Qt.QComboBox()
        self.dimCombo.insertItem(0, '3')
        self.dimCombo.insertItem(0, '2')

        projectDimLayout.addWidget(dimensionText)
        projectDimLayout.addWidget(self.dimCombo)

        # -------------- Line --------------
        mainLayout.addWidget(QHLine())
        # ----------------------------------

        # Create layouts
        appendScalarLayout = Qt.QHBoxLayout()  # Vertical layout to hold all fields
        appendScalarCheckboxLayout = Qt.QVBoxLayout()  # Horizontal layout to hold Append Scalar Checkbox
        appendScalarCheckboxLayout.setAlignment(Qt.Qt.AlignTop)
        appendScalarOptionsLayout = Qt.QVBoxLayout()  # Horizontal layout to hold Scalar options
        appendScalarOptionsLayout.setAlignment(Qt.Qt.AlignTop | Qt.Qt.AlignCenter)

        appendScalarLayout.addLayout(appendScalarCheckboxLayout)
        appendScalarLayout.addWidget(QVLine())
        appendScalarLayout.addLayout(appendScalarOptionsLayout)

        mainLayout.addLayout(appendScalarLayout)

        self.appendScalars = Qt.QCheckBox("")
        self.appendScalars.stateChanged.connect(self.appendScalersChanged)
        appendScalarText = Qt.QLabel("Append Scalars to Latent Space")
        appendScalarText.setWordWrap(True)

        appendScalarCheckboxSplitLayout = Qt.QFormLayout()
        appendScalarCheckboxSplitLayout.addRow(appendScalarText,
                                               self.appendScalars)
        appendScalarCheckboxLayout.addLayout(appendScalarCheckboxSplitLayout)

        scalarOptionsText = Qt.QLabel("Set Scalar Weights")
        self.scalarWeights = ScalarWeights()
        self.scalarWeights.hide()
        self.scalarWeights.setEnabled(False)
        appendScalarOptionsLayout.addWidget(scalarOptionsText)
        appendScalarOptionsLayout.addWidget(self.scalarWeights)

        # -------------- Line --------------
        mainLayout.addWidget(QHLine())
        # ----------------------------------

        projectionBtnsLayout = Qt.QHBoxLayout()  # Vertical layout to hold all fields
        mainLayout.addLayout(projectionBtnsLayout)

        self.reproj = Qt.QPushButton("Project Data")
        self.reproj.setEnabled(False)
        self.reproj.clicked.connect(self.project)
        projectionBtnsLayout.addWidget(self.reproj)

        export = Qt.QPushButton("Export Projection")
        export.clicked.connect(self.exportVTK)
        export.setEnabled(False)
        projectionBtnsLayout.addWidget(export)

        return mainLayout

    def createLayoutManipulatePlot(self, mainLayout):
        """
        Layout which sets up method for user to manipulate the plot data

        :param mainLayout:
        :return:
        """

        self.manipulatePlotBox = CollapsibleBox("Manipulate Plot")
        mainLayout.addWidget(self.manipulatePlotBox)
        self.manipulatePlotLayout = Qt.QVBoxLayout()

        manipulateSlidersLayout = Qt.QHBoxLayout()  # Vertical layout to hold all fields
        self.manipulatePlotLayout.addLayout(manipulateSlidersLayout)

        # Create layouts
        sphereSizeLayout = Qt.QVBoxLayout()  # Horizontal layout to hold latent space info
        sphereSizeLayout.setAlignment(Qt.Qt.AlignTop)
        alphaValueLayout = Qt.QVBoxLayout()  # Horizontal layout to hold Scalar info
        alphaValueLayout.setAlignment(Qt.Qt.AlignTop)

        manipulateSlidersLayout.addLayout(sphereSizeLayout)
        manipulateSlidersLayout.addWidget(QVLine())
        manipulateSlidersLayout.addLayout(alphaValueLayout)

        sphereSizeLayout.addWidget(Qt.QLabel("Sphere Size"))
        self.sphereSlider = Qt.QSlider()
        self.sphereSlider.setOrientation(QtCore.Qt.Horizontal)
        self.sphereSlider.setMinimum(1)
        self.sphereSlider.setMaximum(50)
        self.sphereSlider.setValue(5)
        self.sphereSlider.valueChanged.connect(self.sphereSizeChanged)
        self.sphereSlider.setEnabled(False)
        sphereSizeLayout.addWidget(self.sphereSlider)

        alphaValueLayout.addWidget(Qt.QLabel("Alpha Value"))
        self.alphaSlider = Qt.QSlider()
        self.alphaSlider.setOrientation(QtCore.Qt.Horizontal)
        self.alphaSlider.setMinimum(1)
        self.alphaSlider.setMaximum(100)
        self.alphaSlider.setValue(15)
        self.alphaSlider.valueChanged.connect(self.alphaChanged)
        self.alphaSlider.setEnabled(False)
        alphaValueLayout.addWidget(self.alphaSlider)

        # -------------- Line --------------
        self.manipulatePlotLayout.addWidget(QHLine())
        # ----------------------------------

        ''' Choice of active scalar and range for selected scalar '''

        # Create layouts
        scalarChoiceLayout = Qt.QHBoxLayout()  # Vertical layout to hold all fields
        activeScalarLayout = Qt.QVBoxLayout()  # Horizontal layout to hold latent space info
        scalarRangeLayout = Qt.QVBoxLayout()  # Horizontal layout to hold Scalar info
        scalarRangeLayout.setAlignment(Qt.Qt.AlignTop)

        scalarChoiceLayout.addLayout(activeScalarLayout)
        scalarChoiceLayout.addWidget(QVLine())
        scalarChoiceLayout.addLayout(scalarRangeLayout)

        self.manipulatePlotLayout.addLayout(scalarChoiceLayout)

        # Create the widgets
        activeScalarText = Qt.QLabel("Active Scalars")
        self.scalarCombo = Qt.QComboBox()
        self.scalarCombo.setEditable(False)
        self.scalarCombo.setEnabled(False)
        self.scalarCombo.currentTextChanged.connect(self.activeScalarsChanged)

        # Depending on type of data we will either have slider or checkboxes
        self.scalarRange = ScalarBarSlider()
        self.scalarRange.setEnabled(False)
        self.scalarRange.scalarRangeChanged.connect(self.userScalarRangeChanged)

        # self.scalarDiscreteValues = ScalarValuesCheckboxes()
        # self.scalarDiscreteValues.setEnabled(False)
        # self.scalarDiscreteValues.scalarValuesCheckboxesChanged.connect(self.userScalarValueCheckboxChanged)

        # Add them to the layout
        activeScalarLayout.addWidget(activeScalarText)
        activeScalarLayout.addWidget(self.scalarCombo)
        scalarRangeLayout.addWidget(self.scalarRange)
        # scalarRangeLayout.addWidget(self.scalarDiscreteValues)

        self.manipulatePlotBox.setContentLayout(self.manipulatePlotLayout)

        return mainLayout

    def createLayoutScalarDetails(self, mainLayout):
        self.scalarDetailsBox = CollapsibleBox("Scalar Details (Selected Point)")
        mainLayout.addWidget(self.scalarDetailsBox)
        self.scalarDetailsLayout = Qt.QVBoxLayout()

        self.scalarDetails = ScalarDetailsWidget()
        self.scalarDetailsLayout.addWidget(self.scalarDetails)

        self.scalarDetailsBox.setContentLayout(self.scalarDetailsLayout)

        return mainLayout

    def createLayoutMoleculeGraph(self, mainLayout):
        self.moleculeGraphBox = CollapsibleBox("Molecule Graph (Selected Point)")
        mainLayout.addWidget(self.moleculeGraphBox)
        self.moleculeGraphLayout = Qt.QVBoxLayout()

        self.moleculeGraph = MoleculeGraphWidget()
        self.moleculeGraphLayout.addWidget(self.moleculeGraph)

        self.moleculeGraphBox.setContentLayout(self.moleculeGraphLayout)

        return mainLayout

    def createLayoutViewImage(self, mainLayout):
        self.viewImageBox = CollapsibleBox("View Input Image (Selected Point)")
        mainLayout.addWidget(self.viewImageBox)
        self.viewImageLayout = Qt.QVBoxLayout()

        self.viewImage = ViewImageWidget()
        self.viewImageLayout.addWidget(self.viewImage)

        self.viewImageBox.setContentLayout(self.viewImageLayout)

        return mainLayout

    def createLayoutCompareNeighbours(self, mainLayout):
        self.neighbourBox = CollapsibleBox("Compare Points")
        mainLayout.addWidget(self.neighbourBox)
        self.neighbourLayout = Qt.QVBoxLayout()

        compareTypeRadio = Qt.QRadioButton("Compare kNN Neighbours")
        compareTypeRadio.setChecked(True)
        compareTypeRadio.type = "Neighbours"
        compareTypeRadio.toggled.connect(self.compareTypeRadioClicked)
        self.neighbourLayout.addWidget(compareTypeRadio)
        self.compareType = "Neighbours"

        compareTypeRadio = Qt.QRadioButton("Compare Selected Points")
        compareTypeRadio.type = "Points"
        compareTypeRadio.toggled.connect(self.compareTypeRadioClicked)
        self.neighbourLayout.addWidget(compareTypeRadio)

        # Line
        self.neighbourLayout.addWidget(QHLine())

        # Compare by Neighbours
        self.comparisonChoiceText = Qt.QLabel("Compare By:")
        self.compareByCombo = Qt.QComboBox()
        self.compareByCombo.setDuplicatesEnabled(False)
        self.compareByCombo.currentIndexChanged.connect(self.updateCompareLayout)

        self.neighbourLayout.addWidget(self.comparisonChoiceText)
        self.neighbourLayout.addWidget(self.compareByCombo)

        self.neighbourDetails = NeighbourDetailsWidget()
        self.neighbourLayout.addWidget(self.neighbourDetails)

        # Compare by Points
        self.compareDetails = CompareDetailsWidget()
        self.neighbourLayout.addWidget(self.compareDetails)

        self.graphLayout = Qt.QVBoxLayout()
        self.neighbourLayout.addLayout(self.graphLayout)
        self.setupBlankPlotScalarValues()

        # Add button for VTK image dock show / hide
        self.vtkImageBtn = Qt.QPushButton("Show Comparison Images")
        self.vtkImageBtn.clicked.connect(self.vtkImageBtnPressed)
        self.vtkImageBtn.setEnabled(False)
        self.vtkImageBtn.setMaximumWidth(200)
        self.neighbourLayout.addWidget(self.vtkImageBtn, alignment=Qt.Qt.AlignCenter)

        self.neighbourBox.setContentLayout(self.neighbourLayout)

        return mainLayout

    def compareTypeRadioClicked(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            self.compareType = radioButton.type
            print("Type is " + radioButton.type)
            self.compareTypeChanged.emit(radioButton.type)

    def setEmbeddingSpace(self, space):
        if getenv("SHOW_SCALAR_BOX") == "True":
            self.scalarDetails.setEmbeddingSpace(space)

        if getenv("SHOW_MOLECULE_BOX") == "True":
            self.moleculeGraph.setEmbeddingSpace(space)

        if getenv("SHOW_COMPARISON_BOX") == "True":
            self.neighbourDetails.setEmbeddingSpace(space)
            self.compareDetails.setEmbeddingSpace(space)

    ''' SLOTS '''

    def updateCompareLayout(self):
        if self.compareType == "Neighbours":
            self.neighbourDetails.setNeighbours(9999, None, self.compareByCombo.currentText())
        else:
            self.compareDetails.setCompare(-1, -1, self.compareByCombo.currentText())

    def vtkImageBtnPressed(self):
        self.showVtkImageDock.emit()

    def createScreenshot(self):
        print('createScreenshot')
        date = datetime.now()
        filename = date.strftime('%Y-%m-%d_%H-%M-%S.png')
        self.screenshot.emit(filename)

    def openHdf5(self):
        print('openHdf5')
        # fname = Qt.QFileDialog.getOpenFileName(None, "Read HDF5 Data", getenv("FOLDER_DATA"), "(*.h5)")
        # TODO Remove
        fname = (getenv("FOLDER_DATA") + 'Example3D_1.npy', "(*.npy)")

        if len(fname[0]) < 1:
            return

        print('emitting dataFileReadRequested(' + fname[0] + ')')
        self.dataFileReadRequested.emit(fname[0])
        self.dataLoaded = True
        self.initializeProjectButtons()

    def openVTK(self):
        print('openVTK')
        fname = Qt.QFileDialog.getOpenFileName(self, "Open Projection", "", "(*.vtk)")
        if len(fname) < 1:
            return
        self.vtkFileReadRequested.emit(fname[0])

    def project(self):
        method = self.projCombo.currentText()
        dim = int(self.dimCombo.currentText())
        useScalars = self.appendScalars.isChecked()
        weights = self.scalarWeights.getWeights()

        if useScalars:
            print(weights)

        self.projectRequested.emit(method, dim, useScalars, weights)

        # Enable the "Manipulate Plot" Widgets
        self.sphereSlider.setEnabled(True)
        self.alphaSlider.setEnabled(True)
        self.scalarCombo.setEnabled(True)
        self.scalarRange.setEnabled(True)

        self.sweep.setEnabled(True)

        if getenv("SHOW_SCALAR_BOX") == "True":
            self.scalarDetails.show()
        if getenv("SHOW_MOLECULE_BOX") == "True":
            self.moleculeGraph.show()
        if getenv("SHOW_COMPARISON_BOX") == "True":
            self.neighbourDetails.show()

    @staticmethod
    def exportVTK():
        fname = Qt.QFileDialog.getSaveFileName(None, "Write VTK Data", ".", "(*.vtk)")
        if len(fname) < 1:
            return
        print('Export as VTK - ' + fname)

    def triggerRender(self):
        # Signal a re-render
        self.render.emit()

    def retrainRequested(self):
        self.retrainSystem.emit()

    def appendScalersChanged(self):
        if self.appendScalars.isChecked():
            self.scalarWeights.setEnabled(True)
        else:
            self.scalarWeights.setEnabled(False)

    def userScalarRangeChanged(self, minv, maxv):
        self.scalarRanges[self.activeAr] = [minv, maxv]
        self.changeScalarRange.emit(minv, maxv)

    def userScalarValueCheckboxChanged(self):
        checkedBoxes = self.scalarDiscreteValues.checkedBoxes
        self.changeScalarCheckboxes.emit(checkedBoxes)

    def alphaChanged(self, val):
        self.changeAlpha.emit(float(val) / 100.)

    def activeScalarsChanged(self, val):
        print('Changing Active Scalars to: ' + val)
        self.activeAr = val
        self.changeActiveScalars.emit(val)

    def sphereSizeChanged(self, val):
        val = float(val) / 100.0
        self.changeSphereSize.emit(val)

    ''' SETTERS '''

    def setScalarArrays(self, arNames, currentSet):
        if self.scalarCombo.count() > 0:
            return

        self.scalarCombo.clear()
        for name in arNames:
            self.scalarCombo.addItem(name)

        self.scalarCombo.setCurrentText(currentSet)

    def setDataRange(self, minv, maxv):
        self.scalarRange.setDataRange(minv, maxv)

    def setUserRange(self, minv, maxv):
        self.scalarRange.setUserRange(minv, maxv)

    def setCheckboxes(self, names):
        for name in names:
            print("adding checkbox: " + name)
            self.scalarDiscreteValues.createCheckbox(name)

    def setDataFile(self, fname):
        name = fname.split('/')
        self.hdf5Lbl.setText(name[len(name) - 1])

    ''' Support funcs '''

    def updateScalarInfoControl(self, space):
        if getenv("SHOW_SCALAR_BOX") == "True":
            self.scalarDetails.rebuildInterior()

        # Add the scalars to our weight form
        scalars = space.getNumericScalars()

        # Do not add scalars which are just labels
        scalars = [x for x in scalars if "_label" not in x]

        for i in range(len(scalars)):
            name = scalars[i]
            print('name = ' + name + ' : idx = ' + str(i))
            self.scalarWeights.addScalar(name, i)

        if getenv("SHOW_COMPARISON_BOX") == "True":
            for i in range(len(space.scalarLbls_)):
                self.compareByCombo.insertItem(0, space.scalarLbls_[i])

    def initializeProjectButtons(self):
        if (self.coordsLoaded & self.scalarsLoaded) | self.dataLoaded:
            self.reproj.setEnabled(True)
        else:
            self.reproj.setEnabled(False)

        # We also must show and populate our scalar weight dialog
        # Note that the scalar fields are populated in the setScalarArrays func
        if self.scalarsLoaded | self.dataLoaded:
            self.scalarWeights.show()
        else:
            self.scalarWeights.hide()

    def setupBlankPlotScalarValues(self):
        self.canvas = FigureCanvas(Figure())
        self.graphLayout.addWidget(self.canvas)
        self.ax = self.canvas.figure.subplots()

    def plotScalarValues(self):
        import numpy as np

        # Delete the previous graph
        self.graphLayout.removeWidget(self.canvas)
        self.canvas.deleteLater()
        self.canvas = None

        # Create the new canvas
        self.canvas = FigureCanvas(Figure())
        self.graphLayout.addWidget(self.canvas)
        self.ax = self.canvas.figure.subplots()

        if self.compareType == "Neighbours":
            allScalarValues = self.neighbourDetails.allScalarValues
            neighbourScalarValues = self.neighbourDetails.neighbourScalarValues
            scalarName = self.neighbourDetails.scalarName
        else:
            allScalarValues = self.compareDetails.allScalarValues
            neighbourScalarValues = self.compareDetails.neighbourScalarValues
            scalarName = self.compareDetails.scalarName

        # Convert from a list to an array
        try:
            npa = np.asarray(allScalarValues, dtype=np.float32)

            print(npa)

            # Plot the histogram
            self.ax.hist(npa, 50, alpha=0.25)

            # Plot the scalar values as vertical lines, the first one (selected point) will be red
            self.ax.axvline(float(neighbourScalarValues[0]),
                            color='r', linestyle='solid', linewidth=2)
            for i in range(1, len(neighbourScalarValues)):
                self.ax.axvline(float(neighbourScalarValues[i]),
                                color='k', linestyle='dashed', linewidth=1)

            self.ax.set_title(scalarName)
        except ValueError:
            print("Can not plot this data type")
