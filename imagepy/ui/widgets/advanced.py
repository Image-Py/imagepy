from . normal import Choice, Choices
from ...core.manager import ImageManager, TableManager

class ImageList(Choice):
	def __init__(self, parent, title, unit):
		Choice.__init__(self, parent, ImageManager.get_titles(), str, title, unit)

class TableFields(Choices):
	def __init__(self, parent, title):
		self.tps = TableManager.get()
		Choices.__init__(self, parent,  self.tps.data.columns, title)
		
	def SetValue(self, value):
		Choices.SetValue(self, self.tps.colmsk)