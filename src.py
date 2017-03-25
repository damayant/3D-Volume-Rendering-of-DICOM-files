import vtk
dir_ = r"CT"

# Read data
reader = vtk.vtkDICOMImageReader()
reader.SetDirectoryName(dir_)
reader.Update()

renWin = vtk.vtkRenderWindow()
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)


# Create colour transfer function
colorFunc = vtk.vtkColorTransferFunction()
colorFunc.AddRGBPoint(-3024, 0.0, 0.0, 0.0)
colorFunc.AddRGBPoint(-77, 0.54902, 0.25098, 0.14902)
colorFunc.AddRGBPoint(94, 0.882353, 0.603922, 0.290196)
colorFunc.AddRGBPoint(179, 1, 0.937033, 0.954531)
colorFunc.AddRGBPoint(260, 0.615686, 0, 0)
colorFunc.AddRGBPoint(3071, 0.827451, 0.658824, 1)

# Create opacity transfer function
alphaChannelFunc = vtk.vtkPiecewiseFunction()
alphaChannelFunc.AddPoint(-3024, 0.0)
alphaChannelFunc.AddPoint(-77, 0.0)
alphaChannelFunc.AddPoint(94, 0.29)
alphaChannelFunc.AddPoint(179, 0.55)
alphaChannelFunc.AddPoint(260, 0.84)
alphaChannelFunc.AddPoint(3071, 0.875)

# Instantiate necessary classes and create VTK pipeline
volume = vtk.vtkVolume()
ren = vtk.vtkRenderer()
ren.SetViewport(0,0,0.6,1)
ren.SetBackground(0.1,0.2,0.4)



ren.AddVolume(volume)

RGB_tuples = [(1, 0, 0), (0, 1, 0), (0, 0, 1)] # define colors for plane outline


# Define volume mapper
volumeMapper = vtk.vtkSmartVolumeMapper()  
volumeMapper.SetInputConnection(reader.GetOutputPort())

# Define volume properties
volumeProperty = vtk.vtkVolumeProperty()
volumeProperty.SetScalarOpacity(alphaChannelFunc)
volumeProperty.SetColor(colorFunc)
volumeProperty.ShadeOn()

# Set the mapper and volume properties
volume.SetMapper(volumeMapper)
volume.SetProperty(volumeProperty)
volume.Update()

renWin.AddRenderer(ren)
renWin.Render()



mapToColors = vtk.vtkImageMapToColors()
mapToColors.SetInputConnection(reader.GetOutputPort(0))
#mapToColors.SetLookupTable(table)
mapToColors.Update()

# A picker is used to get information about the volume
picker = vtk.vtkCellPicker()
picker.SetTolerance(0.005)

# Define plane widget
planeWidgetX = vtk.vtkImagePlaneWidget() 

 

# Set plane properties

planeWidgetX.SetInputConnection(mapToColors.GetOutputPort(0))
planeWidgetX.SetPlaneOrientation(0)
planeWidgetX.DisplayTextOn()
planeWidgetX.SetSliceIndex(100)
planeWidgetX.SetPicker(picker)
#planeWidgetX.SetLookupTable(table)
planeWidgetX.SetColorMap(mapToColors)
planeWidgetX.SetKeyPressActivationValue("x")
planeWidgetX.GetPlaneProperty().SetColor(RGB_tuples[0])



# Place plane widget and set interactor

planeWidgetX.SetCurrentRenderer(ren)
planeWidgetX.SetInteractor(iren)
planeWidgetX.PlaceWidget()
planeWidgetX.On()


#code for sliced portion
image = planeWidgetX.GetResliceOutput()
image.Modified()

actor = vtk.vtkImageActor()
actor.GetMapper().SetInputData(image) 
actor.Update()

# Place plane widget and set interactor

 

# Add the volume to the renderer
ren2 = vtk.vtkRenderer()
ren2.SetBackground(0,0,0)



ren2.AddActor(actor)
ren2.SetViewport(0.6,0.5,1,1)
ren2.ResetCamera()



renWin.AddRenderer(ren2)

renWin.Render()
plot = vtk.vtkXYPlotActor()
ren3 = vtk.vtkRenderer()
ren3.SetViewport(0.6,0,1,0.5)
ren3.SetBackground(0,0,0)
renWin.AddRenderer(ren3)
renWin.Render()

histogram = vtk.vtkImageAccumulate()
histogram.AddInputData(image)
(x,y)=image.GetScalarRange()


print x
print y 


histogram.SetComponentExtent(int(x),int(y),0,0,0,0);
histogram.SetInputData(image)
histogram.Modified()


plot.AddDataSetInputConnection(histogram.GetOutputPort(0))
ren3.AddActor(plot)
ren3.ResetCamera()
renWin.AddRenderer(ren3)
renWin.Render()
#renderer3 ## Problem with viewport Position
renWin.SetSize(800,800)

# Render the scene

renWin.Render()

#converting to jpeg file format
w2if = vtk.vtkWindowToImageFilter()
w2if.SetInput(renWin)
w2if.Update()
 
writer = vtk.vtkJPEGWriter()
writer.SetFileName("assignment3.jpeg")
writer.SetInputConnection(w2if.GetOutputPort())
writer.Write()
#renWin.Modified()
iren.Initialize()
iren.Start()


