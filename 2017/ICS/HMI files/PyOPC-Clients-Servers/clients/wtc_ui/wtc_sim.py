#!/usr/bin/env python

import wx, wx.media
import os
import math
import random,copy,threading
from wx.lib.floatcanvas import NavCanvas, FloatCanvas, Resources
from time import strftime, sleep
from PyOPC.XDAClient import XDAClient
from PyOPC.OPCContainers import *
from rsrc import water_treatment_items_client
from lib import wxWTC,WTCShapes,OPCHelpers
from lib import WTCControls_basic as wtc_b
from lib import WTCControls as wtc
from lib import Process
from wx.lib.ticker import Ticker
import logging, shutil, ConfigParser

BACKGROUND_COLOR = '#EEEEEE'
LOG_FILENAME = 'wtc.log'

log_save_filter = 'Log files (*.log)| *.log| All files (*.*)|*.*'

def EVT_RESULT(win, event, func):
	win.Connect(-1, -1, event, func)

class ResultEvent(wx.PyEvent):
	def __init__(self, event, data):
		wx.PyEvent.__init__(self)
		self.SetEventType(event)
		self.data = data

class WorkerThread(threading.Thread):
	def __init__(self, notify_window, xda, handle, event):
		threading.Thread.__init__(self)
		self.xda = xda
		self.subhandle = handle
		self.notify_window = notify_window
		self.event = event
		self.daemon = True
		self.start()

	def run(self):
		while True:
			(inIClist, inOptions) = self.xda.SubscriptionPolledRefresh(ServerSubHandles=self.subhandle,
																   ReturnAllItems=False)
			if inIClist:
				wx.PostEvent(self.notify_window, ResultEvent(self.event, inIClist))
			sleep(1)

class TopLevelFrame(wx.Frame):

	config = ConfigParser.ConfigParser()
	config.read('wtc.cfg')
	tc_attrs = (config.get('treatment_center', 'address'), water_treatment_items_client.tc_master_tags, water_treatment_items_client.WTCOPCItems)
	ps_attrs = [(config.get('pump_station_0', 'address'), water_treatment_items_client.ps0_master_tags, water_treatment_items_client.PS0OPCItems),
				(config.get('pump_station_1', 'address'), water_treatment_items_client.ps1_master_tags, water_treatment_items_client.PS1OPCItems),
				(config.get('pump_station_2', 'address'), water_treatment_items_client.ps2_master_tags, water_treatment_items_client.PS2OPCItems),
				(config.get('pump_station_3', 'address'), water_treatment_items_client.ps3_master_tags, water_treatment_items_client.PS3OPCItems),
				(config.get('pump_station_4', 'address'), water_treatment_items_client.ps4_master_tags, water_treatment_items_client.PS4OPCItems),
				(config.get('pump_station_5', 'address'), water_treatment_items_client.ps5_master_tags, water_treatment_items_client.PS5OPCItems)]

	def __init__(self, *args, **kwargs):
		super(TopLevelFrame, self).__init__(*args, **kwargs)

		logging.basicConfig(filename=LOG_FILENAME, filemode='w+', level=logging.INFO, datefmt='%d-%b-%Y   %I:%M:%S', format='%(asctime)s %(levelname)s %(message)s')

		hsizer0 = wx.BoxSizer(wx.HORIZONTAL)
		hsizer1 = wx.BoxSizer(wx.HORIZONTAL)
		vsizer0 = wx.BoxSizer(wx.VERTICAL)
		self.NC = []
		self.Canvas = []
		self.current_canvas = None

		self.alert_sound = wx.media.MediaCtrl(self, style=wx.SIMPLE_BORDER)
		self.alert_sound.Load('rsrc/sounds/sonar.ogg')
		self.alarm_sound = wx.media.MediaCtrl(self, style=wx.SIMPLE_BORDER)
		self.alarm_sound.Load('rsrc/sounds/alarm-short.wav')

		self.log = wx.TextCtrl(self, wx.NewId(), style=wx.TE_MULTILINE|wx.TE_READONLY)
		self.log.Hide()

		for i in range(8):
			self.NC.append(NavCanvas.NavCanvas(self, BackgroundColor = BACKGROUND_COLOR))
			self.NC[i].Hide()
			self.Canvas.append(self.NC[i].Canvas)
			self.Canvas[i].SetSize((900,900))
			hsizer1.Add(self.NC[i], 1, wx.EXPAND|wx.ALL)

		self.procs = []
		for i in range(6):
			self.procs.append(PumpPanel(parent=self))
			self.procs[i].BuildFrame(i, self.ps_attrs[i], self.Canvas[i], 'Pump Station ' + str(i))

		self.procs.append(TreatmentPanel(parent=self))
		self.procs[6].BuildFrame(self.tc_attrs, self.Canvas[6], 'Treatment Center')
		self.procs.append(OverviewPanel(parent=self))
		self.procs[7].BuildFrame(self.Canvas[7])

		self.sb = wxWTC.WTCStatusBar(self)
		self.ticker = Ticker(self, start=False)
		self.ticker.SetPPF(4)

		hsizer0.Add(self.sb, 0)
		vsizer0.Add(hsizer0, 0)
		vsizer0.Add(hsizer1, 1, wx.EXPAND|wx.ALL)
		vsizer0.Add(self.log, 1, wx.EXPAND | wx.ALL)
		vsizer0.Add(self.ticker, flag=wx.EXPAND|wx.ALL)

		menubar = wx.MenuBar()
		filemenu = wx.Menu()
		logmenu = wx.Menu()
		sitemenu = wx.Menu()

		f_exit = filemenu.Append(wx.ID_EXIT, 'E&xit', 'Exit application')
		log_view = logmenu.Append(wx.ID_ANY, '&View Log', 'View current log')
		log_refresh = logmenu.Append(wx.ID_ANY, '&Refresh Log', 'Refresh Log')
		log_save = logmenu.Append(wx.ID_ANY, 'Sa&ve Log', 'Save the log')
		overview = sitemenu.Append(wx.ID_ANY, '&Overview', 'Network Overview')
		treat_fac = sitemenu.Append(wx.ID_ANY, '&Treatment Facility', 'Treatment Facility')
		pump_0 = sitemenu.Append(wx.ID_ANY, 'Pump Facility &1', 'Pump Maintaince')
		pump_1 = sitemenu.Append(wx.ID_ANY, 'Pump Facility &2', 'Pump Maintaince')
		pump_2 = sitemenu.Append(wx.ID_ANY, 'Pump Facility &3', 'Pump Maintaince')
		pump_3 = sitemenu.Append(wx.ID_ANY, 'Pump Facility &4', 'Pump Maintaince')
		pump_4 = sitemenu.Append(wx.ID_ANY, 'Pump Facility &5', 'Pump Maintaince')
		pump_5 = sitemenu.Append(wx.ID_ANY, 'Pump Facility &6', 'Pump Maintaince')

		menubar.Append(filemenu, '&File')
		menubar.Append(sitemenu, '&Sites')
		menubar.Append(logmenu, '&Logs')
		self.SetMenuBar(menubar)

		self.Bind(wx.EVT_MENU, self.OnQuit, f_exit)
		self.Bind(wx.EVT_MENU, self.ViewLog, log_view)
		self.Bind(wx.EVT_MENU, self.RefreshLog, log_refresh)
		self.Bind(wx.EVT_MENU, self.SaveLog, log_save)
		self.Bind(wx.EVT_MENU, lambda event: self.SwitchCanvas(event, 7), overview)
		self.Bind(wx.EVT_MENU, lambda event: self.SwitchCanvas(event, 6), treat_fac)
		self.Bind(wx.EVT_MENU, lambda event: self.SwitchCanvas(event, 0), pump_0)
		self.Bind(wx.EVT_MENU, lambda event: self.SwitchCanvas(event, 1), pump_1)
		self.Bind(wx.EVT_MENU, lambda event: self.SwitchCanvas(event, 2), pump_2)
		self.Bind(wx.EVT_MENU, lambda event: self.SwitchCanvas(event, 3), pump_3)
		self.Bind(wx.EVT_MENU, lambda event: self.SwitchCanvas(event, 4), pump_4)
		self.Bind(wx.EVT_MENU, lambda event: self.SwitchCanvas(event, 5), pump_5)

		self.SetSizer(vsizer0)
		self.SetTitle('Water Treatment Facility')
		self.Maximize(True)
		self.Show(True)

		self.current_canvas = self.NC[7]
		self.active_proc = self.procs[7]
		self.active_proc.timer.Start(750)
		self.current_canvas.Show()
		self.current_canvas.Canvas.Draw()
		self.current_canvas.Canvas.ZoomToBB()
		self.Layout()

		self.elog = ''
		self.raise_alarm = False

	def SwitchCanvas(self, e, snum):
		if self.current_canvas:
			self.current_canvas.Hide()
		self.current_canvas = self.NC[snum]
		self.active_proc = self.procs[snum]
		self.current_canvas.Show()
		self.Layout()
		self.Canvas[snum].Draw()
		self.Canvas[snum].ZoomToBB()

	def ViewLog(self, e):
		self.current_canvas.Hide()
		self.current_canvas = self.log
		self.log.LoadFile(LOG_FILENAME)
		self.log.Show()
		self.Layout()

	def RefreshLog(self, e):
		self.log.LoadFile(LOG_FILENAME)

	def SaveLog(self, e):
		dlg = wx.FileDialog(self, message="Save log as...", defaultDir=os.getcwd(),
							defaultFile=LOG_FILENAME, wildcard=log_save_filter, style=wx.SAVE)
		if dlg.ShowModal() == wx.ID_OK:
			path = dlg.GetPath()
			try:
				shutil.copyfile(LOG_FILENAME, path)
			except e:
				print str(e)
				print 'Could not save file because problems.'
		dlg.Destroy()

	def TopLevelTimers(self, e):
		self.sb.SetStatusText(time.strftime('%d-%b-%Y   %I:%M:%S'), 0)
		self.ticker.OnTick(e)
		if not isinstance(self.active_proc, OverviewPanel):
			self.active_proc.BeatPumps(None)

	def OnQuit(self, e):
		self.Close()

class NetworkCorr:
	def __init__(self, node, edges, prev_edge, process):
		self.node = node
		self.edges = edges
		self.proc = process
		self.prev = prev_edge

	def Update(self):
		self.UpdateNodeHealth()
		self.UpdateEdgeHealth()

	def UpdateNodeHealth(self):
		if not self.proc.health:
			color = 'Red'
		elif self.proc.health == 1:
			color = 'Orange'
		else:
			color = 'Green'

		if type(self.node) == wx.lib.floatcanvas.FloatCanvas.ScaledTextBox:
			self.node.SetColor(color)
		else:
			self.node.SetFillColor(color)

	def UpdateEdgeHealth(self):
		if self.edges:
			for skip, edge in enumerate(self.edges):
				if not self.proc.out:
					edge.SetLineColor('Red')
				elif self.proc.health == 1:
					edge.SetLineColor('Purple')
				else:
					edge.SetLineColor('Blue')

class GenericPanel(wx.Panel):
	def __init__(self, *args, **kwargs):
		wx.Panel.__init__(self, *args, **kwargs)

	def MouseOver(self, e):
		self.GetParent().SetCursor(wx.StockCursor(wx.CURSOR_HAND))

	def MouseOut(self, e):
		self.GetParent().SetCursor(wx.NullCursor)

class OverviewPanel(GenericPanel):
	def __init__(self, *args, **kwargs):
		GenericPanel.__init__(self, *args, **kwargs)

	def BuildFrame(self, canvas):
		self.Canvas = canvas
		self.corr = []
		self.alert_switch = True
		self.Canvas.AddScaledTextBox('Pump Station (healthy):\nPump Station (caution):\nPump Station (critical):\nResevoir:',
											 (15,-47),
											 WTCShapes.TEXT_SCALE,
											 Color = WTCShapes.DYNLABEL_FONT_COLOR,
											 BackgroundColor = WTCShapes.DYNLABEL_BACKGROUND,
											 LineColor= WTCShapes.DYNLABEL_OUTLINE_COLOR,
											 Width=50,
											 PadSize = 2,
											 Position = 'cc',
											 Alignment='left')
		self.Canvas.AddCircle((33, -42.5), 2, FillColor='Green')
		self.Canvas.AddCircle((33, -45.5), 2, FillColor='Orange')
		self.Canvas.AddCircle((33, -48.5), 2, FillColor='Red')
		self.Canvas.AddRectangle((32.1, -52.5), (2,2), FillColor='BLUE')

		self.Canvas.AddLine(((-40,51),(-20,51)), LineWidth=2, LineColor='BLUE')
		self.Canvas.AddScaledTextBox('source',
											 (-40,51),
											 WTCShapes.TEXT_SCALE,
											 Color = WTCShapes.DYNLABEL_FONT_COLOR,
											 BackgroundColor = WTCShapes.DYNLABEL_BACKGROUND,
											 LineColor= WTCShapes.DYNLABEL_OUTLINE_COLOR,
											 Width=12,
											 PadSize = 2,
											 Position = 'cc',
											 Alignment='center')
		self.Canvas.AddScaledTextBox('\nRESERVOIR\n',
											 (-20,51),
											 WTCShapes.TEXT_SCALE,
											 Color = WTCShapes.DYNLABEL_FONT_COLOR,
											 BackgroundColor = WTCShapes.DYNLABEL_BACKGROUND,
											 LineColor= WTCShapes.DYNLABEL_OUTLINE_COLOR,
											 Width=20,
											 PadSize = 2,
											 Position = 'cc',
											 Alignment='center')
		self.Canvas.AddScaledBitmap(wx.Bitmap('rsrc/img/ames.png'), (0,0), Height=75, Position='cc')
		self.pipes = []
		self.Canvas.AddLine(((-10,51.5),(-5,51.5)), LineWidth=2, LineColor='BLUE')
		self.Canvas.AddLine(((-10,50.5),(-5,50.5)), LineWidth=2, LineColor='BLUE')
		self.pipes.append(self.Canvas.AddLine(((-4,51),(10,51)), LineWidth=2, LineColor='BLUE', InForeground=True))
		self.pipes.append(self.Canvas.AddLine(((10.5,47),(10.5,43)), LineWidth=2, LineColor='BLUE', InForeground=True))
		self.pipes.append(self.Canvas.AddLine(((10.5,43),(-35,20)), LineWidth=2, LineColor='BLUE', InForeground=True))
		self.pipes.append(self.Canvas.AddLine(((10.5,43),(6,20)), LineWidth=2, LineColor='BLUE', InForeground=True))
		self.pipes.append(self.Canvas.AddLine(((-35,20),(-35,-20)), LineWidth=2, LineColor='BLUE', InForeground=True))
		self.pipes.append(self.Canvas.AddLine(((6,20),(5.5,-15)), LineWidth=2, LineColor='BLUE', InForeground=True))

		self.ps = []
		self.ps.append(self.Canvas.AddCircle((-5,51), 2, FillColor='Green', InForeground=True))

		treatment_center = self.Canvas.AddScaledTextBox('TREATMENT\nCENTER',
											 (10,51),
											 WTCShapes.TEXT_SCALE,
											 Color = WTCShapes.DYNLABEL_FONT_COLOR,
											 BackgroundColor = WTCShapes.LABEL_BACKGROUND,
											 LineColor= WTCShapes.DYNLABEL_OUTLINE_COLOR,
											 Width=20,
											 PadSize = 2,
											 Position = 'cc',
											 Alignment='center', InForeground=True)
		treatment_center.Bind(FloatCanvas.EVT_FC_ENTER_OBJECT, self.MouseOver)
		treatment_center.Bind(FloatCanvas.EVT_FC_LEAVE_OBJECT, self.MouseOut)
		treatment_center.Bind(FloatCanvas.EVT_FC_LEFT_DOWN, lambda event: self.Parent.SwitchCanvas(None, 6))

		self.ps.append(self.Canvas.AddCircle((10.5,43), 2, FillColor='Green', InForeground=True))

		self.ps.append(self.Canvas.AddCircle((-35, 20), 2, FillColor='Green', InForeground=True))
		self.Canvas.AddRectangle((-36,21.5), (2,2), FillColor='Blue')

		self.ps.append(self.Canvas.AddCircle((6, 20), 2, FillColor='Green', InForeground=True))
		self.Canvas.AddRectangle((4, 21.5), (2,2), FillColor='Blue')

		self.ps.append(self.Canvas.AddCircle((-35, -20), 2, FillColor='Green', InForeground=True))
		self.Canvas.AddRectangle((-36, -23.5), (2,2), FillColor='Blue')

		self.ps.append(self.Canvas.AddCircle((5.5, -15), 2, FillColor='Green', InForeground=True))
		self.Canvas.AddRectangle((4, -18.5), (2,2), FillColor='Blue')

		self.ps.append(treatment_center)

		self.quality_display = self.Canvas.AddScaledTextBox('Sanitation Units: ',
											 (-27,-47),
											 WTCShapes.TEXT_SCALE,
											 Color = WTCShapes.DYNLABEL_FONT_COLOR,
											 BackgroundColor = WTCShapes.DYNLABEL_BACKGROUND,
											 LineColor= WTCShapes.DYNLABEL_OUTLINE_COLOR,
											 Width=30,
											 PadSize = 2,
											 Position = 'cc',
											 Alignment='center',
											 Family=wx.SCRIPT, InForeground=True)

		self.alert = WTCShapes.Alert(self.Canvas, (35, 51))
		self.alert.Hide()

		self.alert.label.Bind(FloatCanvas.EVT_FC_ENTER_OBJECT, self.MouseOver)
		self.alert.label.Bind(FloatCanvas.EVT_FC_LEAVE_OBJECT, self.MouseOut)
		self.alert.label.Bind(FloatCanvas.EVT_FC_LEFT_DOWN, self.AlertDialog)

		self.corr.append(NetworkCorr(self.ps[0], [self.pipes[0]], None, self.GetParent().procs[0]))
		self.corr.append(NetworkCorr(self.ps[6], [self.pipes[1]], self.GetParent().procs[0], self.GetParent().procs[6]))
		self.corr.append(NetworkCorr(self.ps[1], [self.pipes[2], self.pipes[3]], self.GetParent().procs[6], self.GetParent().procs[1]))
		self.corr.append(NetworkCorr(self.ps[2], [self.pipes[4]], self.GetParent().procs[1], self.GetParent().procs[2]))
		self.corr.append(NetworkCorr(self.ps[3], [self.pipes[5]], self.GetParent().procs[1], self.GetParent().procs[3]))
		self.corr.append(NetworkCorr(self.ps[4], None, self.GetParent().procs[2], self.GetParent().procs[4]))
		self.corr.append(NetworkCorr(self.ps[5], None, self.GetParent().procs[3], self.GetParent().procs[5]))


		for i in range(6):
			self.ps[i].Bind(FloatCanvas.EVT_FC_ENTER_OBJECT, self.MouseOver)
			self.ps[i].Bind(FloatCanvas.EVT_FC_LEAVE_OBJECT, self.MouseOut)
			self.ps[i].Bind(FloatCanvas.EVT_FC_LEFT_DOWN, lambda event, i=i: self.Parent.SwitchCanvas(None, i))

		self.timer = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self.HealthCheck, self.timer)

	def HealthCheck(self, e):
		for skip, net in enumerate(self.corr):
			net.Update()
		stat = 0
		leng = 0
		node_msg = '|\t '
		status = {2 : 'Healthy', 1 : 'Caution', 0 : 'Critical'}
		for skip,proc in enumerate(self.GetParent().procs):
			if isinstance(proc, OverviewPanel):
				continue
			leng += 1
			if proc.health:
				stat += 1
			node_msg += proc.name + ' : ' + status[proc.health] + '\t|\t '
		if self.GetParent().ticker.GetText() != node_msg:
			self.GetParent().ticker.SetText(node_msg)
		self.quality_display.SetText('Sanitation Units: ' + '{0:.0f}%'.format(float(self.GetParent().procs[6].wquality)*100))
		if len(self.GetParent().elog) > 0:
			self.alert.Show()
			if self.GetParent().raise_alarm:
				self.GetParent().alarm_sound.Play()
			if self.alert.GetBlink():
				self.alert.Blink(False)
			else:
				self.alert.Blink(True)
		if self.Canvas.GetParent().IsShown():
			self.Canvas.Draw()

	def AlertDialog(self, e):
		alert = self.GetParent().elog
		self.GetParent().elog = ''
		dlg = wx.MessageDialog(self, alert, 'ALERT', wx.OK | wx.ICON_INFORMATION)
		dlg.ShowModal()
		dlg.Destroy()
		self.GetParent().raise_alarm = False
		self.alert.Hide()

class ProcPanel(GenericPanel):
	def __init__(self, *args, **kwargs):
		GenericPanel.__init__(self, *args, **kwargs)
		self.pumps = []
		self.state_nodes = 0
		self.health = 2
		self.which_beat = True
		self.status_enum = {'1' : 'Operational', '0' : 'Offline'}
		self.out = True
		self.out_locked = True
		self.critical_nodes = []

	def InitializePanel(self, addr, item):
		self.xda = XDAClient(OPCServerAddress=addr)
		(i,rd) = self.xda.Subscribe(item, SubscriptionPingRate=50000)
		self.subhandle = rd['ServerSubHandle']
		EVT_RESULT_ID = wx.NewId()
		EVT_RESULT(self, EVT_RESULT_ID, self.SubscriptionReceived)
		self.worker = WorkerThread(self, self.xda, self.subhandle, EVT_RESULT_ID)

	def CreatePumpBeats(self):
		self.which_beat = True
		self.timer = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self.BeatPumps, self.timer)

	def BuildNetworks(self):
		for index,net in enumerate(self.networks):
			pump =  net.ReturnPump()
			if pump:
				self.pumps.append(pump)
				pump.pump.Bind(FloatCanvas.EVT_FC_ENTER_OBJECT, self.MouseOver)
				pump.pump.Bind(FloatCanvas.EVT_FC_LEAVE_OBJECT, self.MouseOut)
				pump.pump.Bind(FloatCanvas.EVT_FC_LEFT_DOWN, self.EnableDisableDlg)
			valves = net.ReturnValves()
			if valves:
				for index,valve in enumerate(valves):
					valve.valve.Bind(FloatCanvas.EVT_FC_ENTER_OBJECT, self.MouseOver)
					valve.valve.Bind(FloatCanvas.EVT_FC_LEAVE_OBJECT, self.MouseOut)
					valve.valve.Bind(FloatCanvas.EVT_FC_LEFT_DOWN, self.EnableDisableDlg)
			if isinstance(net.masterTag, tuple):
				for index,tag in enumerate(net.masterTag):
					net.assets.append(Process.ProcessObject(
															   tag,
															   0,
															   '==',
															   [net.masterTag[index:], \
															   net.masterTag[:index-1]],
															   None))
			else:
				net.assets.append(Process.ProcessObject(net.masterTag, 0, '==', None, None))
			self.state_nodes += 1
			self.back.Bind(FloatCanvas.EVT_FC_ENTER_OBJECT, self.MouseOver)
			self.back.Bind(FloatCanvas.EVT_FC_LEAVE_OBJECT, self.MouseOut)
			self.back.Bind(FloatCanvas.EVT_FC_LEFT_DOWN, self.Back)

	def SingleBinding(self, node, focus, func, tag):
		node.assets.append(Process.ProcessObject(tag, 0, '==', None, None))
		focus.Bind(FloatCanvas.EVT_FC_ENTER_OBJECT, self.MouseOver)
		focus.Bind(FloatCanvas.EVT_FC_LEAVE_OBJECT, self.MouseOut)
		focus.Bind(FloatCanvas.EVT_FC_LEFT_DOWN, func)

	def Back(self, e):
		self.GetParent().SwitchCanvas(e, 7)

	def BeatPumps(self, e):
		if self.which_beat:
			self.which_beat = False
			for skip,pump in enumerate(self.pumps):
				pump.status.Visible = True
		else:
			self.which_beat = True
			for skip,pump in enumerate(self.pumps):
				pump.status.Visible = False
		self.Canvas.Draw()

	def SubscriptionReceived(self, e):
		status = 0
		for skip,item in enumerate(e.data):
			self.RefreshState(item, self.networks)
			self.RefreshState(item, self.nodes)

		for skip,net in enumerate(self.networks):
			if net.state:
				status += 1

		if not status:
			self.health = 0
		elif status != self.state_nodes:
			self.health = 1
		else:
			self.health = 2

	def RefreshState(self, item, procs):
		ding = False
		for skip,net in enumerate(procs):
			asset = net.ReturnAsset(item.ItemName)
			if asset:
				msg = item.ItemName + ' changed value: ' + str(item.Value) + '\n'
				logging.info(msg)
				asset.UpdateState(item.Value)
				if net.dirty:
					net.dirty = False
				else:
					if item.Value == '0':
						ding = True
						msg = item.ItemName + ' changed value: ' + self.status_enum[item.Value] + '\n'
						self.GetParent().elog +=  'WARNING: ' + msg
						logging.warn(msg)
				net.Online()
				self.out = False
				for skip,net in enumerate(self.critical_nodes):
					if net.state:
						self.out = True
						self.out_locked = True
				if not self.out and self.out_locked:
					self.out_locked = False
					msg = self.name + ' is no longer outputting\n'
					self.GetParent().elog += 'CRITICAL: ' + msg
					logging.critical(msg)
					self.GetParent().raise_alarm = True
		if ding:
			self.GetParent().alert_sound.Play()

	def EnableDisableDlg(self, e):
		dlg = wx.SingleChoiceDialog(self, e.masterTag, 'Management Menu',  ['Enable', 'Disable'], wx.CHOICEDLG_STYLE)
		if dlg.ShowModal() == wx.ID_OK:
			if dlg.GetStringSelection() == 'Enable':
				value = '1'
			else:
				value = '0'
			self.xda.Write([ItemContainer(ItemName=e.masterTag, Value=value)])
			if isinstance(e.parent, wtc_b.AutomatedValve) or isinstance(e.parent, wtc_b.Pump):
				e.parent.parent.dirty = True
			else:
				e.parent.dirty = True
		dlg.Destroy()

class TreatmentPanel(ProcPanel):
	def __init__(self, *args, **kwargs):
		ProcPanel.__init__(self, *args, **kwargs)

	def BuildFrame(self, tc_attrs, canvas, name):
		self.name = name
		self.Canvas = canvas
		(opc_addr, master_tags, tags) = tc_attrs
		self.InitializePanel(opc_addr, tags)

		self.wquality = 0
		self.networks = []
		self.nodes = []
		self.back = self.Canvas.AddScaledTextBox('Back to Overview',
											 (-140,140),
											 WTCShapes.TEXT_SCALE,
											 Color = WTCShapes.LABEL_FONT_COLOR,
											 BackgroundColor = WTCShapes.LABEL_BACKGROUND,
											 LineColor= WTCShapes.LABEL_OUTLINE_COLOR,
											 Width=20,
											 PadSize = 2,
											 Position = 'cc',
											 Alignment='center')

		self.Canvas.AddScaledTextBox('Pump Station 1',
											 (-140,78),
											 WTCShapes.TEXT_SCALE,
											 Color = WTCShapes.DYNLABEL_FONT_COLOR,
											 BackgroundColor = WTCShapes.DYNLABEL_BACKGROUND,
											 LineColor= WTCShapes.DYNLABEL_OUTLINE_COLOR,
											 Width=20,
											 PadSize = 2,
											 Position = 'cc',
											 Alignment='center')
		self.sulfuric_acid = wtc.ChemicalTank(self.Canvas, (-100,100), 'Sulfuric\nAcid',
											  masterTag=master_tags[0])

		self.SingleBinding(self.sulfuric_acid, self.sulfuric_acid.label, self.EnableDisableDlg, self.sulfuric_acid.masterTag)
		self.nodes.append(self.sulfuric_acid)

		self.ferric_chloride = wtc.ChemicalTank(self.Canvas, (-78, 100), 'Ferric\nChloride',
												masterTag=master_tags[1])
		self.SingleBinding(self.ferric_chloride, self.ferric_chloride.label, self.EnableDisableDlg, self.ferric_chloride.masterTag)
		self.nodes.append(self.ferric_chloride)

		self.net_seg_0 = wtc.PumpPipeNetwork(name='NET_SEG_0', masterTag=master_tags[2])
		self.net_seg_0.AddObject(wtc_b.Pipe((-130,77), length=85, width=3), self.Canvas)
		self.net_seg_0.AddObject(wtc_b.Pipe((-40,77), length=30, width=3), self.Canvas)
		self.net_seg_0.AddObject(wtc_b.Pump((-43,78), name=master_tags[2]), self.Canvas, master_tags[2])

		self.flocculation_basin = wtc.FlocculationBasin((-10,63), self.Canvas)

		self.net_seg_0.AddObject(wtc_b.Pipe((50,77), length=20, width=3), self.Canvas)

		self.ozone_contractor = wtc.OzoneContractor((70,70), self.Canvas,
													 masterTag=(master_tags[3],master_tags[4]))
		self.SingleBinding(self.ozone_contractor.tank, self.ozone_contractor.tank.label, self.EnableDisableDlg, self.ozone_contractor.masterTag[0])
		self.SingleBinding(self.ozone_contractor, self.ozone_contractor.dev, self.EnableDisableDlg, self.ozone_contractor.masterTag[1])
		self.nodes.append(self.ozone_contractor.tank)
		self.nodes.append(self.ozone_contractor)

		self.net_seg_0.AddObject(wtc_b.Pipe((90,77), length=20, width=3), self.Canvas)
		self.networks.append(self.net_seg_0)

		self.net_seg_1 = wtc.PumpPipeNetwork(name='NET_SEG_1', masterTag=master_tags[5])
		self.net_seg_1.AddObject(wtc_b.Pipe((109,77), length=50, width=3, horizontal=False), self.Canvas)
		self.net_seg_1.AddObject(wtc_b.Pump((110,78), name=master_tags[5]), self.Canvas, masterTag=master_tags[5])
		self.net_seg_1.AddObject(wtc_b.Pipe((79,40), length=31, width=2), self.Canvas)
		self.net_seg_1.AddObject(wtc_b.Pipe((79,27), length=31, width=2), self.Canvas)
		self.networks.append(self.net_seg_1)

		self.net_seg_2 = wtc.PumpPipeNetwork(name='NET_SEG_2', masterTag=master_tags[6])
		self.net_seg_3 = wtc.PumpPipeNetwork(name='NET_SEG_3', masterTag=master_tags[7])
		self.net_seg_2.AddObject(wtc_b.Pipe((50,40), length=31, width=2), self.Canvas)
		self.net_seg_3.AddObject(wtc_b.Pipe((50,27), length=31, width=2), self.Canvas)
		self.net_seg_2.AddObject(wtc_b.AutomatedValve((79, 38), name=master_tags[6]), self.Canvas, masterTag=master_tags[6])
		self.net_seg_3.AddObject(wtc_b.AutomatedValve((79, 25), name=master_tags[7]), self.Canvas, masterTag=master_tags[7])

		self.filter_tanks = wtc.FilterTanks((-10,20), self.Canvas)

		self.net_seg_2.AddObject(wtc_b.Pipe((-40, 38), length=30, width=2), self.Canvas)
		self.net_seg_3.AddObject(wtc_b.Pipe((-40, 25), length=30, width=2), self.Canvas)
		self.networks.append(self.net_seg_2)
		self.networks.append(self.net_seg_3)

		self.net_seg_4 = wtc.PumpPipeNetwork(name='NET_SEG_4', masterTag=master_tags[8])
		self.net_seg_5 = wtc.PumpPipeNetwork(name='NET_SEG_5', masterTag=master_tags[9])
		self.net_seg_4.AddObject(wtc_b.Pipe((-45, 38), length=5, width=2), self.Canvas)
		self.net_seg_5.AddObject(wtc_b.Pipe((-45, 25), length=5, width=2), self.Canvas)
		self.net_seg_4.AddObject(wtc_b.Pipe((-45, 38), length=4.5, width=3, horizontal=False), self.Canvas)
		self.net_seg_5.AddObject(wtc_b.Pipe((-45, 31), length=6, width=3, horizontal=False), self.Canvas)
		self.net_seg_4.AddObject(wtc_b.Pipe((-50, 31), length=7.9, width=3), self.Canvas)
		self.net_seg_5.AddObject(wtc_b.Pipe((-50, 31), length=7.9, width=3), self.Canvas)
		self.net_seg_4.AddObject(wtc_b.AutomatedValve((-40, 36), name=master_tags[8]), self.Canvas, masterTag=master_tags[8])
		self.net_seg_5.AddObject(wtc_b.AutomatedValve((-40, 23), name=master_tags[9]), self.Canvas, masterTag=master_tags[9])
		self.networks.append(self.net_seg_4)
		self.networks.append(self.net_seg_5)

		self.chlorine_contact_chamber = wtc.ChlorineChamber((-105, 29), self.Canvas,
															 masterTag=(master_tags[10], master_tags[11]))
		self.SingleBinding(self.chlorine_contact_chamber.chlor, self.chlorine_contact_chamber.chlor.label, self.EnableDisableDlg, self.chlorine_contact_chamber.masterTag[0])
		self.SingleBinding(self.chlorine_contact_chamber.sodium, self.chlorine_contact_chamber.sodium.label, self.EnableDisableDlg, self.chlorine_contact_chamber.masterTag[1])
		self.nodes.append(self.chlorine_contact_chamber.chlor)
		self.nodes.append(self.chlorine_contact_chamber.sodium)

		self.net_seg_4.AddObject(wtc_b.Pipe((-78, 14), length=10, width=3, horizontal=False), self.Canvas)
		self.net_seg_5.AddObject(wtc_b.Pipe((-78, 14), length=10, width=3, horizontal=False), self.Canvas)
		self.clear_well = wtc.ClearWell((-97, -12), self.Canvas)

		self.net_seg_4.AddObject(wtc_b.Pipe((-78, -12), length=10, width=3, horizontal=False), self.Canvas)
		self.net_seg_5.AddObject(wtc_b.Pipe((-78, -12), length=10, width=3, horizontal=False), self.Canvas)

		self.net_seg_6 = wtc.PumpPipeNetwork(name='NET_SEG_6', masterTag=master_tags[12])
		self.net_seg_6.AddObject(wtc_b.Pipe((-77, -25), length=30, width=3), self.Canvas)
		self.net_seg_6.AddObject(wtc_b.Pump((-77, -25), name=master_tags[12]), self.Canvas, masterTag=master_tags[12])
		self.net_seg_6.AddObject(wtc_b.Pipe((-47, -8), length=30, width=2, horizontal=False), self.Canvas)
		self.networks.append(self.net_seg_6)

		self.net_seg_7 = wtc.PumpPipeNetwork(name='NET_SEG_7', masterTag=master_tags[13])
		self.net_seg_8 = wtc.PumpPipeNetwork(name='NET_SEG_8', masterTag=master_tags[14])
		self.net_seg_9 = wtc.PumpPipeNetwork(name='NET_SEG_9', masterTag=master_tags[15])
		self.net_seg_7.AddObject(wtc_b.Pipe((-47, -8), length=15, width=2), self.Canvas)
		self.net_seg_8.AddObject(wtc_b.Pipe((-47, -24), length=15, width=2), self.Canvas)
		self.net_seg_9.AddObject(wtc_b.Pipe((-47, -38), length=15, width=2), self.Canvas)
		self.net_seg_7.AddObject(wtc_b.AutomatedValve(pos=(-44, -10), name=master_tags[13]), self.Canvas, masterTag=master_tags[13])
		self.net_seg_8.AddObject(wtc_b.AutomatedValve(pos=(-44, -26), name=master_tags[14]), self.Canvas, masterTag=master_tags[14])
		self.net_seg_9.AddObject(wtc_b.AutomatedValve(pos=(-44, -40), name=master_tags[15]), self.Canvas, masterTag=master_tags[15])
		self.net_seg_7.AddObject(wtc_b.Pipe((4, -8), length=15, width=2), self.Canvas)
		self.net_seg_8.AddObject(wtc_b.Pipe((4, -24), length=15, width=2), self.Canvas)
		self.net_seg_9.AddObject(wtc_b.Pipe((4, -38), length=15, width=2), self.Canvas)
		self.net_seg_7.AddObject(wtc_b.Pipe((19, -6), length=32, width=2, horizontal=False), self.Canvas)
		self.net_seg_8.AddObject(wtc_b.Pipe((19, -6), length=32, width=2, horizontal=False), self.Canvas)
		self.net_seg_9.AddObject(wtc_b.Pipe((19, -6), length=32, width=2, horizontal=False), self.Canvas)

		self.critical_nodes.append(self.net_seg_7)
		self.critical_nodes.append(self.net_seg_8)
		self.critical_nodes.append(self.net_seg_9)

		self.uv_chambers = wtc.UVChambers((-35, -12), self.Canvas,
											masterTag=[master_tags[16], master_tags[17], master_tags[18]])

		self.SingleBinding(self.uv_chambers, self.uv_chambers.uv0, self.EnableDisableDlg, self.uv_chambers.masterTag[0])
		self.SingleBinding(self.uv_chambers, self.uv_chambers.uv1, self.EnableDisableDlg, self.uv_chambers.masterTag[1])
		self.SingleBinding(self.uv_chambers, self.uv_chambers.uv2, self.EnableDisableDlg, self.uv_chambers.masterTag[2])
		self.nodes.append(self.uv_chambers)
		self.Canvas.AddScaledTextBox('UV Chambers',
											 (-14, -48),
											 WTCShapes.TEXT_SCALE,
											 Color = WTCShapes.DYNLABEL_FONT_COLOR,
											 BackgroundColor = WTCShapes.DYNLABEL_BACKGROUND,
											 LineColor= WTCShapes.DYNLABEL_OUTLINE_COLOR,
											 Width=20,
											 PadSize = 2,
											 Position = 'cc',
											 Alignment='center')

		self.net_seg_7.AddObject(wtc_b.Pipe((20, -24), length=122, width=3), self.Canvas)
		self.net_seg_8.AddObject(wtc_b.Pipe((20, -24), length=122, width=3), self.Canvas)
		self.net_seg_9.AddObject(wtc_b.Pipe((20, -24), length=122, width=3), self.Canvas)
		self.networks.append(self.net_seg_7)
		self.networks.append(self.net_seg_8)
		self.networks.append(self.net_seg_9)

		self.flouride = wtc.ChemicalTank(self.Canvas, (50, -4), 'Flouride', masterTag=master_tags[19])
		self.SingleBinding(self.flouride, self.flouride.label, self.EnableDisableDlg, self.flouride.masterTag)
		self.nodes.append(self.flouride)
		self.ortho_phosphate = wtc.ChemicalTank(self.Canvas, (80, -1), 'Ortho-\nphosphate', masterTag=master_tags[20])
		self.SingleBinding(self.ortho_phosphate, self.ortho_phosphate.label, self.EnableDisableDlg, self.ortho_phosphate.masterTag)
		self.nodes.append(self.ortho_phosphate)
		self.Canvas.AddScaledTextBox('DISTRIBUTION\nNETWORK',
											 (144,-22),
											 WTCShapes.TEXT_SCALE,
											 Color = WTCShapes.DYNLABEL_FONT_COLOR,
											 BackgroundColor = WTCShapes.DYNLABEL_BACKGROUND,
											 LineColor= WTCShapes.DYNLABEL_OUTLINE_COLOR,
											 Width=20,
											 PadSize = 2,
											 Position = 'cc',
											 Alignment='center',
											 InForeground=True)
		self.BuildNetworks()

	def SubscriptionReceived(self, e):
		status = 0
		for skip,item in enumerate(e.data):
			if item.ItemName == 'H20_QUALITY':
				self.wquality = item.Value
			self.RefreshState(item, self.networks)
			self.RefreshState(item, self.nodes)

		for skip,net in enumerate(self.networks):
			if net.state:
				status += 1
		if not status:
			self.health = 0
		elif status != self.state_nodes:
			self.health = 1
		else:
			self.health = 2

		if self.net_seg_4.ReturnState() and self.net_seg_5.ReturnState():
			self.chlorine_contact_chamber.tank.UpdateTankFill(5)
		elif self.net_seg_4.ReturnState() or self.net_seg_5.ReturnState():
			self.chlorine_contact_chamber.tank.UpdateTankFill(3)
		else:
			self.chlorine_contact_chamber.tank.UpdateTankFill(0)

class PumpPanel(ProcPanel):
	def __init__(self, *args, **kwargs):
		ProcPanel.__init__(self, *args, **kwargs)

	def BuildFrame(self, pump_number, ps_attrs, canvas, name):
		self.name = name
		self.Canvas = canvas
		(opc_addr, master_tags, tags) = ps_attrs
		self.InitializePanel(opc_addr, tags)
		self.networks = []
		self.nodes = []
		self.back = self.Canvas.AddScaledTextBox('Back to Overview',
											 (-60,100),
											 WTCShapes.TEXT_SCALE,
											 Color = WTCShapes.LABEL_FONT_COLOR,
											 BackgroundColor = WTCShapes.LABEL_BACKGROUND,
											 LineColor= WTCShapes.LABEL_OUTLINE_COLOR,
											 Width=20,
											 PadSize = 2,
											 Position = 'cc',
											 Alignment='center')
		self.Canvas.AddScaledTextBox('Pumping Station ' + str(pump_number+1),
									 (0,100),
									 WTCShapes.TEXT_SCALE,
									 Color = WTCShapes.DYNLABEL_FONT_COLOR,
									 BackgroundColor = WTCShapes.DYNLABEL_BACKGROUND,
									 LineColor= WTCShapes.DYNLABEL_OUTLINE_COLOR,
									 Width=50,
									 PadSize = 2,
									 Position = 'cc',
									 Alignment='center')
		net_seg_0 = wtc.PumpPipeNetwork(name='NET_SEG_0',
							   masterTag = master_tags[0])
		net_seg_0.AddObject(wtc_b.Pipe((-49,68.5), length=40, width=3), self.Canvas)
		net_seg_0.AddObject(wtc_b.Pipe((-79,68.5), length=30, width=3), self.Canvas)
		net_seg_0.AddObject(wtc_b.Pump((-50,70), name=master_tags[0]), self.Canvas)
		net_seg_1 = wtc.PumpPipeNetwork(name='NET_SEG_1',
							   masterTag = master_tags[1])
		net_seg_1.AddObject(wtc_b.Pipe((-49,25.5), length=30, width=3), self.Canvas)
		net_seg_1.AddObject(wtc_b.Pipe((-79,25.5), length=30, width=3), self.Canvas)
		net_seg_1.AddObject(wtc_b.Pump((-50,27), name=master_tags[1]), self.Canvas)
		net_seg_2 = wtc.PumpPipeNetwork(name='NET_SEG_2',
								   masterTag = master_tags[2])
		net_seg_2.AddObject(wtc_b.Pipe((3, 65.5), length=90, width=3), self.Canvas)
		net_seg_2.AddObject(wtc_b.Pipe((-9, 68.5), length=15, width=3), self.Canvas)
		net_seg_2.AddObject(wtc_b.AutomatedValve(pos=(-9, 67.5), name=master_tags[2]), self.Canvas)
		net_seg_3 = wtc.PumpPipeNetwork(name='NET_SEG_3',
								   masterTag = master_tags[3])
		net_seg_3.AddObject(wtc_b.Pipe((-17,25.5), length=20, width=3), self.Canvas)
		net_seg_3.AddObject(wtc_b.Pipe((3, 65.5), length=40, width=3, horizontal=False), self.Canvas)
		net_seg_3.AddObject(wtc_b.AutomatedValve(pos=(-19, 24.5), name=master_tags[3]), self.Canvas)
		net_seg_3.AddObject(wtc_b.Pipe((3, 65.5), length=90, width=3), self.Canvas)

		self.critical_nodes.append(net_seg_2)
		self.critical_nodes.append(net_seg_3)

		self.chlorine = wtc.ChemicalTank(self.Canvas, (40, 86), 'Chlorine', masterTag=master_tags[4])
		self.SingleBinding(self.chlorine, self.chlorine.label, self.EnableDisableDlg, self.chlorine.masterTag)
		self.nodes.append(self.chlorine)

		self.networks.append(net_seg_0)
		self.networks.append(net_seg_1)
		self.networks.append(net_seg_2)
		self.networks.append(net_seg_3)

		self.BuildNetworks()

class HMIApp(wx.App):
	def OnInit(self):
		frame = TopLevelFrame(None)
		return True

def main():
	app = HMIApp(False)
	app.MainLoop()

if __name__ == '__main__':
	main()
