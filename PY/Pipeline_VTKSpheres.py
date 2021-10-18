from PY.Pipeline_VTK import *


class VTKSpherePipeline(VTKPipeline):
    def __init__(self):
        super(VTKSpherePipeline, self).__init__()

        self.sphereSrc = None
        self.selectedSphere = None

    def updateProperty(self, key, value):
        if key == 'sphereSize':
            self.sphereSrc.SetRadius(value)
            self.selectRadius = value * 2.0
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

        self.actors.append(actor)
