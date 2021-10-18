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

    def setupPipeline(self, data, alphaValue):
        self.vtkData = data

        self.triangulator = vtk.vtkDelaunay2D()
        self.triangulator.SetAlpha(alphaValue)
        self.triangulator.SetInputDataObject(self.vtkData)

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(self.triangulator.GetOutputPort())

        sProp = vtk.vtkProperty()
        sProp.SetOpacity(1.0)
        actor = vtk.vtkActor()
        actor.SetProperty(sProp)
        actor.SetMapper(mapper)
        
        self.actors.append(actor)


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
            print("Alpha Value: " + str(value))

    def setupPipeline(self, data, alphaValue):
        self.vtkData = data

        self.triangulator = vtk.vtkDelaunay3D()
        self.triangulator.SetAlpha(alphaValue)
        print("Alpha Value: " + str(alphaValue))
        self.triangulator.SetInputData(self.vtkData)

        mapper = vtk.vtkDataSetMapper()
        
        mapper.SetInputConnection(self.triangulator.GetOutputPort())

        sProp = vtk.vtkProperty()
        sProp.SetOpacity(1.0)
        actor = vtk.vtkActor()
        actor.SetProperty(sProp)
        actor.SetMapper(mapper)
        
        self.actors.append(actor)
