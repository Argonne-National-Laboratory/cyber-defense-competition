import wx
import time

class WTCStatusBar(wx.StatusBar):
	def __init__(self, *args, **kwargs):
		wx.StatusBar.__init__(self, *args, **kwargs)
		self.SetFieldsCount(1)
		self.SetStatusText(time.strftime('%d-%b-%Y   %I:%M:%S'), 0)
		self.Time_Timer = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self.GetParent().TopLevelTimers, self.Time_Timer)
		self.Time_Timer.Start(500)
         
	def RefreshTime(self, e):
		self.SetStatusText(time.strftime('%d-%b-%Y   %I:%M:%S'), 0)

class Disinfection_Dialog(wx.Dialog):
	def __init__(self, *args, **kwargs):
		super(Disinfection_Dialog, self).__init__(*args, **kwargs)
		self.sc = wx.SpinCtrl(self, -1, 'Tank level')
		self.sc.SetRange(1,10)
		vbox = wx.BoxSizer(wx.VERTICAL)

		hbox1 = wx.BoxSizer(wx.HORIZONTAL)
		hbox1.Add(self.sc)

		hbox2 = wx.BoxSizer(wx.HORIZONTAL)
		self.okButton = wx.Button(self, label='Ok')
		self.closeButton = wx.Button(self, label='Close')

		hbox2.Add(self.closeButton, flag=wx.LEFT, border=5)
		hbox2.Add(self.okButton)

		vbox.Add(hbox1, proportion=1, flag=wx.ALL|wx.EXPAND, border=5)
		vbox.Add(hbox2,flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=10)

		self.Bind(wx.EVT_BUTTON, self.Submit, self.okButton)
		self.Bind(wx.EVT_BUTTON, self.Cancel, self.closeButton)
		self.SetSizer(vbox)

	def Submit(self, e):
		self.setTankValue = self.sc.GetValue()
		self.Close()
	
	def Cancel(self, e):
		self.Close()
		return 0

class Clarification_Dialog(wx.Dialog):
	def __init__(self, *args, **kwargs):
		super(Clarification_Dialog, self).__init__(*args, **kwargs)
