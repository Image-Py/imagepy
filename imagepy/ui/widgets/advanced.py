from . normal import Choice, Choices
from ...core.manager import ImageManager, TableManager

class ImageList(Choice):
	def __init__(self, parent, title, unit):
		Choice.__init__(self, parent, ImageManager.get_titles(), str, title, unit)

class TableFields():
	def __init__(self, parent, title):
		Choices.__init__(self, parent, TableManager.get_titles(), title)
