#!/usr/bin/env

import wx
from wx.lib.floatcanvas import NavCanvas, FloatCanvas, Resources
from lib import WTCControls as wtc
from lib import WTCControls_basic as wtc_b
from lib import WTCShapes as wtc_s
import threading
from PyOPC.XDAClient import XDAClient
from PyOPC.OPCContainers import *
from lib import Process
from time import sleep

BACKGROUND_COLOR='#EEEEEE'

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
	ps_attrs = ('http://localhost:8000', ['PUMP'], [ItemContainer(ItemName='PUMP')])
	def __init__(self, *args, **kwargs):
		super(TopLevelFrame, self).__init__(*args, **kwargs)
		self.NC = NavCanvas.NavCanvas(self, BackgroundColor = BACKGROUND_COLOR)
		self.Canvas = self.NC.Canvas
		
		pump_pipe = wtc.PumpPipeNetwork(name='Basic', masterTag='PUMP_NET')
		
		res = wtc_s.WaterTower(pos=(22,80),scale=2)
		pump_pipe.AddObject(res, self.Canvas)
		pump_pipe.AddObject(wtc_b.Pipe((-47, 29), length=81), self.Canvas)
		pump_pipe.AddObject(wtc_b.Pipe((32, 60), width=1, length=30, horizontal=False), self.Canvas)
		pump_pipe.AddObject(wtc_b.Pump((-50, 30), name='PUMP'), self.Canvas, masterTag='PUMP', append=True)
		
		pump = pump_pipe.ReturnPump()
		self.pumps = []
		self.pumps.append(pump)
		
		pump.pump.Bind(FloatCanvas.EVT_FC_ENTER_OBJECT, self.MouseOver)
		pump.pump.Bind(FloatCanvas.EVT_FC_LEAVE_OBJECT, self.MouseOut)
		pump.pump.Bind(FloatCanvas.EVT_FC_LEFT_DOWN, self.EnableDisableDlg)
		
		res.Draw(self.Canvas)
		
		(opc_addr, master_tags, tags) = self.ps_attrs
		self.InitializePanel(opc_addr, tags)
		self.networks = []
		self.networks.append(pump_pipe)
		pump_pipe.assets.append(Process.ProcessObject('PUMP', 0, '==', None, None))
		
		self.CreatePumpBeats()
		
		self.Canvas.SetSize((900,900))
		self.SetTitle('Pump HMI')
		self.Maximize(True)
		self.Show(True)
		
	def MouseOver(self, e):
		self.SetCursor(wx.StockCursor(wx.CURSOR_HAND))

	def MouseOut(self, e):
		self.SetCursor(wx.NullCursor)
		
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
		
	def InitializePanel(self, addr, item):
		self.xda = XDAClient(OPCServerAddress=addr)
		(i,rd) = self.xda.Subscribe(item, SubscriptionPingRate=50000)
		self.subhandle = rd['ServerSubHandle']
		EVT_RESULT_ID = wx.NewId()
		EVT_RESULT(self, EVT_RESULT_ID, self.SubscriptionReceived)
		self.worker = WorkerThread(self, self.xda, self.subhandle, EVT_RESULT_ID)
		
	def SubscriptionReceived(self, e):
		status = 0
		for skip,item in enumerate(e.data):
			self.RefreshState(item, self.networks)

	def RefreshState(self, item, procs):
		for skip,net in enumerate(procs):
			asset = net.ReturnAsset(item.ItemName)
			if asset:
				asset.UpdateState(item.Value)
				net.Online()
				
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
		
	def CreatePumpBeats(self):
		self.which_beat = True
		self.timer = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self.BeatPumps, self.timer)
		self.timer.Start(500)
		
class HMIApp(wx.App):
	def OnInit(self):
		frame = TopLevelFrame(None)
		return True
		
def main():
	app = HMIApp(False)
	app.MainLoop()
	
if __name__ == '__main__':
	main()
