from PyQt5 import QtCore, QtGui, Qt 

from PY.Box_Collapsible import CollapsibleBox

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


class ControlWidget(Qt.QWidget):
    ''' SIGNALS '''
    changeAlpha = QtCore.pyqtSignal(float)
    changeAlphaCheckbox = QtCore.pyqtSignal(bool)
    changeSphereSize = QtCore.pyqtSignal(float)
    changeOpacityValue = QtCore.pyqtSignal(float)
    dataChanged = QtCore.pyqtSignal()
    dataFileReadRequested = QtCore.pyqtSignal(str)
    projectRequested = QtCore.pyqtSignal()
    render = QtCore.pyqtSignal()

    def __init__(self):
        super(Qt.QWidget, self).__init__()

        self.setupControls()
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

        ''' Select Data to work with '''
        mainLayout = self.createLayoutLoad(mainLayout)
        mainLayout.addWidget(QHLine(sunken=False))

        ''' Manipulate Plot '''
        mainLayout = self.createLayoutManipulatePlot(mainLayout)
        mainLayout = self.createLayoutSphere(mainLayout)
        mainLayout = self.createLayoutAlpha(mainLayout)
        mainLayout = self.createLayoutOpacity(mainLayout)
        mainLayout.addWidget(QHLine(sunken=False))

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
        selectFilesLayout = Qt.QHBoxLayout()    # Vertical layout to hold all fields
        dataLayout = Qt.QVBoxLayout()           # Horizontal layout to hold latent space info
        dataLayout.setAlignment(Qt.Qt.AlignCenter)

        selectFilesLayout.addLayout(dataLayout)

        mainLayout.addLayout(selectFilesLayout)

        # Data button
        dataFile = Qt.QPushButton('Select Data File (.npy)')
        dataFile.clicked.connect(self.openDataFile)

        # text showing file name
        self.dataLbl = Qt.QLabel('--')
        self.dataLbl.setStyleSheet(self.fileTextStyle)

        dataLayout.addWidget(dataFile)
        dataLayout.addWidget(self.dataLbl)

        return mainLayout

    def createLayoutManipulatePlot(self, mainLayout):
        """
        Layout which sets up method for user to manipulate the plot data

        :param mainLayout:
        :return:
        """

        # Manipulate Plot Title 
        manipulatePlotText = Qt.QLabel('Manipulate Plot')
        manipulatePlotText.setAlignment(Qt.Qt.AlignCenter)
        manipulatePlotText.setStyleSheet(self.headingTextStyle)

        mainLayout.addWidget(manipulatePlotText)

        return mainLayout

    def createLayoutSphere(self, mainLayout):

        # Create Sphere Layout
        self.sphereInfoBox = CollapsibleBox("Sphere: Info")
        mainLayout.addWidget(self.sphereInfoBox)
        self.sphereInfoLayout = Qt.QVBoxLayout()

        infoSphere = Qt.QLabel("""The Slider allows the user to amend the size of the spheres representing the data points to allow for ease of viewing""")
        # infoSphere.setStyleSheet("background-color: white; border: 1px solid lightgrey; color:black")
        infoSphere.setWordWrap(True)

        self.sphereInfoLayout.addWidget(infoSphere)
        self.sphereInfoBox.setContentLayout(self.sphereInfoLayout)

        sphereLayout = Qt.QVBoxLayout()       # Vertical Layout to hold all Sphere controls
        sphereLayout.setAlignment(Qt.Qt.AlignTop)
        
        sphereTextLayout = Qt.QHBoxLayout() # Horizontal layout to hold text "Sphere Size" and text-value
        sphereLayout.addLayout(sphereTextLayout)
        
        sphereTextLayout.addWidget(Qt.QLabel("Sphere Size"))
        self.sphereLabel = Qt.QLabel('0.05', self)
        sphereTextLayout.addWidget(self.sphereLabel)

        self.sphereSlider = Qt.QSlider()
        self.sphereSlider.setOrientation(QtCore.Qt.Horizontal)
        self.sphereSlider.setMinimum(1)
        self.sphereSlider.setMaximum(50)
        self.sphereSlider.setValue(5)
        self.sphereSlider.valueChanged.connect(self.sphereSizeChanged)
        self.sphereSlider.setEnabled(False)
        sphereLayout.addWidget(self.sphereSlider)

        mainLayout.addLayout(sphereLayout)

        return mainLayout

    def createLayoutAlpha(self, mainLayout):

        # Create Alpha Layout 
        self.alphaInfoBox = CollapsibleBox("Alpha: Info")
        mainLayout.addWidget(self.alphaInfoBox)
        self.alphaInfoLayout = Qt.QVBoxLayout()
        
        infoAlpha = Qt.QLabel("""If a non-zero alpha distance value is specified (called the "alpha" value), then only tetrahedra, triangles, edges, and vertices laying within the alpha radius are output. In other words, non-zero alpha values may result in arbitrary combinations of tetrahedra, triangles, lines, and vertices""")
        # infoAlpha.setStyleSheet("background-color: white; border: 1px solid lightgrey; color:black")
        infoAlpha.setWordWrap(True)
        self.alphaInfoLayout.addWidget(infoAlpha)
        self.alphaInfoBox.setContentLayout(self.alphaInfoLayout)

        alphaLayout = Qt.QVBoxLayout()       # Vertical Layout to hold all Aplha controls
        alphaLayout.setAlignment(Qt.Qt.AlignTop)
        
        alphaTextLayout = Qt.QHBoxLayout()  # Horizontal layout to hold text "Alpha Value" and text-value
        alphaLayout.addLayout(alphaTextLayout)

        alphaTextLayout.addWidget(Qt.QLabel("Alpha Value"))
        self.alphaLabel = Qt.QLabel('0.15', self)
        alphaTextLayout.addWidget(self.alphaLabel)

        self.alphaSlider = Qt.QSlider()
        self.alphaSlider.setOrientation(QtCore.Qt.Horizontal)
        self.alphaSlider.setMinimum(1)
        self.alphaSlider.setMaximum(100)
        self.alphaSlider.setValue(15)
        self.alphaSlider.valueChanged.connect(self.alphaChanged)
        self.alphaSlider.setEnabled(False)
        alphaLayout.addWidget(self.alphaSlider)

        self.alphaCheckbox = Qt.QCheckBox("Turn Off Alpha", self)
        self.alphaCheckbox.stateChanged.connect(self.alphaCheckboxChanged)
        self.alphaCheckbox.setEnabled(False)
        alphaLayout.addWidget(self.alphaCheckbox)

        mainLayout.addLayout(alphaLayout)

        return mainLayout

    def createLayoutOpacity(self, mainLayout):

        # Create Opacity Layout
        self.opacityInfoBox = CollapsibleBox("Opacity: Info")
        mainLayout.addWidget(self.opacityInfoBox)
        self.opacityInfoLayout = Qt.QVBoxLayout()
        
        infoOpacity = Qt.QLabel("""The Slider allows the user to amend the opacity of the spheres / Delaunay mesh to be able to view structures within the mesh""")
        # infoOpacity.setStyleSheet("background-color: white; border: 1px solid lightgrey; color:black")
        infoOpacity.setWordWrap(True)

        self.opacityInfoLayout.addWidget(infoOpacity)
        self.opacityInfoBox.setContentLayout(self.opacityInfoLayout)

        opacityLayout = Qt.QVBoxLayout()       # Vertical Layout to hold all Opacity controls
        opacityLayout.setAlignment(Qt.Qt.AlignTop)

        opacityTextLayout = Qt.QHBoxLayout()   # Horizontal layout to hold text "Opacity Value" and text-value
        opacityLayout.addLayout(opacityTextLayout)
        
        opacityTextLayout.addWidget(Qt.QLabel("Opacity Value"))
        self.opacityLabel = Qt.QLabel('1', self)
        opacityTextLayout.addWidget(self.opacityLabel)

        self.opacitySlider = Qt.QSlider()
        self.opacitySlider.setOrientation(QtCore.Qt.Horizontal)
        self.opacitySlider.setMinimum(0)
        self.opacitySlider.setMaximum(100)
        self.opacitySlider.setValue(100)
        self.opacitySlider.valueChanged.connect(self.opacityValueChanged)
        self.opacitySlider.setEnabled(False)
        opacityLayout.addWidget(self.opacitySlider)

        mainLayout.addLayout(opacityLayout)

        # mainLayout.setSpacing(30)

        return mainLayout

    ''' SLOTS '''

    def openDataFile(self):
        
        fname = Qt.QFileDialog.getOpenFileName(None, "Select Data", "./Data/", "(*.npy)")

        if len(fname[0]) < 1:
            return

        self.dataFileReadRequested.emit(fname[0])
        self.dataLoaded = True

        self.setDataFileLbl(fname[0])

        self.projectRequested.emit()

        # Enable the "Manipulate Plot" Widgets
        self.sphereSlider.setEnabled(True)
        self.alphaSlider.setEnabled(True)
        self.alphaCheckbox.setEnabled(True)
        self.opacitySlider.setEnabled(True)

        self.opacitySlider.setValue(100)

    def alphaChanged(self, val):
        self.changeAlpha.emit(float(val) / 100.)
        self.alphaLabel.setText(str(val))

    def alphaCheckboxChanged(self, val):
        self.changeAlphaCheckbox.emit(val)


    def sphereSizeChanged(self, val):
        val = float(val) / 100.0
        self.changeSphereSize.emit(val)
        self.sphereLabel.setText(str(val))


    def opacityValueChanged(self, val):
        val = float(val) / 100.0
        self.changeOpacityValue.emit(val)
        self.opacityLabel.setText(str(val))

    ''' SETTERS '''

    def setDataFileLbl(self, fname):
        name = fname.split('/')
        self.dataLbl.setText(name[len(name) - 1])

    def setMaxSliders(self, val):

        self.sphereSlider.setMaximum(val)
        self.alphaSlider.setMaximum(val*10)

        self.sphereSlider.setValue(int(val/2))
        self.alphaSlider.setValue(int(val/2))
