import vtk
import numpy as np
import matplotlib.pyplot as plt

import vtk
import numpy as np
import matplotlib.pyplot as plt

class VtkColorPointCloud:

    def __init__(self, zMin=-10000.0, zMax=10000.0, maxNumPoints=2e8):
        self.maxNumPoints = maxNumPoints
        self.vtkPolyData = vtk.vtkPolyData()
        self.clearPoints()
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(self.vtkPolyData)
        mapper.SetColorModeToDefault()
        mapper.SetScalarRange(zMin, zMax)
        mapper.SetScalarVisibility(1)
        self.vtkActor = vtk.vtkActor()
        self.vtkActor.SetMapper(mapper)

    def addPoint(self, point,color):
        if self.vtkPoints.GetNumberOfPoints() < self.maxNumPoints:
            pointId = self.vtkPoints.InsertNextPoint(point[:])
            self.vtkDepth.InsertNextTuple3(color[0],color[1],color[2])
            self.vtkCells.InsertNextCell(1)
            self.vtkCells.InsertCellPoint(pointId)
        else:
            raise TypeError("too many points")
            
        self.vtkCells.Modified()
        self.vtkPoints.Modified()
        self.vtkDepth.Modified()

    def clearPoints(self):
        self.vtkPoints = vtk.vtkPoints()
        self.vtkCells = vtk.vtkCellArray()
        self.vtkDepth = vtk.vtkUnsignedCharArray()
        self.vtkDepth.SetNumberOfComponents(3)
        self.vtkDepth.SetName('DepthArray')
        self.vtkPolyData.SetPoints(self.vtkPoints)
        self.vtkPolyData.SetVerts(self.vtkCells)
        self.vtkPolyData.GetPointData().SetScalars(self.vtkDepth)
        self.vtkPolyData.GetPointData().SetActiveScalars('DepthArray')

def showcolorpoints(points,colors):
    pointCloud = VtkColorPointCloud()
    for k in range(points.shape[0]):
        point = points[k,:]
        color = colors[k,:]
        pointCloud.addPoint(point,color)
    pointCloud.addPoint([0,0,0],[0,0,0])
    pointCloud.addPoint([0,1,0],[0,0,0])
    pointCloud.addPoint([0,0,1],[0,0,0])
    pointCloud.addPoint([1,0,0],[0,0,0])

    # add axes
    axes = vtk.vtkAxesActor()
    axes.SetTotalLength(100.0, 100.0, 100.0)

    # Renderer
    renderer = vtk.vtkRenderer()
    renderer.AddActor(pointCloud.vtkActor)
    renderer.AddActor(axes)
    renderer.SetBackground(0, 0, 0)
    renderer.ResetCamera()

    # Render Window
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(renderer)

    # Interactor
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)

    # Begin Interaction
    renderWindow.Render()
    renderWindowInteractor.Start()


class VtkPointCloud:

    def __init__(self, zMin=-10000.0, zMax=10000.0, maxNumPoints=2e8):
        self.maxNumPoints = maxNumPoints
        self.vtkPolyData = vtk.vtkPolyData()
        self.clearPoints()
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(self.vtkPolyData)
        mapper.SetColorModeToDefault()
        mapper.SetScalarRange(zMin, zMax)
        mapper.SetScalarVisibility(1)
        self.vtkActor = vtk.vtkActor()
        self.vtkActor.SetMapper(mapper)

    def addPoint(self, point):
        if self.vtkPoints.GetNumberOfPoints() < self.maxNumPoints:
            pointId = self.vtkPoints.InsertNextPoint(point[:])
            self.vtkDepth.InsertNextValue(point[2])
            self.vtkCells.InsertNextCell(1)
            self.vtkCells.InsertCellPoint(pointId)
        else:
        	raise TypeError("too many points")
        	
        self.vtkCells.Modified()
        self.vtkPoints.Modified()
        self.vtkDepth.Modified()

    def clearPoints(self):
        self.vtkPoints = vtk.vtkPoints()
        self.vtkCells = vtk.vtkCellArray()
        self.vtkDepth = vtk.vtkDoubleArray()
        self.vtkDepth.SetName('DepthArray')
        self.vtkPolyData.SetPoints(self.vtkPoints)
        self.vtkPolyData.SetVerts(self.vtkCells)
        self.vtkPolyData.GetPointData().SetScalars(self.vtkDepth)
        self.vtkPolyData.GetPointData().SetActiveScalars('DepthArray')

def showpoints(points):
    pointCloud = VtkPointCloud()
    for k in range(points.shape[0]):
        point = points[k,:]
        pointCloud.addPoint(point)
    pointCloud.addPoint([0,0,0])
    pointCloud.addPoint([0,1,0])
    pointCloud.addPoint([0,0,1])
    pointCloud.addPoint([1,0,0])

    # add axes
    axes = vtk.vtkAxesActor()
    axes.SetTotalLength(100.0, 100.0, 100.0)

    # Renderer
    renderer = vtk.vtkRenderer()
    renderer.AddActor(pointCloud.vtkActor)
    renderer.AddActor(axes)
    renderer.SetBackground(0, 0, 0)
    renderer.ResetCamera()

    # Render Window
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(renderer)

    # Interactor
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)

    # Begin Interaction
    renderWindow.Render()
    renderWindowInteractor.Start()

def show2d(tmp):

    h = (tmp - tmp.min(axis = 0)).astype(np.int32)
    I = np.zeros([h.max()+1,h.max()+1])
    for item in h:
        I[item[0],item[1]] += 1

    I[I == I.max()] = 0
    plt.imshow(I)
    plt.show()