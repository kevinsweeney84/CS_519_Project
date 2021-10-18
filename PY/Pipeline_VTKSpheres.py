from PY.Pipeline_VTK import *
import numpy as np


class VTKSpherePipeline(VTKPipeline):
    def __init__(self):
        super(VTKSpherePipeline, self).__init__()

        self.sphereSrc = None
        self.selectedSphere = None

    def updateProperty(self, key, value):
        if key == 'sphereSize':
            self.sphereSrc.SetRadius(value)
            self.selectRadius = value * 2.0
            self.sphereHighlighter.sphereSrc.SetRadius(self.selectRadius)
            print("Sphere Value: " + str(value))

    def update(self):
        self.interactor.Render()

    def setupPipeline(self, data, sphereSize):
        self.vtkData = data
        
        self.sphereSrc = vtk.vtkSphereSource()
        self.sphereSrc.SetRadius(sphereSize)
        self.selectRadius = 2 * sphereSize

        glyphs = vtk.vtkGlyph3D()
        glyphs.ScalingOff()
        glyphs.SetInputData(self.vtkData)
        glyphs.SetSourceConnection(self.sphereSrc.GetOutputPort())

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(glyphs.GetOutputPort())

        sProp = vtk.vtkProperty()
        sProp.SetOpacity(1.0)
        actor = vtk.vtkActor()
        actor.SetProperty(sProp)
        actor.SetMapper(mapper)

        # Setup our selection sphere
        self.selectedSphere = vtk.vtkSphereSource()
        self.selectedSphere.SetRadius(0.0)
        self.selectedSphere.SetCenter(0, 0, 0)
        sMapper = vtk.vtkPolyDataMapper()
        sMapper.SetInputConnection(self.selectedSphere.GetOutputPort())
        sActor = vtk.vtkActor()
        sProp = vtk.vtkProperty()
        sProp.SetColor(1, 1, 1)
        sProp.SetOpacity(0.5)
        sActor.SetProperty(sProp)
        sActor.SetMapper(sMapper)

        self.actors.append(actor)
        self.actors.append(sActor)
