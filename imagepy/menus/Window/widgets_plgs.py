from imagepy.core.engine import Free
from imagepy import IPy
import wx

class Widgets(Free):
	"""ImageKiller: derived from imagepy.core.engine.Free"""
	title = 'Widgets'
	asyn = False

	#process
	def run(self, para = None):
		app = IPy.curapp
		info = app.auimgr.GetPane(app.widgets)
		info.Show(not info.IsShown())
		app.auimgr.Update()

class ToolBar(Free):
	"""ImageKiller: derived from imagepy.core.engine.Free"""
	title = 'Toolbar'
	asyn = False
	
	#process
	def run(self, para = None):
		app = IPy.curapp
		info = app.auimgr.GetPane(app.toolbar)
		info.Show(not info.IsShown())
		app.auimgr.Update()

plgs = [Widgets, ToolBar]