class Widget():
	def __init__(self, panel):
		self.panel = panel
		self.title = panel.title

	def __call__(self): return self

	def start(self, app):
		app.show_widget(self.panel)