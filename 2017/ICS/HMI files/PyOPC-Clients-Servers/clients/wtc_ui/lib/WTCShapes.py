import WTCControls_basic as wtc
import wx

LABEL_BACKGROUND = '#000000'
LABEL_FONT_COLOR = '#FFFFFF'
LABEL_OUTLINE_COLOR = '#8FDA02'
DYNLABEL_FONT_COLOR = '#000000'
DYNLABEL_BACKGROUND = '#FFFFFF'
DYNLABEL_OUTLINE_COLOR = '#32A8DA'

WARNING = '#FF0004'

TEXT_SCALE = 2

class Label:
	def __init__(self, pos=(0,0), text=None):
		self.pos = pos
		self.text = text
	
	def Draw(self, canvas):
		Canvas = canvas
		self.label = Canvas.AddScaledTextBox(self.text,
                                          self.pos,
                                          TEXT_SCALE,
                                          Color = LABEL_FONT_COLOR,
                                          BackgroundColor = LABEL_BACKGROUND,
                                          LineColor = LABEL_OUTLINE_COLOR,
                                          PadSize = 3,
                                          Position = 'tl',
                                          Alignment = 'center')

class DynLabel:
	def __init__(self, pos=(0,0), text=None, value=None):
		self.pos = pos
		self.text = text
		self.value = value
		self.BuildLabel()

	def BuildLabel(self):
		self.output_label = self.text + '\n'
		if self.value:
			for key, data in self.value.iteritems():
				self.output_label = self.output_label + key + ': ' + str(data) + '\n'


	def Draw(self, canvas, label_background_color=DYNLABEL_BACKGROUND, line_color=DYNLABEL_OUTLINE_COLOR,
																	color=DYNLABEL_FONT_COLOR, padsz=5, 
																	position='tl', alignment='center', width=None, 
																	text_scale=TEXT_SCALE):
		self.label = canvas.AddScaledTextBox(self.output_label,
                                              self.pos,
                                              text_scale,
                                              Color = color,
                                              BackgroundColor = label_background_color,
                                              LineColor = line_color,
                                              Width=width,
                                              PadSize = padsz,
                                              Position = position,
                                              Alignment = alignment, Family=wx.MODERN)

class Resevoir:
	def __init__(self, pos=(0,0), text='Resevoir', scale=10, height=3, width=10, label=True):
		self.pos = pos
		self.scale = scale
		self.label = label
		self.height = height * self.scale
		self.ellip_height = height * self.scale / 2
		self.width = width * self.scale
		self.text = text

	def Draw(self, canvas):
		self.resevoir = canvas.AddRectangle((self.pos[0], self.pos[1]-self.height+self.ellip_height/2), (self.width+1, self.height), FillColor=wtc.TANK_BACKGROUND_COLOR)
		canvas.AddEllipse((self.pos[0], self.pos[1]-self.height), (self.width, self.ellip_height), FillColor=wtc.TANK_BACKGROUND_COLOR)
		canvas.AddEllipse(self.pos, (self.width, self.ellip_height), FillColor=wtc.TANK_BACKGROUND_COLOR)
		if self.text:
			canvas.AddScaledText(self.text, (self.pos[0]+self.width/4+self.width/6, self.pos[1]-self.ellip_height/2), Size=TEXT_SCALE)
   
class Alert:
	def __init__(self, canvas, pos=(0,0), msg='Alert'):
		self.canvas = canvas
		self.pos = pos
		
		self.label = canvas.AddScaledTextBox(msg,
                                              self.pos,
                                              TEXT_SCALE,
                                              Color = 'RED',
                                              BackgroundColor = 'WHITE',
                                              LineColor = 'RED',
                                              Width=18,
                                              PadSize = 2,
                                              Position = 'cc',
                                              Alignment = 'left', 
                                              Family=wx.MODERN, InForeground=True)
		self.icon = canvas.AddScaledBitmap(wx.Bitmap('rsrc/icons/alert.png'), (self.pos[0]+2, self.pos[1]+3), Height=6, Position='tl', InForeground=True)
		self.blink = False
		
	def Show(self):
		self.label.Show()
		self.icon.Show()
		
	def Hide(self):
		self.label.Hide()
		self.icon.Hide()
		
	def Blink(self, blink):
		self.blink = blink
		if blink:
			self.icon.Show()
		else:
			self.icon.Hide()
	
	def GetBlink(self):
		return self.blink

