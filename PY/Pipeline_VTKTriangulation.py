from PY.Pipeline_VTK import *

'''
The VTKTriangulatorPipeline is a pipeline that handles 2D triangulation using
alpha-shape constrained Delaunay triangulation
'''


class VTKTriangulatorPipeline(VTKPipeline):
    def __init__(self):
        super(VTKTriangulatorPipeline, self).__init__()
        self.opacity = 1
        self.triangulator = None

    def updateProperty(self, key, value):
        if key == 'alpha':
            self.triangulator.SetAlpha(value)

            self.add_colour()
        
        if key == 'opacityValue':

            self.opacity = value
            self.add_colour()

    def setupPipeline(self, data, alphaValue):
        self.vtkData = data

        self.triangulator = vtk.vtkDelaunay2D()
        self.triangulator.SetAlpha(alphaValue)

        self.triangulator.SetInputDataObject(self.vtkData)

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(self.triangulator.GetOutputPort())

        sProp = vtk.vtkProperty()
        sProp.SetOpacity(1.0)
        self.actor = vtk.vtkActor()
        self.actor.SetProperty(sProp)
        self.actor.SetMapper(mapper)
        self.add_colour()
        
        self.actors.append(self.actor)

    def add_colour(self,):
        self.actor.GetProperty().SetEdgeVisibility(1)
        self.actor.GetProperty().SetEdgeColor(0.9,0.9,0.4)
        self.actor.GetProperty().SetLineWidth(6)
        self.actor.GetProperty().SetRenderLinesAsTubes(1)
        self.actor.GetProperty().SetVertexVisibility(1)
        self.actor.GetProperty().SetVertexColor(0.5,1.0,0.8)
        self.actor.GetProperty().SetOpacity(self.opacity )


'''
The VTKTetrahedralizerPipeline is a pipeline that handles 3D tetrahedralization using
alpha-shape constrained Delaunay tetrahedralization.
'''


class VTKTetrahedralizerPipeline(VTKPipeline):
    def __init__(self):
        super(VTKTetrahedralizerPipeline, self).__init__()
        self.triangulator = None
        self.opacity = 1

    def updateProperty(self, key, value):
        if key == 'alpha':
            self.triangulator.SetAlpha(value)
            
            self.add_colour()
        
        if key == 'opacityValue':
            self.opacity = value
            self.add_colour()

    def setupPipeline(self, data, alphaValue):
        self.vtkData = data

        self.triangulator = vtk.vtkDelaunay3D()
        self.triangulator.SetAlpha(alphaValue)
        
        self.triangulator.SetInputData(self.vtkData)

        mapper = vtk.vtkDataSetMapper()
        mapper.SetInputConnection(self.triangulator.GetOutputPort())

        sProp = vtk.vtkProperty()
        sProp.SetOpacity(1.0)
        self.actor = vtk.vtkActor()
        self.actor.SetProperty(sProp)
        self.actor.SetMapper(mapper)
        self.add_colour()
        
        self.actors.append(self.actor)

    def add_colour(self):
        self.actor.GetProperty().SetEdgeVisibility(1)
        self.actor.GetProperty().SetEdgeColor(0.9,0.9,0.4)
        self.actor.GetProperty().SetLineWidth(6)
        self.actor.GetProperty().SetRenderLinesAsTubes(1)
        self.actor.GetProperty().SetVertexVisibility(1)
        self.actor.GetProperty().SetVertexColor(0.5,1.0,0.8)
        self.actor.GetProperty().SetOpacity(self.opacity)