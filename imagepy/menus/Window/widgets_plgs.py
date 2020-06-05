from imagepy.core.engine import Free

class Widgets(Free):
	"""ImageKiller: derived from imagepy.core.engine.Free"""
	title = 'Widgets'
	asyn = False

	def run(self, para = None):
		self.app.switch_widget()

class ToolBar(Free):
	title = 'Toolbar'
	asyn = False
	
	def run(self, para = None):
		self.app.switch_toolbar()

class TableWindow(Free):
	"""ImageKiller: derived from imagepy.core.engine.Free"""
	title = 'Tables Window'
	asyn = False
	
	#process
	def run(self, para = None):
		self.app.switch_table()

plgs = [Widgets, ToolBar, TableWindow]