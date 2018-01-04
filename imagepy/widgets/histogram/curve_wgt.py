from ...ui.widgets import CurvePanel

class Plugin(CurvePanel):
	title = 'Curve Adjust'
	def __init__(self, parent):
		CurvePanel.__init__(self, parent)