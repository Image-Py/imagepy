from imagepy.ui.workflowwindow import WorkFlowPanel
import threading, wx, os, wx.lib.agw.aui as aui
from imagepy.core.manager import ReaderManager, ViewerManager
from imagepy import IPy

def parse(cont):
	ls = cont.split('\n')
	workflow = {'title':ls[0], 'chapter':[]}
	for line in ls[2:]:
		line = line.strip()
		if line.startswith('## '):
			chapter = {'title':line[3:], 'section':[]}
			workflow['chapter'].append(chapter)
		elif line[1:3] == '. ':
			section = {'title':line[3:]}
		else:
			section['hint'] = line
			chapter['section'].append(section)
	return workflow

class WorkFlow:
	def __init__(self, title, cont):
		self.title = title
		self.workflow = parse(cont)
		self.cont = cont

	def __call__(self):
		return self

	def start(self, para=None, callafter=None):
		pan = WorkFlowPanel(IPy.curapp)
		pan.load(self.cont, self.workflow)
		info = aui.AuiPaneInfo(). DestroyOnClose(True). Left(). Caption(self.title)  .PinButton( True ) \
			.Resizable().FloatingSize( wx.DefaultSize ).Dockable(IPy.uimode()=='ipy').Layer( 5 ) 
		
		if IPy.uimode()=='ipy': info.Dock().Top()
		if IPy.uimode()=='ij': info.Float()
		IPy.curapp.auimgr.AddPane(pan, info)
		IPy.curapp.Layout()
		IPy.curapp.auimgr.Update()

def show_wf(data, title):
	wx.CallAfter(WorkFlow(title, data).start)

ViewerManager.add('wf', show_wf)

def read_wf(path):
	f = open(path, encoding='utf-8')
	cont = f.read()
	f.close()
	print(cont)
	return cont

ReaderManager.add('wf', read_wf, tag='wf')