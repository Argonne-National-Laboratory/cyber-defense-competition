#!/usr/bin/env python

import ast, copy
from PyOPC.OPCContainers import *

def create_state_compare(logic, failValue):
	def CheckFailed(cur):
		source = str(failValue) + logic + str(cur)
		node = ast.parse(source, mode='eval')
		return eval(compile(node, '<string>', mode='eval'))
	return CheckFailed

class ProcessObject:
	def __init__(self, name, failValue, cmp_op, depends, next_list, cur=0, state=True):
		self.name = name
		self.dep_list = depends
		self.next_list = next_list
		self.nnodes = []
		self.depends = []
		self.failValue = failValue
		self.state = state
		self.checkFailed = create_state_compare(cmp_op, self.failValue)
		self.cur = cur

	def UpdateState(self, cur, xda):
		self.cur = cur
		if not self.checkFailed(cur):
			self.state = True
			self.Online(xda)
		else:
			self.state = False
			for index,dep in enumerate(self.nnodes):
				dep.Online(xda)

	def Online(self, xda):
		if not self.depends or (not self.state and self.nnodes):
			return self.state
		else:
			for index,dep in enumerate(self.depends):
				if dep.Online(xda):
					if not self.nnodes:
						self.state = True
						xda.Write([ItemContainer(ItemName=self.name, Value=dep.cur)])
					return self.state
			self.state = False
			xda.Write([ItemContainer(ItemName=self.name, Value=str(self.failValue))])
			return self.state
			
	def ReturnState(self):
		return self.state

class QualityProcessObject(ProcessObject):
	def __init__(self, name, failValue, cmp_op, depends, next_list, cur=0, track=False, state=True):
		ProcessObject.__init__(self, name, failValue, cmp_op, depends, next_list, cur, state)
		self.track = track

class ProcessGroup:
	def __init__(self, name, depends, assets, state=True):
		self.name = name
		self.depends = depends
		self.state = state
		self.process_list = []

		module = __import__("lib.assets.%s" % assets)
		plist = getattr(module.assets, assets)
		self.BuildChain(plist.tags)

	def BuildChain(self, plist):
		if not plist:
			return
		for skip,p in enumerate(plist):
			self.process_list.append(ProcessObject(*p))
		self.start = self.process_list[0]
		self.BuildDependencyChain()

	def BuildDependencyChain(self):
		self.BuildReverseChain()
		self.BuildForwardChain()

	def BuildReverseChain(self):
		for skip,p in enumerate(self.process_list):
			deps = p.dep_list
			if deps:
				for skip,dep in enumerate(deps):
					depobj = self.FindProcess(dep)
					if depobj:
						p.depends.append(depobj)

	def BuildForwardChain(self):
		for skip,p in enumerate(self.process_list):
			nxtn = p.next_list
			if nxtn:
				for skip,nxt in enumerate(nxtn):
					depobj = self.FindProcess(nxt)
					if depobj:
						p.nnodes.append(depobj)

	def FindProcess(self, name):
		for skip,p in enumerate(self.process_list):
			if p.name == name:
				return p
		return None

	def Online(self, xda):
		return self._Online(self.start, xda)

	def _Online(self, p, xda):
		if not p.nnodes:
			return p.state
		else:
			for skip,np in enumerate(p.nnodes):
				if np.Online(xda):
					ret =  self._Online(np, xda)
					if ret:
						return ret
					else:
						continue
			return False

class QualityProcessGroup(ProcessGroup):
	tracked = 0
	
	def __init__(self, name, depends, assets, state=True):
		ProcessGroup.__init__(self, name, depends, assets, state)
		self.NumberToTrack()
		
	def NumberToTrack(self):
		for skip, proc in enumerate(self.process_list):
			if proc.track:
				self.tracked += 1
	
	def BuildChain(self, plist):
		if not plist:
			return
		for skip,p in enumerate(plist):
			self.process_list.append(QualityProcessObject(*p))
		self.start = self.process_list[0]
		self.BuildDependencyChain()
		
	def Health(self):
		health = 0
		for skip, proc in enumerate(self.process_list):
			if proc.track:
				if proc.ReturnState():
					health += 1
		return '{:3.2f}'.format(float(health)/self.tracked)
	
	def _Online(self, p, xda):
		for skip,np in enumerate(p.nnodes):
			np.Online(xda)
			self._Online(np, xda)

	def ReturnHealth(self):
		return self.Health()
