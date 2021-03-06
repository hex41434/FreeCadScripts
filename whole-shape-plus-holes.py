################################## 
# Type in the dimensions here
# e.g. 4x8 wall would be
# hFeet = float(8)
# wFeet = float(4)
# tFeet = float(0.5)

hFeet = float(8)
wFeet = float(4)
tFeet = float(0.5)
scale = float(1.0/20)
horizontalMagnets = 8
verticalMagnets = 16


hInches = float(hFeet*12*scale)
wInches = float(wFeet*12*scale)
tInches = float(tFeet*12*scale)

magnetRadiusMM = 3.175
magnetThicknessMM = 3.175

##################################

hMM = float(hInches*25.4)
wMM = float(wInches*25.4)
tMM = float(tInches*25.4)


App.activeDocument().addObject('Sketcher::SketchObject','Sketch')
App.activeDocument().Sketch.Placement = App.Placement(App.Vector(0.000000,0.000000,0.000000),App.Rotation(0.000000,0.000000,0.000000,1.000000))
Gui.activeDocument().activeView().setCamera('#Inventor V2.1 ascii \n OrthographicCamera {\n viewportMapping ADJUST_CAMERA \n position 0 0 87 \n orientation 0 0 1  0 \n nearDistance -112.88701 \n farDistance 287.28702 \n aspectRatio 1 \n focalDistance 87 \n height 143.52005 }')
Gui.activeDocument().setEdit('Sketch')
App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(0.000000,0.000000,0),App.Vector(wMM,0.000000,0)))
App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(wMM,0.000000,0),App.Vector(wMM,hMM,0)))
App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(wMM,hMM,0),App.Vector(0.000000,hMM,0)))
App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(0.000000,hMM,0),App.Vector(0.000000,0.000000,0)))
App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',0,2,1,1)) 
App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',1,2,2,1)) 
App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',2,2,3,1)) 
App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',3,2,0,1)) 
App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Horizontal',0)) 
App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Horizontal',2)) 
App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Vertical',1)) 
App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Vertical',3)) 
App.ActiveDocument.recompute()
App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',0,1,-1,1)) 
App.ActiveDocument.recompute()
Gui.activeDocument().resetEdit()
App.activeDocument().recompute()
App.activeDocument().addObject("PartDesign::Pad","Pad")
App.activeDocument().Pad.Sketch = App.activeDocument().Sketch
App.activeDocument().Pad.Length = 10.0
App.ActiveDocument.recompute()
Gui.activeDocument().hide("Sketch")
Gui.activeDocument().setEdit('Pad',0)
App.ActiveDocument.Pad.Length = float(tMM/2)
App.ActiveDocument.Pad.Reversed = 0
App.ActiveDocument.Pad.Midplane = 0
App.ActiveDocument.Pad.Length2 = 100.000054
App.ActiveDocument.Pad.Type = 0
App.ActiveDocument.Pad.UpToFace = None
App.ActiveDocument.recompute()
Gui.activeDocument().resetEdit()


App.activeDocument().addObject('Sketcher::SketchObject','Sketch001')
App.activeDocument().Sketch001.Support = (App.ActiveDocument.Pad,["Face6"])
App.activeDocument().recompute()
Gui.activeDocument().setEdit('Sketch001')


def addCircle():
	App.ActiveDocument.Sketch001.addGeometry(Part.Circle(App.Vector(x,y,0),App.Vector(0,0,1),float(magnetRadiusMM)))
	App.ActiveDocument.recompute()
	pass

offset = (tMM-(2*magnetRadiusMM))/2

x = magnetRadiusMM + offset
y = magnetRadiusMM + offset
yStart = y

def getCondtions():

	global xCondition
	global yCondition
	global yChange
	global xChange

	if x > 0:
		xCondition = "x < " + str(wMM)
		xChange    = "x + " + str(float(wMM/horizontalMagnets))
	else:
		xCondition = "x >- " + str(wMM)
		xChange    = "x - " + str(float(wMM/horizontalMagnets))
		pass

	if y > 0:
		yCondition = "y < " + str(hMM-7)
		yChange    = "y + " + str(float(hMM/verticalMagnets))
	else:
		yCondition = "y >-" + str(hMM-7)
		yChange    = "y - " + str(float(hMM/verticalMagnets))
		pass
	pass


getCondtions()

while eval(xCondition):
	addCircle()
	while eval(yCondition):
		y = eval(yChange)
		addCircle()
		pass
	x = eval(xChange)
 	y = yStart
 	getCondtions()
	pass

Gui.activeDocument().resetEdit()
App.activeDocument().recompute()
App.activeDocument().addObject("PartDesign::Pocket","Pocket")
App.activeDocument().Pocket.Sketch = App.activeDocument().Sketch001
App.activeDocument().Pocket.Length = 5.0
App.ActiveDocument.recompute()
Gui.activeDocument().hide("Sketch001")
Gui.activeDocument().hide("Pad")
Gui.activeDocument().setEdit('Pocket')
Gui.ActiveDocument.Pocket.ShapeColor=Gui.ActiveDocument.Pad.ShapeColor
Gui.ActiveDocument.Pocket.LineColor=Gui.ActiveDocument.Pad.LineColor
Gui.ActiveDocument.Pocket.PointColor=Gui.ActiveDocument.Pad.PointColor
App.ActiveDocument.Pocket.Length = float(magnetThicknessMM/2)
App.ActiveDocument.Pocket.Type = 0
App.ActiveDocument.Pocket.UpToFace = None
App.ActiveDocument.recompute()
Gui.activeDocument().resetEdit()



App.activeDocument().addObject('Sketcher::SketchObject','Sketch002')
App.activeDocument().Sketch002.Support = (App.ActiveDocument.Pocket,["Face5"])
App.activeDocument().recompute()
Gui.activeDocument().setEdit('Sketch002')




x = magnetThicknessMM/2+offset
y = float(magnetRadiusMM+offset)

while y < hMM:
	lx = x - float(magnetThicknessMM/2)
	rx = x + float(magnetThicknessMM/2)
	ty = y + float(magnetRadiusMM)
	by = y - float(magnetRadiusMM)
	App.ActiveDocument.Sketch002.addGeometry(Part.Line(App.Vector(lx,ty,0),App.Vector(rx,ty,0)))
	App.ActiveDocument.Sketch002.addGeometry(Part.Line(App.Vector(lx,by,0),App.Vector(rx,by,0)))
	App.ActiveDocument.Sketch002.addGeometry(Part.Line(App.Vector(lx,ty,0),App.Vector(lx,by,0)))
	App.ActiveDocument.Sketch002.addGeometry(Part.Line(App.Vector(rx,ty,0),App.Vector(rx,by,0)))
	y = y + float(hMM/verticalMagnets)
	pass

x = wMM-magnetThicknessMM/2-offset
y = float(magnetRadiusMM+offset)

while y < hMM:
	lx = x - float(magnetThicknessMM/2)
	rx = x + float(magnetThicknessMM/2)
	ty = y + float(magnetRadiusMM)
	by = y - float(magnetRadiusMM)
	App.ActiveDocument.Sketch002.addGeometry(Part.Line(App.Vector(lx,ty,0),App.Vector(rx,ty,0)))
	App.ActiveDocument.Sketch002.addGeometry(Part.Line(App.Vector(lx,by,0),App.Vector(rx,by,0)))
	App.ActiveDocument.Sketch002.addGeometry(Part.Line(App.Vector(lx,ty,0),App.Vector(lx,by,0)))
	App.ActiveDocument.Sketch002.addGeometry(Part.Line(App.Vector(rx,ty,0),App.Vector(rx,by,0)))
	y = y + float(hMM/verticalMagnets)
	pass

Gui.activeDocument().resetEdit()
App.activeDocument().recompute()
App.activeDocument().addObject("PartDesign::Pocket","Pocket001")
App.activeDocument().Pocket001.Sketch = App.activeDocument().Sketch002
App.activeDocument().Pocket001.Length = 5.0
App.ActiveDocument.recompute()
Gui.activeDocument().hide("Sketch002")
Gui.activeDocument().hide("Pocket")
Gui.activeDocument().setEdit('Pocket001')
Gui.ActiveDocument.Pocket001.ShapeColor=Gui.ActiveDocument.Pocket.ShapeColor
Gui.ActiveDocument.Pocket001.LineColor=Gui.ActiveDocument.Pocket.LineColor
Gui.ActiveDocument.Pocket001.PointColor=Gui.ActiveDocument.Pocket.PointColor
App.ActiveDocument.Pocket001.Length = float(magnetRadiusMM)
App.ActiveDocument.Pocket001.Type = 0
App.ActiveDocument.Pocket001.UpToFace = None
App.ActiveDocument.recompute()
Gui.activeDocument().resetEdit()




App.activeDocument().addObject('Sketcher::SketchObject','Sketch003')
App.activeDocument().Sketch003.Support = (App.ActiveDocument.Pocket001,["Face5"])
App.activeDocument().recompute()
Gui.activeDocument().setEdit('Sketch003')




x = magnetRadiusMM + offset
y = magnetThicknessMM/2+offset

while x < wMM:
	lx = x - float(magnetRadiusMM)
	rx = x + float(magnetRadiusMM)
	ty = y + float(magnetThicknessMM/2)
	by = y - float(magnetThicknessMM/2)
	App.ActiveDocument.Sketch003.addGeometry(Part.Line(App.Vector(lx,ty,0),App.Vector(rx,ty,0)))
	App.ActiveDocument.Sketch003.addGeometry(Part.Line(App.Vector(lx,by,0),App.Vector(rx,by,0)))
	App.ActiveDocument.Sketch003.addGeometry(Part.Line(App.Vector(lx,ty,0),App.Vector(lx,by,0)))
	App.ActiveDocument.Sketch003.addGeometry(Part.Line(App.Vector(rx,ty,0),App.Vector(rx,by,0)))
	x = x + float(wMM/horizontalMagnets)
	pass

x = magnetRadiusMM + offset
y = hMM - magnetThicknessMM/2 - offset

while x < wMM:
	lx = x - float(magnetRadiusMM)
	rx = x + float(magnetRadiusMM)
	ty = y + float(magnetThicknessMM/2)
	by = y - float(magnetThicknessMM/2)
	App.ActiveDocument.Sketch003.addGeometry(Part.Line(App.Vector(lx,ty,0),App.Vector(rx,ty,0)))
	App.ActiveDocument.Sketch003.addGeometry(Part.Line(App.Vector(lx,by,0),App.Vector(rx,by,0)))
	App.ActiveDocument.Sketch003.addGeometry(Part.Line(App.Vector(lx,ty,0),App.Vector(lx,by,0)))
	App.ActiveDocument.Sketch003.addGeometry(Part.Line(App.Vector(rx,ty,0),App.Vector(rx,by,0)))
	x = x + float(wMM/horizontalMagnets)
	pass

Gui.activeDocument().resetEdit()
App.activeDocument().recompute()
App.activeDocument().addObject("PartDesign::Pocket","Pocket002")
App.activeDocument().Pocket002.Sketch = App.activeDocument().Sketch003
App.activeDocument().Pocket002.Length = 5.0
App.ActiveDocument.recompute()
Gui.activeDocument().hide("Sketch003")
Gui.activeDocument().hide("Pocket001")
Gui.activeDocument().setEdit('Pocket002')
Gui.ActiveDocument.Pocket002.ShapeColor=Gui.ActiveDocument.Pocket001.ShapeColor
Gui.ActiveDocument.Pocket002.LineColor=Gui.ActiveDocument.Pocket001.LineColor
Gui.ActiveDocument.Pocket002.PointColor=Gui.ActiveDocument.Pocket001.PointColor
App.ActiveDocument.Pocket002.Length = float(magnetRadiusMM)
App.ActiveDocument.Pocket002.Type = 0
App.ActiveDocument.Pocket002.UpToFace = None
App.ActiveDocument.recompute()
Gui.activeDocument().resetEdit()

