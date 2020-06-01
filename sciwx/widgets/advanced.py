from . normal import Choice, Choices
from . colormap import CMapSelPanel
# from ...core.manager import ImageManager, TableManager, ColorManager

class ImageList(Choice):
	def __init__(self, parent, title, unit, app=None):
		Choice.__init__(self, parent, app.get_img_name(), str, title, unit)

class TableList(Choice):
	def __init__(self, parent, title, unit, app=None):
		Choice.__init__(self, parent, app.get_tab_name(), str, title, unit)

class TableField(Choice):
	def __init__(self, parent, title, unit, app=None):
		Choice.__init__(self, parent,  ['None'] + list(app.get_tab().data.columns), lambda x:x, title, unit)

class TableFields(Choices):
	def __init__(self, parent, title, app=None):
		self.tps = app.get_tab()
		Choices.__init__(self, parent,  app.get_tab().data.columns, title)
	
	def SetValue(self, value):
		Choices.SetValue(self, self.tps.colmsk)
	
class ColorMap(CMapSelPanel):
	def __init__(self, parent, title, app=None):
		CMapSelPanel.__init__(self, parent, title)
		self.SetItems(ColorManager.luts)