from PY.Pipeline_VTK import *

'''
The VTKTriangulatorPipeline is a pipeline that handles 2D triangulation using
alpha-shape constrained Delaunay triangulation
'''


class VTKTriangulatorPipeline(VTKPipeline):
    def __init__(self):
        super(VTKTriangulatorPipeline, self).__init__()
        self.triangulator = None

    def updateProperty(self, key, value):
        if key == 'alpha':
            self.triangulator.SetAlpha(value)

            cellData = vtk.vtkUnsignedCharArray()
            cellData.SetName("colors")
            cellData.SetNumberOfComponents(3)
            
            for i in range(self.triangulator.GetOutput().GetNumberOfCells()):                
                cellData.InsertNextTypedTuple((255,0,0))

            self.triangulator.GetOutput().GetCellData().SetScalars(cellData)
        
        if key == 'opacityValue':
            sProp = vtk.vtkProperty()
            sProp.SetOpacity(value)
            self.actor.SetProperty(sProp)

    def setupPipeline(self, data, alphaValue):
        self.vtkData = data

        self.triangulator = vtk.vtkDelaunay2D()
        self.triangulator.SetAlpha(alphaValue)

        self.triangulator.SetInputDataObject(self.vtkData)

        cellData = vtk.vtkUnsignedCharArray()
        cellData.SetName("colors")
        cellData.SetNumberOfComponents(3)

        for i in range(self.triangulator.GetOutput().GetNumberOfCells()):                
            cellData.InsertNextTypedTuple((255,0,0))

        self.triangulator.GetOutput().GetCellData().SetScalars(cellData)

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(self.triangulator.GetOutputPort())
        mapper.SetScalarModeToUseCellData()

        sProp = vtk.vtkProperty()
        sProp.SetOpacity(1.0)
        self.actor = vtk.vtkActor()
        self.actor.SetProperty(sProp)
        self.actor.SetMapper(mapper)
        self.actor.GetProperty().SetInterpolationToFlat()
        
        self.actors.append(self.actor)


'''
The VTKTetrahedralizerPipeline is a pipeline that handles 3D tetrahedralization using
alpha-shape constrained Delaunay tetrahedralization.
'''


class VTKTetrahedralizerPipeline(VTKPipeline):
    def __init__(self):
        super(VTKTetrahedralizerPipeline, self).__init__()
        self.triangulator = None

    def updateProperty(self, key, value):
        if key == 'alpha':
            self.triangulator.SetAlpha(value)
        
        if key == 'opacityValue':
            sProp = vtk.vtkProperty()
            sProp.SetOpacity(value)
            self.actor.SetProperty(sProp)

    def setupPipeline(self, data, alphaValue):
        self.vtkData = data

        self.triangulator = vtk.vtkDelaunay3D()
        self.triangulator.SetAlpha(alphaValue)
        
        self.triangulator.SetInputData(self.vtkData)

        cellData = vtk.vtkUnsignedCharArray()
        cellData.SetName("colors")
        cellData.SetNumberOfComponents(3)

        for i in range(self.triangulator.GetOutput().GetNumberOfCells()):                
            cellData.InsertNextTypedTuple((255,0,0))

        self.triangulator.GetOutput().GetCellData().SetScalars(cellData)

        mapper = vtk.vtkDataSetMapper()
        mapper.SetInputConnection(self.triangulator.GetOutputPort())
        mapper.SetScalarModeToUseCellData()

        sProp = vtk.vtkProperty()
        sProp.SetOpacity(1.0)
        self.actor = vtk.vtkActor()
        self.actor.SetProperty(sProp)
        self.actor.SetMapper(mapper)
        self.actor.GetProperty().SetInterpolationToFlat()
        
        self.actors.append(self.actor)
