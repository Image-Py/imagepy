class SciAction:
	name = 'SciAction'

	def __init__(self): pass

	def start(self, app, para=None, callafter=None): 
		self.app = app
		print(self.name, 'started!')