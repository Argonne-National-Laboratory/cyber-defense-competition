import WTCShapes as wtcsh

PIPE_COLOR = '#759FFF'
PIPE_COLOR_OFFLINE = '#FF0616'
PIPE_COLOR_WASTE = '#FFD249'
PUMPING_STATION_COLOR = '#BAD473'
TREATMENT_FACILITY_COLOR = '#658CD4'
DISTRIBUTION_NETWORK_COLOR = '#C8D455'
MOTOR_COLOR_1 = '#A2A69E'
MOTOR_COLOR_2 = '#9AFF15'
MOTOR_COLOR_3 = '#FF0D4D'
MOTOR_COLOR_4 = '#FCFFC9'
VALVE_COLOR_1 = '#FFFFFF'
TANK_BACKGROUND_COLOR = '#FFFFFF'
TANK_FILL_COLOR = '#A4E7FF'
FILTRATION_FILL_COLOR = '#525478'
AUTOMATED_VALVE = '#82FF14'
AUTOMATED_VALVE_OFFLINE = '#FF0814'
LINE_COLOR = '#32A8DA'
FILTER_TANKS = '#54565E'

class Tank:
	def __init__(self,  pos=(0,0), operational=True):
		self.pos = pos
		self.operational = operational
		self.y1 = 15
		self.y2 = 7
		self.x1 = 5
		self.x2 = 50
		self.x3 = self.x2 + self.x1
		self.ty = self.y1 + 15

	def Draw(self, canvas):
		self.points = ((self.pos[0], self.pos[1]+self.y2), (self.pos[0], self.pos[1]),
                            (self.pos[0]+self.x1, self.pos[1]-self.y1),
                            (self.pos[0]+self.x2, self.pos[1]-self.y1),
                            (self.pos[0]+self.x3, self.pos[1]), (self.pos[0]+self.x3, self.pos[1]+self.y2),
                            (self.pos[0]+self.x2, self.pos[1]+(self.y1+self.y2)),
                            (self.pos[0]+self.x1, self.pos[1]+self.y1+self.y2))
		self.tank_outline = canvas.AddPolygon(self.points, FillColor=TANK_BACKGROUND_COLOR)

		self.CreateFillLines(canvas)
		self.status = self.fill0

	def CreateFillLines(self, canvas):
		self.fill0 = canvas.AddPolygon(self.points, FillColor=TANK_BACKGROUND_COLOR, InForeground=True)
		self.fill0.Hide()

		fill1_pts = ((self.pos[0], self.pos[1]), (self.pos[0] + self.x3, self.pos[1]), (self.pos[0]+self.x2, self.pos[1] - self.y1), (self.pos[0] + self.x1, self.pos[1]-self.y1))
		self.fill1 = canvas.AddPolygon(fill1_pts, FillColor = TANK_FILL_COLOR, InForeground=True)
		self.fill1.Hide()

		fill2_pts = ((self.pos[0], self.pos[1]), (self.pos[0], self.pos[1] + self.y2), (self.pos[0]+self.x3, self.pos[1] + self.y2),
                      (self.pos[0] + self.x3, self.pos[1]), (self.pos[0]+self.x2, self.pos[1] - self.y1), (self.pos[0] + self.x1, self.pos[1]-self.y1) )
		self.fill2 = canvas.AddPolygon(fill2_pts, FillColor = TANK_FILL_COLOR, InForeground=True)
		self.fill2.Hide()

		fill3_pts = ((self.pos[0], self.pos[1]+self.y2), (self.pos[0], self.pos[1]),
                            (self.pos[0]+self.x1, self.pos[1]-self.y1),
                            (self.pos[0]+self.x2, self.pos[1]-self.y1),
                            (self.pos[0]+self.x3, self.pos[1]), (self.pos[0]+self.x3, self.pos[1]+self.y2),
                            (self.pos[0]+self.x2, self.pos[1]+self.y1+self.y2),
                            (self.pos[0]+self.x1, self.pos[1]+self.y1+self.y2))
		self.fill3 = canvas.AddPolygon(fill3_pts, FillColor = TANK_FILL_COLOR, InForeground=True)
		self.fill3.Hide()

	def UpdateTank(self):
		self.status.Hide()
		if self.fill_value >= 8:
			self.status = self.fill3
		elif self.fill_value >= 5:
			self.status = self.fill2
		elif self.fill_value >= 3:
			self.status = self.fill1
		else:
			self.status = self.fill0		
		self.status.Show()

	def UpdateTankFill(self, value):
		self.fill_value = value
		self.UpdateTank()

class Filtration:
	def __init__(self, pos=(0,0), operational=True):
		self.pos = pos
		self.operational = operational
		self.x1 = 20
		self.x2 = 40
		self.y1 = 40
		self.y2 = 50
		self.tx = 8
		self.ty = 6

	def Draw(self, canvas):
		self.points = ((self.pos[0], self.pos[1]), (self.pos[0]+self.x2, self.pos[1]), (self.pos[0]+self.x2, self.pos[1]-self.y1),
                            (self.pos[0]+self.x1, self.pos[1]-self.y2), (self.pos[0], self.pos[1]-self.y1))
		canvas.AddPolygon(self.points, FillColor=TANK_BACKGROUND_COLOR)
		self.filtration_online = canvas.AddPolygon(self.points, FillColor=FILTRATION_FILL_COLOR)

class Valve:
	def __init__(self, pos=(0,0)):
		self.pos = pos
		self.y1 = 2
		self.y2 = 4
		self.x1 = 2
		self.x2 = 4

	def Draw(self, canvas):
		Canvas = canvas
		self.points = ((self.pos[0], self.pos[1]), (self.pos[0], self.pos[1]-self.y2),
                            (self.pos[0]+self.x1, self.pos[1]-self.y1),
                            (self.pos[0]+self.x2, self.pos[1]), (self.pos[0]+self.x2, self.pos[1]-self.y2),
                            (self.pos[0],self.pos[1]))
		Canvas.AddPolygon(self.points, FillColor=VALVE_COLOR_1)

class Pump:
	def __init__(self, pos=(0,0), state=None, diameter=8, pump_number=0, name=''):
		self.pos = pos
		self.state = state
		self.diameter = diameter
		self.inner_diameter = self.diameter/2
		self.inner_circle_pos = (self.pos[0]+self.inner_diameter/(self.diameter), self.pos[1]-self.inner_diameter/(self.diameter))
		self.feet = self.diameter/2
		self.pump_number = pump_number
		self.name = name
		self.dirty = False

	def Draw(self, canvas):
		Canvas = canvas
		self.feet_points = ((self.pos[0]-self.feet, self.pos[1]-self.feet), (self.pos[0], self.pos[1]), (self.pos[0]+self.feet, self.pos[1]-self.feet))
		Canvas.AddPolygon(self.feet_points, FillColor=MOTOR_COLOR_1)
		self.pump = Canvas.AddCircle((self.pos[0], self.pos[1]), self.diameter, FillColor=MOTOR_COLOR_1, InForeground=True)
		setattr(self.pump, 'masterTag', self.name)
		setattr(self.pump, 'parent', self)
		self.op_static = Canvas.AddCircle((self.inner_circle_pos[0], self.inner_circle_pos[1]), self.inner_diameter, FillColor=MOTOR_COLOR_4, InForeground=True)
		self.op_bad = Canvas.AddCircle((self.inner_circle_pos[0], self.inner_circle_pos[1]), self.inner_diameter, FillColor=MOTOR_COLOR_3, InForeground=True)
		self.op_good = Canvas.AddCircle((self.inner_circle_pos[0], self.inner_circle_pos[1]), self.inner_diameter, FillColor=MOTOR_COLOR_2, InForeground=True)
		self.op_bad.Visible = False
		self.op_good.Visible = False
		self.status = self.op_good

	def Online(self):
		self.status.Visible = False
		self.status = self.op_good

	def Offline(self):
		self.status.Visible = False
		self.status = self.op_bad

class Pipe:
	def __init__(self, pos=(0,0), length=30, width=2, horizontal=True):
		self.pos = pos
		self.width = width
		self.length = length
		self.horizontal = horizontal
		self.state = None

	def Draw(self, canvas):
		if self.horizontal == True:
			wh = (self.length, self.width)
		else:
			wh = (self.width, -self.length)
		self.on_pipe = canvas.AddRectangle(self.pos, wh, FillColor=PIPE_COLOR, LineStyle='Transparent', InForeground=True)
		canvas.AddRectangle(self.pos, wh, FillColor=PIPE_COLOR_OFFLINE, LineStyle='Transparent')

	def Offline(self):
		self.on_pipe.Visible = False

	def Online(self):
		self.on_pipe.Visible = True


class ClarificationTank:
	def __init__(self, pos=(0,0), operational=True):
		self.pos = pos
		self.operational = operational
		self.x1 = 20
		self.x2 = 40
		self.y1 = 10
		self.y2 = 80
		self.tx = 6
		self.ty = 12 + self.y2

	def Draw(self, canvas):
		self.points = ((self.pos[0], self.pos[1]), (self.pos[0]+self.x1, self.pos[1]+self.y1), (self.pos[0]+self.x2, self.pos[1]),
                        (self.pos[0]+self.x2, self.pos[1]-self.y2), (self.pos[0] + self.x1, self.pos[1]-self.y2-self.y1), (self.pos[0], self.pos[1]-self.y2))
		self.clarification_outline = canvas.AddPolygon(self.points, FillColor=TANK_BACKGROUND_COLOR)
		self.clarification_tank_online = canvas.AddPolygon(self.points, FillColor=TANK_FILL_COLOR)

class AutomatedValve:
	def __init__(self, pos=(0,0), name='', state=False):
		self.pos = pos
		self.wh = (5,5)
		self.name = name
		self.state = state
		self.dirty = False

	def Draw(self, canvas):
		self.valve = canvas.AddRectangle(self.pos, self.wh, FillColor=AUTOMATED_VALVE, LineStyle='Transparent', InForeground=True)
		setattr(self.valve, 'masterTag', self.name)
		setattr(self.valve, 'parent', self)
		self.offline = canvas.AddRectangle(self.pos, self.wh, FillColor="PINK", LineStyle='Transparent', InForeground=True)
		self.offline.Visible = False

	def Online(self):
		self.offline.Visible = False

	def Offline(self):
		self.offline.Visible = True
