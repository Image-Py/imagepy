from . normal import Choice, Choices
from . colormap import CMapSelPanel
from ...core.manager import ImageManager, TableManager, ColorManager

class ImageList(Choice):
	def __init__(self, parent, title, unit):
		Choice.__init__(self, parent, ImageManager.get_titles(), str, title, unit)

class TableList(Choice):
	def __init__(self, parent, title, unit):
		Choice.__init__(self, parent, TableManager.get_titles(), str, title, unit)

class TableField(Choice):
	def __init__(self, parent, title, unit):
		self.tps = TableManager.get()
		Choice.__init__(self, parent,  ['None'] + list(self.tps.data.columns), lambda x:x, title, unit)

class TableFields(Choices):
	def __init__(self, parent, title):
		self.tps = TableManager.get()
		Choices.__init__(self, parent,  self.tps.data.columns, title)
		
	def SetValue(self, value):
		Choices.SetValue(self, self.tps.colmsk)

class ColorMap(CMapSelPanel):
	def __init__(self, parent, title):
		CMapSelPanel.__init__(self, parent, title)
		self.SetItems(ColorManager.luts)
