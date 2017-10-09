import WTCControls_basic as wtc
import WTCShapes as wtcsh
import wx
import Process
	
class GenericHMIObject:
	def __init__(self, name, masterTag):
		self.masterTag = masterTag
		self.name = name
		self.assets = []
		self.objects = []
		self.state = True
		self.dirty = False

	def ReturnAsset(self, name):
		for index,obj in enumerate(self.assets):
			if obj.name == name:
				return obj
	
	def AddObject(self, obj, canvas, masterTag=None, append=True):
		if append:
			self.objects.append(obj)
		setattr(obj, 'parent', self)
		if masterTag:
			setattr(obj, 'masterTag', masterTag)
		if hasattr(obj, 'Draw'):
			obj.Draw(canvas)

	def Online(self):
		for index,obj in enumerate(self.assets):
			if obj.Online():
				self._Online()
				self.state = True
			else:
				self.Offline()
				self.state = False

	def _Online(self):
		for index,obj in enumerate(self.objects):
			obj.Online()

	def Offline(self):
		for index,obj in enumerate(self.objects):
			obj.Offline()
			
	def ReturnState(self):
		return self.state

class ChemicalTank(GenericHMIObject):
	def __init__(self, canvas, pos, name='', masterTag=None, operational=True):
		GenericHMIObject.__init__(self, name, masterTag)
		self.operational = operational
		self.pos = pos
		self.label = canvas.AddScaledTextBox(self.name,
											  self.pos,
											  wtcsh.TEXT_SCALE,
											  Width=20,
											  Color = wtcsh.LABEL_FONT_COLOR,
											  BackgroundColor = wtcsh.LABEL_BACKGROUND,
											  LineColor= wtcsh.LABEL_OUTLINE_COLOR,
											  PadSize = 2,
											  Position = 'tl',
											  Alignment='center')
		self.AddObject(self.label, canvas, masterTag, False)
		((x,y), (w,h)) = self.label.GetBoxRect()
		self.pipe = wtc.Pipe((self.pos[0]+w/2, self.pos[1]-h), width=1, length=5, horizontal=False)
		self.AddObject(self.pipe, canvas)
		self.valve = wtc.AutomatedValve((self.pos[0]+w/3+2, self.pos[1]-h-5*2))
		self.AddObject(self.valve, canvas)
		

class PumpPipeNetwork(GenericHMIObject):
	def __init__(self, name='', masterTag=None):
		GenericHMIObject.__init__(self, name, masterTag)
		self.objects = []

	def ReturnPump(self):
		for index,obj in enumerate(self.objects):
			if isinstance(obj, wtc.Pump):
				return obj
		return None

	def ReturnValves(self):
		valves = []
		for index,obj in enumerate(self.objects):
			if isinstance(obj, wtc.AutomatedValve):
				valves.append(obj)
		return valves



class FlocculationBasin:
	def __init__(self, pos, canvas, name='Flocculation Basin', operational=True):
		self.name = name
		self.operational = operational
		self.pos = pos

		self.height = 30
		self.width = 40

		canvas.AddRectangle(self.pos, (self.width, self.height), FillColor=wtc.TANK_BACKGROUND_COLOR)
		canvas.AddRectangle((self.pos[0]+self.width, self.pos[1]), (self.width/2, self.height), FillColor=wtc.TANK_BACKGROUND_COLOR)
		canvas.AddLine(((self.pos[0] + self.width/3, self.pos[1]+self.height), (self.pos[0] + self.width/3, self.pos[1]+self.height/2)))
		canvas.AddLine(((self.pos[0] + self.width/3*2, self.pos[1]), (self.pos[0] + self.width/3*2, self.pos[1]+self.height/2)))
		canvas.AddScaledBitmap(wx.Bitmap('rsrc/icons/civil_vertical_propeller.png'), (self.pos[0] + self.width/12, self.pos[1] + self.height), Height=6, Position='tl')
		canvas.AddScaledBitmap(wx.Bitmap('rsrc/icons/civil_vertical_propeller.png'), (self.pos[0] + self.width/12*5, self.pos[1] + self.height), Height=6, Position='tl')
		canvas.AddScaledBitmap(wx.Bitmap('rsrc/icons/civil_vertical_propeller.png'), (self.pos[0] + self.width/12*9, self.pos[1] + self.height), Height=6, Position='tl')
		canvas.AddScaledBitmap(wx.Bitmap('rsrc/icons/pnuemv.png'), (self.pos[0] + self.width + self.width/6, self.pos[1] + self.height - self.height/3), Height=6, Position='tl')
		canvas.AddScaledTextBox(self.name,
											  ((self.pos[0] + self.width/3+2), self.pos[1]-self.height/20),
											  wtcsh.TEXT_SCALE,
											  Color = wtcsh.DYNLABEL_FONT_COLOR,
											  BackgroundColor = wtcsh.DYNLABEL_BACKGROUND,
											  LineColor= wtcsh.DYNLABEL_OUTLINE_COLOR,
											  PadSize = 3,
											  Position = 'tl',
											  Alignment='center')
		canvas.AddRectangle((self.pos[0] + self.width + self.width/4, self.pos[1] + self.height), (1, 50), FillColor=wtc.PIPE_COLOR_WASTE, LineStyle='Transparent')
		canvas.AddScaledTextBox('REPROCESSING',
											  (self.pos[0] + self.width-1, self.pos[1] + self.height + 50),
											  wtcsh.TEXT_SCALE,
											  Color = wtcsh.DYNLABEL_FONT_COLOR,
											  BackgroundColor = wtcsh.DYNLABEL_BACKGROUND,
											  LineColor= wtcsh.DYNLABEL_OUTLINE_COLOR,
											  PadSize = 3,
											  Position = 'tl',
											  Alignment='center')

class OzoneContractor(GenericHMIObject):
	def __init__(self, pos, canvas, name='Ozone\nContractor', masterTag=None, operational=True):
		GenericHMIObject.__init__(self, name, masterTag)
		self.operational = operational
		self.pos = pos
		self.height = 20
		self.width = 20

		self.tank = ChemicalTank(canvas, (pos[0],pos[1]+2*self.height), 'Sodium\nBisulphate', masterTag=masterTag[0])
		canvas.AddRectangle(self.pos, (self.width, self.height), FillColor=wtc.TANK_BACKGROUND_COLOR)
		canvas.AddScaledTextBox(self.name,
											  (self.pos[0], self.pos[1]+self.height-self.height/4),
											  wtcsh.TEXT_SCALE,
											  Color = wtcsh.DYNLABEL_FONT_COLOR,
											  BackgroundColor = wtcsh.DYNLABEL_BACKGROUND,
											  LineColor= wtcsh.DYNLABEL_OUTLINE_COLOR,
											  Width=20,
											  PadSize = 2,
											  Position = 'tl',
											  Alignment='center')
		self.dev = canvas.AddCircle((self.pos[0], self.pos[1]-self.height/5), 12, FillColor=wtc.AUTOMATED_VALVE, InForeground=True)
		self.AddObject(self.dev, canvas, masterTag[1])
		canvas.AddScaledBitmap(wx.Bitmap('rsrc/icons/storagesphere.png'), (self.pos[0]-3, self.pos[1]-1), Height=6, Position='tl', InForeground=True)

#FIXME 		
	def Online(self):
		if self.assets[0].Online():
			self.objects[0].SetFillColor(wtc.AUTOMATED_VALVE)
		else:
			self.objects[0].SetFillColor("RED")

class FilterTanks:
	def __init__(self, pos, canvas, name='Filter Tanks', operational=True):
		self.name = name
		self.operational = operational
		self.pos = pos
		self.height = 30
		self.width = 60

		canvas.AddRectangle(self.pos, (self.width, self.height), FillColor=wtc.TANK_BACKGROUND_COLOR)
		for i in range(0, 60, 10):
			canvas.AddRectangle((self.pos[0]+i,self.pos[1]), (3, self.height), FillColor=wtc.FILTER_TANKS)
		canvas.AddScaledTextBox(self.name,
											  (self.pos[0]+self.width/2, self.pos[1]+self.height/2),
											  wtcsh.TEXT_SCALE,
											  Color = wtcsh.DYNLABEL_FONT_COLOR,
											  BackgroundColor = wtcsh.DYNLABEL_BACKGROUND,
											  LineColor= wtcsh.DYNLABEL_OUTLINE_COLOR,
											  Width=20,
											  PadSize = 2,
											  Position = 'cc',
											  Alignment='center')
		canvas.AddRectangle((self.pos[0] + self.width/2, self.pos[1] - 10), (1, 10), FillColor=wtc.PIPE_COLOR_WASTE, LineStyle='Transparent')
		canvas.AddRectangle((self.pos[0] + self.width/2, self.pos[1] - 10), (100, 1), FillColor=wtc.PIPE_COLOR_WASTE, LineStyle='Transparent')
		canvas.AddScaledTextBox('REPROCESSING',
											  (self.pos[0] + self.width + 75, self.pos[1] - 9),
											  wtcsh.TEXT_SCALE,
											  Color = wtcsh.DYNLABEL_FONT_COLOR,
											  BackgroundColor = wtcsh.DYNLABEL_BACKGROUND,
											  LineColor= wtcsh.DYNLABEL_OUTLINE_COLOR,
											  PadSize = 3,
											  Position = 'cc',
											  Alignment='center')

class ChlorineChamber(GenericHMIObject):
	def __init__(self, pos, canvas, name='Chlorine\nContact\nChamber', masterTag=None, operational=True):
		GenericHMIObject.__init__(self, name, masterTag)
		self.operational = operational
		self.pos = pos

		self.tank = wtc.Tank(self.pos)
		self.tank.Draw(canvas)
		self.chlor = ChemicalTank(canvas, (self.pos[0]+6, self.pos[1]+self.tank.y1+self.tank.y2+20), name='Chlorine\n', masterTag=masterTag[0])
		self.sodium = ChemicalTank(canvas, (self.pos[0]+(self.tank.x1+self.tank.x2)/2, self.pos[1]+self.tank.y1+self.tank.y2+20), name='Sodium\nHydroxide', masterTag=masterTag[1])
		self.objects.append(self.chlor)
		self.objects.append(self.sodium)

class ClearWell:
	def __init__(self, pos, canvas, name='Clearwell', operational=True):
		self.name = name
		self.operational = operational
		self.pos = pos

		self.height = 20
		self.width = 40

		canvas.AddRectangle((self.pos), (self.width, self.height), FillColor=wtc.TANK_BACKGROUND_COLOR, InForeground=True)
		canvas.AddScaledTextBox(self.name,
											  (self.pos[0]+self.width/2, self.pos[1]+self.height/2),
											  wtcsh.TEXT_SCALE,
											  Color = wtcsh.DYNLABEL_FONT_COLOR,
											  BackgroundColor = wtcsh.DYNLABEL_BACKGROUND,
											  LineColor= wtcsh.DYNLABEL_OUTLINE_COLOR,
											  Width=20,
											  PadSize = 2,
											  Position = 'cc',
											  Alignment='center', InForeground=True)

class UVChambers(GenericHMIObject):
	def __init__(self, pos, canvas, name='', masterTag=None):
		GenericHMIObject.__init__(self, name, masterTag)
		self.pos = pos
		self.height = 10
		self.width = 40
		self.space = 15
		self.uv = []
		self.canvas = canvas
		
		self.uv.append(canvas.AddEllipse(self.pos, (self.width, self.height), FillColor="PINK", InForeground=True))
		self.uv0 = canvas.AddScaledBitmap(wx.Bitmap('rsrc/icons/Blacklight.png'), (self.pos[0] + self.width/2, self.pos[1] + self.height/2), Height=6, Position='cc', InForeground=True)
		
		self.uv.append(canvas.AddEllipse((self.pos[0], self.pos[1]-self.space), (self.width, self.height), FillColor="PINK", InForeground=True))
		self.uv1 = canvas.AddScaledBitmap(wx.Bitmap('rsrc/icons/Blacklight.png'), (self.pos[0] + self.width/2, self.pos[1] + self.height/2-self.space), Height=6, Position='cc', InForeground=True)
	
		self.uv.append(canvas.AddEllipse((self.pos[0], self.pos[1]-self.space*2), (self.width, self.height), FillColor="PINK", InForeground=True))
		self.uv2 = canvas.AddScaledBitmap(wx.Bitmap('rsrc/icons/Blacklight.png'), (self.pos[0] + self.width/2, self.pos[1] + self.height/2-self.space*2), Height=6, Position='cc', InForeground=True)
		
		self.AddObject(self.uv0, canvas, masterTag[0])
		self.AddObject(self.uv1, canvas, masterTag[1])
		self.AddObject(self.uv2, canvas, masterTag[2])


	def Online(self):
		for i in range(3):
			if self.assets[i].Online():
				self.uv[i].SetFillColor('Purple')
			else:
				self.uv[i].SetFillColor('Yellow')
		
