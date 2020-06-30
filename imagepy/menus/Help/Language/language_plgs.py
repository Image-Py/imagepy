from sciapp.action import Free
from imagepy.app import ConfigManager, DictManager

class Language(Free):
	def __init__(self, key):
		self.title = key
		asyn = False

	def run(self, para = None):
		ConfigManager.add('language', self.title)
		self.app.load_all()

	def __call__(self):
		return self

plgs = [Language(i) for i in DictManager.get('language')]