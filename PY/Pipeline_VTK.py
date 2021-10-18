import sys
import vtk

"""
The VTKPipeline is meant to act as a superclass that can be used 
to create VTK-based functionality.  It should terminate in one (or more) 
VTKActors which can be connected to a VTKWindow.
"""


class VTKPipeline:
    def __init__(self):
        self.actors = []
        self.actor2Ds = []
        self.renderer = None
        self.interactor = None
        self.vtkData = None
        self.highlightedPoint = -1

    def setHighlightedPoint(self, ptId):
        self.highlightedPoint = ptId
        self.interactor.Render()

    def setVTKData(self, data):
        self.vtkData = data

    def setRenderer(self, ren):
        self.renderer = ren

    def setInteractor(self, interactor):
        self.interactor = interactor

    def getActors(self):
        return self.actors

    def get2DActors(self):
        return self.actor2Ds

    def update(self):
        if self.renderer is None:
            return
        self.renderer.Render()

    def updateProperty(self, key, value):
        pass

    def setupPipeline(self, data):
        pass

    def setHighlightIDs(self, ptIdList):
        pass

    def updateLegend(self, legendType):
        pass
